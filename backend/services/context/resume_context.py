from typing import Dict, Any, Optional
from sqlalchemy.future import select
from database.postgres import AsyncSessionLocal
from models.database_models import ResumeAnalysis
from utils.logger import logger

class ResumeContextService:
    """
    Dedicated service for fetching structured resume intelligence from PostgreSQL
    to be injected as context for the AI Assistant.
    """
    
    @staticmethod
    def _build_optimized_context(intelligence: Dict[str, Any]) -> str:
        """
        Builds a token-efficient, dense string representation of the resume intelligence.
        Strips away raw text, metadata, and empty arrays to save Gemini tokens.
        """
        context_parts = []
        
        ats_score = intelligence.get("ats_score", "N/A")
        context_parts.append(f"ATS Score: {ats_score}/100")
        
        summary = intelligence.get("semantic_profile_summary", "")
        if summary:
            context_parts.append(f"Summary: {summary}")
            
        skills = intelligence.get("skills", {})
        if skills:
            hard = ", ".join(skills.get("hard_skills", []))
            soft = ", ".join(skills.get("soft_skills", []))
            if hard: context_parts.append(f"Hard Skills: {hard}")
            if soft: context_parts.append(f"Soft Skills: {soft}")
            
        strengths = intelligence.get("strengths", [])
        if strengths:
            context_parts.append("Strengths: " + " | ".join(strengths))
            
        weaknesses = intelligence.get("weaknesses", [])
        if weaknesses:
            context_parts.append("Weaknesses: " + " | ".join(weaknesses))
            
        project_eval = intelligence.get("project_evaluation", "")
        if project_eval and project_eval != "Not provided":
            context_parts.append(f"Project Evaluation: {project_eval}")
            
        role_alignment = intelligence.get("role_alignment", [])
        if role_alignment:
            context_parts.append("Role Alignment: " + ", ".join(role_alignment))
            
        recommendations = intelligence.get("improvement_suggestions", [])
        if recommendations:
            context_parts.append("Recommendations: " + " | ".join(recommendations))
            
        return "\n".join(context_parts)

    @staticmethod
    async def get_context(file_hash: str) -> Optional[str]:
        """Fetch the analyzed resume intelligence from PostgreSQL and return an optimized context string."""
        try:
            async with AsyncSessionLocal() as db:
                stmt = select(ResumeAnalysis).where(ResumeAnalysis.file_hash == file_hash)
                result = await db.execute(stmt)
                record = result.scalar_one_or_none()
                if record and record.intelligence_result:
                    return ResumeContextService._build_optimized_context(record.intelligence_result)
        except Exception as e:
            logger.error(f"Error fetching resume context from DB for hash {file_hash}: {e}")
        return None
