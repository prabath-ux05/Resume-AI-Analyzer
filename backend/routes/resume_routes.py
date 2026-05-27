import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel

from utils.file_handler import save_upload_file
from services.resume_intelligence_service import ResumeIntelligenceService
from services.jd_matcher import match_resume_to_jd
from utils.logger import logger
from utils.rate_limiter import RateLimiter


router = APIRouter()
resume_service = ResumeIntelligenceService()

rate_limit = RateLimiter(requests=5, window=60)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze-resume", dependencies=[Depends(rate_limit)])
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {"pdf"}
    ext = file.filename.split(".")[-1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF is supported currently."
        )

    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = await save_upload_file(file)

        intelligence_result = await resume_service.analyze_resume(
            file_path,
            file.filename
        )

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
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during processing: {str(e)}"
        )


@router.get("/history")
async def get_resume_history():
    from database.postgres import AsyncSessionLocal
    from models.database_models import ResumeAnalysis
    from sqlalchemy import select

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ResumeAnalysis).order_by(
                    ResumeAnalysis.created_at.desc()
                )
            )

            records = result.scalars().all()
            history = []

            for r in records:
                intel = (
                    r.intelligence_result
                    if isinstance(r.intelligence_result, dict)
                    else {}
                )

                ats_score = intel.get("ats_score", 0)
                skills = intel.get("skills", {})

                total_skills = (
                    sum(len(skills[k]) for k in skills)
                    if isinstance(skills, dict)
                    else 0
                )

                history.append({
                    "file_hash": r.file_hash,
                    "filename": r.filename or "Unknown Resume",
                    "created_at": (
                        r.created_at.isoformat()
                        if r.created_at
                        else None
                    ),
                    "ats_score": ats_score,
                    "total_skills": total_skills
                })

            return {"status": "success", "history": history}

    except Exception as e:
        logger.error(f"Error fetching resume history: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch history"
        )


@router.get("/{file_hash}")
async def get_resume_by_hash(file_hash: str):
    from database.postgres import AsyncSessionLocal
    from models.database_models import ResumeAnalysis
    from sqlalchemy import select

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ResumeAnalysis).where(
                    ResumeAnalysis.file_hash == file_hash
                )
            )

            record = result.scalars().first()

            if not record:
                raise HTTPException(
                    status_code=404,
                    detail="Resume not found"
                )

            return {
                "status": "success",
                "filename": record.filename or "Unknown Resume",
                "data": record.intelligence_result
            }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching specific resume: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch resume"
        )


class JobMatchRequest(BaseModel):
    job_description: str
    resume_text: str = None
    file_hash: str = None


@router.post("/job-match")
async def job_match_endpoint(request: JobMatchRequest):
    if not request.job_description:
        raise HTTPException(
            status_code=400,
            detail="Job description is required."
        )

    if not request.resume_text:
        raise HTTPException(
            status_code=400,
            detail="Resume text is required."
        )

    try:
        from database.postgres import AsyncSessionLocal
        from models.database_models import ResumeAnalysis
        from sqlalchemy import select

        intelligence_result = None

        if request.file_hash:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(ResumeAnalysis).where(
                        ResumeAnalysis.file_hash == request.file_hash
                    )
                )

                record = result.scalars().first()

                if record and record.intelligence_result:
                    intelligence_result = record.intelligence_result

        match_result = match_resume_to_jd(
            request.resume_text,
            request.job_description,
            intelligence_result,
            request.file_hash
        )

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
    if not request.file_hash:
        raise HTTPException(
            status_code=400,
            detail="file_hash is required."
        )

    try:
        from database.postgres import AsyncSessionLocal
        from models.database_models import ResumeAnalysis
        from sqlalchemy import select
        from services.role_matcher import generate_role_matches

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ResumeAnalysis).where(
                    ResumeAnalysis.file_hash == request.file_hash
                )
            )

            record = result.scalars().first()

            if not record or not record.intelligence_result:
                raise HTTPException(
                    status_code=404,
                    detail="No analyzed resume found. Please upload and analyze a resume first."
                )

            redis_client = None

            try:
                from database.redis import get_redis
                redis_client = get_redis()
            except ImportError:
                logger.warning("Redis client not available in routes")

            cache_key = f"role_match:v1:{request.file_hash}"

            if not request.force_regenerate and redis_client:
                try:
                    cached_matches = await redis_client.get(cache_key)

                    if cached_matches:
                        import json
                        logger.info(
                            f"Auto Role Match - Returning REDIS cached role matches for hash {request.file_hash}"
                        )

                        return {
                            "status": "success",
                            **json.loads(cached_matches)
                        }

                except Exception as e:
                    logger.warning(
                        f"Redis cache read failed for role matches: {e}"
                    )

            if request.only_cache:
                return {"status": "not_found", "matches": []}

            intelligence = record.intelligence_result

            logger.info(
                f"Auto Role Match - Generating new matches for hash {request.file_hash}"
            )

            role_matches = await generate_role_matches(intelligence)

            if redis_client:
                try:
                    import json

                    await redis_client.set(
                        cache_key,
                        json.dumps(role_matches, default=str),
                        ex=86400
                    )

                except Exception as e:
                    logger.warning(
                        f"Failed to cache role matches in Redis: {e}"
                    )

            try:
                from models.database_models import RoleMatchHistory

                new_history = RoleMatchHistory(
                    file_hash=request.file_hash,
                    matches_json=role_matches,
                    model_version="llama-3.1-8b-instant"
                )

                db.add(new_history)
                await db.commit()

                logger.info(
                    f"Auto Role Match - Appended to DB history for hash {request.file_hash}"
                )

            except Exception as e:
                logger.warning(
                    f"Auto Role Match - Failed to save history to DB: {e}"
                )

            return {
                "status": "success",
                **role_matches
            }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error during auto role match: {e}")
        raise HTTPException(status_code=500, detail=str(e))