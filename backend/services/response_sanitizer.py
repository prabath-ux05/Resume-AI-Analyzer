import json
import re
from typing import Dict, Any
from utils.logger import logger

class ResponseSanitizer:
    """
    Sanitizes raw AI JSON outputs before they hit Pydantic validation.
    Handles malformed markdown and missing keys.
    """

    @staticmethod
    def sanitize(raw_text: str) -> str:
        """
        Cleans the raw response string and ensures all required lists exist.
        Returns a valid JSON string.
        """
        # 1. Clean Markdown JSON blocks if the model ignored instructions
        clean_text = raw_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        
        clean_text = clean_text.strip()

        # 2. Try parsing
        try:
            data = json.loads(clean_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI JSON: {clean_text[:100]}...")
            raise e
            
        # 3. Inject safe defaults for top-level arrays/strings if missing
        list_keys = ["strengths", "weaknesses", "missing_keywords", "role_alignment", "improvement_suggestions"]
        for key in list_keys:
            if key not in data or data[key] is None:
                data[key] = []
                
        if "semantic_profile_summary" not in data or not data["semantic_profile_summary"]:
            data["semantic_profile_summary"] = "Profile summary not provided."
            
        if "project_evaluation" not in data or not data["project_evaluation"]:
            data["project_evaluation"] = "Project evaluation not provided."
            
        if "ats_score" not in data or data["ats_score"] is None:
            data["ats_score"] = 0
            
        # 4. Inject safe defaults for nested skills
        if "skills" not in data or not isinstance(data["skills"], dict):
            data["skills"] = {}
            
        skill_keys = ["hard_skills", "soft_skills", "tools", "frameworks"]
        for sk in skill_keys:
            if sk not in data["skills"] or data["skills"][sk] is None:
                data["skills"][sk] = []
                
        logger.debug("Response sanitized successfully.")
        return json.dumps(data)
