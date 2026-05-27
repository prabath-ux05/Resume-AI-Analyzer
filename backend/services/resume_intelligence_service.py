import os
import json
import hashlib

from typing import Dict, Any

from utils.logger import logger
from parsers.parser_factory import ParserFactory
from services.ai_orchestrator import AIOrchestrator
from services.local_parser import LocalResumeParser
from models.resume_schemas import ResumeIntelligenceResponse

from prompts.resume.extraction import RESUME_EXTRACTION_PROMPT

from database.redis import get_redis
from database.postgres import AsyncSessionLocal
from models.database_models import ResumeAnalysis

from sqlalchemy import select


class ResumeIntelligenceService:
    """
    Coordinates resume parsing, AI extraction,
    caching, and DB persistence.
    """

    def __init__(self):

        self.ai_orchestrator = AIOrchestrator()
        self.local_parser = LocalResumeParser()

    async def analyze_resume(
        self,
        file_path: str,
        filename: str = "Unknown"
    ) -> Dict[str, Any]:

        logger.info(
            f"Starting resume analysis for: {file_path}"
        )

        # ==================================================
        # 1. Parse Resume
        # ==================================================

        parser = ParserFactory.get_parser(file_path)

        parsed_data = parser.parse(file_path)

        resume_text = parsed_data.get("text", "")
        metadata = parsed_data.get("metadata", {})

        if not resume_text:

            raise ValueError(
                "Could not extract text from the resume."
            )

        # ==================================================
        # 2. Generate File Hash
        # ==================================================

        file_hash = hashlib.sha256(
            resume_text.encode("utf-8")
        ).hexdigest()

        cache_key = f"resume_analysis:{file_hash}"

        logger.info(
            f"DEBUG - File Hash: {file_hash}"
        )

        logger.info(
            f"DEBUG - Parsed Text Length: "
            f"{len(resume_text)} chars"
        )

        # ==================================================
        # 3. Redis Cache Check
        # ==================================================

        redis = get_redis()

        try:

            if redis:

                cached = await redis.get(cache_key)

                if cached:

                    logger.info(
                        f"Cache hit for resume {file_hash}"
                    )

                    result = json.loads(cached)

                    result["metadata"] = metadata
                    result["file_hash"] = file_hash

                    return result

        except Exception as e:

            logger.error(
                f"Redis cache read failed: {e}"
            )

        # ==================================================
        # 4. Local Resume Parsing
        # ==================================================

        logger.info(
            "Extracting sections locally..."
        )

        structured_resume = self.local_parser.parse(
            resume_text
        )

        # ==================================================
        # 5. Prompt Formatting
        # ==================================================

        resume_json_str = json.dumps(
            structured_resume,
            default=str
        )

        prompt = RESUME_EXTRACTION_PROMPT.format(
            resume_json=resume_json_str
        )

        # ==================================================
        # 6. AI Extraction
        # ==================================================

        logger.info(
            "Extracting intelligence via AI..."
        )

        intelligence: ResumeIntelligenceResponse = (
            await self.ai_orchestrator.extract_structured_data(
                prompt=prompt,
                schema=ResumeIntelligenceResponse
            )
        )

        result = intelligence.model_dump()

        logger.info(
            f"DEBUG - ATS Score: "
            f"{result.get('ats_score')}"
        )

        # Advanced debugging strategy for nested payloads (Production safe)
        try:
            summary_payload = {
                k: (v if not isinstance(v, (list, dict)) else f"<{type(v).__name__} size={len(v)}>")
                for k, v in result.items()
            }
            logger.info(f"AI Extraction Profile Summary: {json.dumps(summary_payload)}")
            logger.debug(f"Full AI Payload:\n{json.dumps(result, indent=2, default=str)}")
        except Exception as e:
            logger.warning(f"Could not serialize debug payload: {e}")

        # ==================================================
        # 7. Redis Cache Save
        # ==================================================

        try:

            if redis:

                await redis.set(
                    cache_key,
                    json.dumps(result, default=str),
                    ex=86400 * 7
                )

        except Exception as e:

            logger.error(
                f"Redis cache write failed: {e}"
            )

        # ==================================================
        # 8. PostgreSQL Persistence
        # ==================================================

        try:

            async with AsyncSessionLocal() as db:

                existing = await db.execute(
                    select(ResumeAnalysis).where(
                        ResumeAnalysis.file_hash == file_hash
                    )
                )

                existing_record = existing.scalar_one_or_none()

                if existing_record:

                    logger.info(
                        "Resume already exists in DB."
                    )

                else:

                    db_record = ResumeAnalysis(
                        file_hash=file_hash,
                        filename=filename,
                        parsed_json=structured_resume,
                        intelligence_result=result
                    )

                    db.add(db_record)

                    await db.commit()

                    logger.info(
                        "Saved resume analysis to PostgreSQL."
                    )

        except Exception as e:

            logger.error(
                f"Database persistence failed: {e}"
            )

        # ==================================================
        # 9. Final Response
        # ==================================================

        result["metadata"] = metadata
        result["file_hash"] = file_hash

        logger.info(
            "Resume analysis completed successfully."
        )

        return result