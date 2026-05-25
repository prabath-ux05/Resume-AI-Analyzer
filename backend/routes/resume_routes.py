from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from utils.file_handler import save_upload_file
from services.resume_intelligence_service import ResumeIntelligenceService
from pydantic import BaseModel
from services.jd_matcher import match_resume_to_jd
from utils.logger import logger
from utils.rate_limiter import RateLimiter

router = APIRouter()
resume_service = ResumeIntelligenceService()

# 5 requests per minute limit
rate_limit = RateLimiter(requests=5, window=60)

@router.post("/analyze-resume", dependencies=[Depends(rate_limit)])
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to upload a resume and generate comprehensive recruiter-grade intelligence.
    Uses PyMuPDF for extraction and Gemini AI for semantic analysis.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    allowed_extensions = {"pdf"}
    ext = file.filename.split(".")[-1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported currently.")
    
    try:
        # 1. Save the file locally
        file_path = await save_upload_file(file)
        
        # 2. Analyze the resume (Parsing + AI Orchestration)
        intelligence_result = await resume_service.analyze_resume(file_path, file.filename)
        
        return {
            "filename": file.filename,
            "status": "success",
            "data": intelligence_result
        }
    except ValueError as ve:
        logger.error(f"Validation error during resume analysis: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during resume analysis: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")

@router.get("/history")
async def get_resume_history():
    """
    Fetch a list of all historically analyzed resumes.
    """
    from database.postgres import AsyncSessionLocal
    from models.database_models import ResumeAnalysis
    from sqlalchemy import select
    
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ResumeAnalysis).order_by(ResumeAnalysis.created_at.desc())
            )
            records = result.scalars().all()
            
            history = []
            for r in records:
                intel = r.intelligence_result if isinstance(r.intelligence_result, dict) else {}
                ats_score = intel.get("ats_score", 0)
                skills = intel.get("skills", {})
                total_skills = sum(len(skills[k]) for k in skills) if isinstance(skills, dict) else 0
                
                history.append({
                    "file_hash": r.file_hash,
                    "filename": r.filename or "Unknown Resume",
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "ats_score": ats_score,
                    "total_skills": total_skills
                })
                
            return {"status": "success", "history": history}
    except Exception as e:
        logger.error(f"Error fetching resume history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")

@router.get("/{file_hash}")
async def get_resume_by_hash(file_hash: str):
    """
    Fetch the full intelligence result for a specific past resume.
    """
    from database.postgres import AsyncSessionLocal
    from models.database_models import ResumeAnalysis
    from sqlalchemy import select
    
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ResumeAnalysis).where(ResumeAnalysis.file_hash == file_hash)
            )
            record = result.scalars().first()
            
            if not record:
                raise HTTPException(status_code=404, detail="Resume not found")
                
            return {
                "status": "success",
                "filename": record.filename or "Unknown Resume",
                "data": record.intelligence_result
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching specific resume: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch resume")

class JobMatchRequest(BaseModel):
    job_description: str
    resume_text: str = None
    file_hash: str = None

@router.post("/job-match")
async def job_match_endpoint(request: JobMatchRequest):
    """
    Match a resume against a job description using semantic similarity and pre-extracted intelligence.
    """
    if not request.job_description:
        raise HTTPException(status_code=400, detail="Job description is required.")
    
    if not request.resume_text:
        raise HTTPException(status_code=400, detail="Resume text is required.")
        
    try:
        from database.postgres import AsyncSessionLocal
        from models.database_models import ResumeAnalysis
        from sqlalchemy import select
        
        intelligence_result = None
        if request.file_hash:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(ResumeAnalysis).where(ResumeAnalysis.file_hash == request.file_hash)
                )
                record = result.scalars().first()
                if record and record.intelligence_result:
                    intelligence_result = record.intelligence_result
                        
        match_result = match_resume_to_jd(request.resume_text, request.job_description, intelligence_result, request.file_hash)
        return match_result
    except Exception as e:
        logger.error(f"Error during job match: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class AutoMatchRequest(BaseModel):
    file_hash: str
    force_regenerate: bool = False
    only_cache: bool = False

@router.post("/job-match/auto")
async def auto_role_match_endpoint(request: AutoMatchRequest):
    """
    Automatically generate AI-powered role matches from stored resume intelligence.
    No job description needed — uses the analyzed resume as the sole input.
    """
    if not request.file_hash:
        raise HTTPException(status_code=400, detail="file_hash is required.")

    try:
        from database.postgres import AsyncSessionLocal
        from models.database_models import ResumeAnalysis
        from sqlalchemy import select
        from services.role_matcher import generate_role_matches

        # Load stored intelligence from DB
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ResumeAnalysis).where(ResumeAnalysis.file_hash == request.file_hash)
            )
            record = result.scalars().first()

            if not record or not record.intelligence_result:
                raise HTTPException(status_code=404, detail="No analyzed resume found. Please upload and analyze a resume first.")

            # 1. Return cached results if they already exist AND we are not forcing regeneration
            if not request.force_regenerate and getattr(record, 'role_matches', None) and isinstance(record.role_matches, dict) and "matches" in record.role_matches:
                logger.info(f"Auto Role Match - Returning cached role matches for hash {request.file_hash}")
                return {
                    "status": "success",
                    **record.role_matches
                }

            # If only looking for cache and none exists, return specific status
            if request.only_cache:
                return {"status": "not_found", "matches": []}

            # 2. Otherwise generate new matches
            intelligence = record.intelligence_result
            logger.info(f"Auto Role Match - Generating new matches for hash {request.file_hash}")
            role_matches = await generate_role_matches(intelligence)

            # 3. Save to database for persistence
            try:
                record.role_matches = role_matches
                await db.commit()
                logger.info(f"Auto Role Match - Successfully cached role matches for hash {request.file_hash}")
            except Exception as e:
                logger.warning(f"Auto Role Match - Failed to cache role matches: {e}")

            return {
                "status": "success",
                **role_matches
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during auto role match: {e}")
        raise HTTPException(status_code=500, detail=str(e))

