import os
import json
import hashlib
from utils.logger import logger
from parsers.parser_factory import ParserFactory
from services.ai_orchestrator import AIOrchestrator
from services.local_parser import LocalResumeParser
from models.resume_schemas import ResumeIntelligenceResponse
from prompts.resume.extraction import RESUME_EXTRACTION_PROMPT
from typing import Dict, Any

from database.redis import get_redis
from database.postgres import AsyncSessionLocal
from models.database_models import ResumeAnalysis

class ResumeIntelligenceService:
    """
    Coordinates the parsing of a resume, caching, DB persistence,
    and the extraction of intelligence via the AI orchestrator.
    """

    def __init__(self):
        self.ai_orchestrator = AIOrchestrator()
        self.local_parser = LocalResumeParser()

    async def analyze_resume(self, file_path: str, filename: str = "Unknown") -> Dict[str, Any]:
        """
        Analyzes a resume by parsing it and running AI extraction.
        
        Args:
            file_path: The path to the uploaded resume file.
            filename: The original name of the uploaded file.
            
        Returns:
            Dictionary containing the intelligence output.
        """
        logger.info(f"Starting resume analysis for: {file_path}")
        
        # 1. Parse Document raw text
        parser = ParserFactory.get_parser(file_path)
        parsed_data = parser.parse(file_path)
        resume_text = parsed_data.get("text", "")
        metadata = parsed_data.get("metadata", {})
        
        if not resume_text:
            raise ValueError("Could not extract text from the provided resume.")
            
        # 2. Hash raw text for debugging and future caching
        file_hash = hashlib.sha256(resume_text.encode('utf-8')).hexdigest()
        cache_key = f"resume_analysis:{file_hash}"
        redis = get_redis()
        
        # Re-enabled Redis Caching
        if redis:
            cached = await redis.get(cache_key)
            if cached:
                logger.info(f"Cache hit for resume {file_hash}. Skipping AI generation.")
                result = json.loads(cached)
                result["metadata"] = metadata
                result["file_hash"] = file_hash
                return result
        
        logger.info(f"DEBUG - File Hash (SHA256): {file_hash}")
        logger.info(f"DEBUG - Parsed Text Length: {len(resume_text)} chars")

        # 3. Local Heuristic Parsing
        logger.info("Extracting sections locally to minimize prompt payload...")
        structured_resume = self.local_parser.parse(resume_text)
        
        # 4. Format Minimal Prompt
        resume_json_str = json.dumps(structured_resume)
        prompt = RESUME_EXTRACTION_PROMPT.format(resume_json=resume_json_str)
        
        # 5. Call AI Orchestrator
        logger.info("Extracting structured intelligence via AI Orchestrator...")
        intelligence: ResumeIntelligenceResponse = await self.ai_orchestrator.extract_structured_data(
            prompt=prompt,
            schema=ResumeIntelligenceResponse
        )
        
        # 6. Build Result
        result = intelligence.model_dump()
        
        logger.info(f"DEBUG - Extracted Skills: {result.get('skills', {})}")
        logger.info(f"DEBUG - Generated ATS Score: {result.get('ats_score')}")
        
        # 7. Cache Result
        if redis:
            await redis.set(cache_key, json.dumps(result), ex=86400 * 7) # Cache for 7 days
            
        # 8. Database Persistence
        try:
            async with AsyncSessionLocal() as db:
                db_record = ResumeAnalysis(
                    file_hash=file_hash,
                    filename=filename,
                    parsed_json=structured_resume,
                    intelligence_result=result
                )
                db.add(db_record)
                await db.commit()
                logger.info("Saved resume analysis to PostgreSQL.")
        except Exception as e:
            logger.error(f"Failed to persist resume analysis to database: {e}")
        
        result["metadata"] = metadata
        result["file_hash"] = file_hash
        
        logger.info("Resume analysis completed successfully.")
        return result
