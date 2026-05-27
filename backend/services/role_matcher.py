import json
import os
import asyncio
import re

from groq import AsyncGroq
from typing import Dict, Any, List
from pydantic import BaseModel, ValidationError

from utils.logger import logger
from services.jd_matcher import get_flattened_resume_skills


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = AsyncGroq(api_key=GROQ_API_KEY)


class RoleMatchItem(BaseModel):
    role: str
    score: int
    matching_skills: List[str]
    missing_skills: List[str]
    reason: str
    recommendations: List[str]

class RoleMatchResponseSchema(BaseModel):
    matches: List[RoleMatchItem]


ROLE_MATCH_PROMPT = """
You are an expert career advisor and technical recruiter with extremely strict standards.

Analyze the following resume intelligence data and generate the best-fit job roles for this candidate.
Do NOT inflate scores. Do not default to 85. Use the following strict rubric:
- 90-100: Perfect fit. Candidate has all required skills and years of exact domain experience.
- 70-89: Strong fit. Candidate matches core skills but lacks some niche requirements.
- 50-69: Stretch role / Partial fit. Missing several core skills or lacking experience level.
- 20-49: Weak fit. Barely qualifies, missing majority of essential skills.

Generate a realistic, varied mix of roles: include 2 strong fits, 2 stretch roles, and 2 weak fits to give the candidate perspective.
Compare the extracted skills against the actual industry requirements for each role.

FORMATTING RULES (CRITICAL):
- DO NOT use markdown bold syntax like **Heading** or __Heading__.
- Headings should always be plain clean text.
- Bullet points using `-` or `*` are acceptable.
- Keep responses minimal, professional, UI-friendly, and clean plain-text style.
- Avoid excessive markdown formatting.

Resume Intelligence:
{resume_json}

Extracted Skills:
{skills_list}

CRITICAL: You must output ONLY a valid JSON object. Do not include markdown code blocks (e.g. ```json). Do not add any conversational text.

The JSON object MUST strictly adhere to this exact schema:
{{
  "matches": [
    {{
      "role": "Job Title (string)",
      "score": <integer between 20 and 95, based strictly on the rubric>,
      "matching_skills": ["skill1", "skill2"],
      "missing_skills": ["core_skill_missing1", "niche_skill_missing2"],
      "reason": "Detailed string explaining exactly why they fit or fall short",
      "recommendations": ["Actionable advice to bridge the gap"]
    }}
  ]
}}

Generate exactly 6 role matches in the array.
"""


def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Robust JSON extractor that finds the JSON block even if conversational text is present."""
    raw_json = raw_text.strip()
    
    # Locate the outer-most JSON object brackets
    start_idx = raw_json.find('{')
    end_idx = raw_json.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
        raw_json = raw_json[start_idx:end_idx+1]
        
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed. Raw response snippet: {raw_text[:200]}...")
        raise ValueError(f"Failed to parse LLM JSON output: {e}")


def _get_static_fallback_roles(skills_list: List[str]) -> Dict[str, Any]:
    """Provides a safe static fallback if the AI completely fails."""
    return {
        "matches": [
            {
                "role": "General Software Professional",
                "score": 50,  # Lowered to 50 to reflect neutral/uncertain fit, avoiding fake high scores
                "matching_skills": skills_list[:5] if skills_list else ["General Tech"],
                "missing_skills": ["Advanced Domain Specific Skills", "Specialized Frameworks"],
                "reason": "Based on a general profile match. High-precision AI matching was temporarily unavailable.",
                "recommendations": ["Ensure your resume contains highly specific keywords", "Tailor your resume precisely to the Job Description"]
            }
        ]
    }


async def generate_role_matches(
    intelligence_result: Dict[str, Any]
) -> Dict[str, Any]:

    logger.info("Role matcher started")

    try:
        skills_list = get_flattened_resume_skills(intelligence_result)

        resume_summary = {
            "ats_score": intelligence_result.get("ats_score"),
            "experience_level": intelligence_result.get("experience_level"),
            "strengths": intelligence_result.get("strengths", []),
            "weaknesses": intelligence_result.get("weaknesses", []),
            "projects": intelligence_result.get("projects", []),
            "summary": intelligence_result.get("summary", ""),
            "semantic_summary": intelligence_result.get("semantic_summary", ""),
        }
        
        # Serialize and check size to avoid Groq Context Window blowouts
        resume_json_str = json.dumps(resume_summary, default=str)
        if len(resume_json_str) > 6000:
            logger.warning(f"Resume JSON abnormally large ({len(resume_json_str)} chars). Truncating.")
            resume_json_str = resume_json_str[:6000] + "... [TRUNCATED]"

        prompt = ROLE_MATCH_PROMPT.format(
            resume_json=resume_json_str,
            skills_list=", ".join(skills_list)
        )

        max_retries = 2
        for attempt in range(max_retries + 1):
            raw_response = ""
            try:
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        temperature=0.0,  # Set to 0.0 for absolute deterministic JSON structure
                        response_format={"type": "json_object"},
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a rigid AI system. You output valid JSON ONLY."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    ),
                    timeout=30.0
                )

                raw_response = response.choices[0].message.content
                result = clean_json_response(raw_response)
                
                # Strict Pydantic Validation
                validated_data = RoleMatchResponseSchema.model_validate(result)
                final_dict = validated_data.model_dump()

                if not final_dict["matches"]:
                    raise ValueError("AI returned an empty matches list")

                # Post-processing Calibration: Penalize scores dynamically based on missing vs matching skills
                for match in final_dict["matches"]:
                    num_matching = len(match.get("matching_skills", []))
                    num_missing = len(match.get("missing_skills", []))
                    total_skills = num_matching + num_missing
                    
                    if total_skills > 0:
                        missing_ratio = num_missing / total_skills
                        # Hard penalty: if a role is missing 50% of the skills, it loses up to 35 points natively
                        penalty = int(missing_ratio * 35)
                        match["score"] = max(10, match["score"] - penalty)
                        
                    # Cap to a realistic maximum to avoid artificial 100s unless perfectly tailored
                    match["score"] = min(98, match["score"])

                # Sort matches by the newly calibrated scores
                final_dict["matches"].sort(
                    key=lambda x: x.get("score", 0),
                    reverse=True
                )

                logger.info("Role matcher succeeded with calibrated scores")
                return final_dict

            except ValidationError as ve:
                logger.warning(f"Role matcher schema validation failed on attempt {attempt + 1}: {ve}")
            except ValueError as ve:
                logger.warning(f"Role matcher parsing failed on attempt {attempt + 1}: {ve}")
            except Exception as e:
                logger.warning(f"Role matcher Groq API failed on attempt {attempt + 1}: {e}")
                
            if attempt == max_retries:
                logger.error(f"Role matcher exhausted all retries. Raw failing output: {raw_response[:500]}")
                return _get_static_fallback_roles(skills_list)

    except Exception as e:
        logger.error(f"Critical error in role matcher before LLM call: {e}", exc_info=True)
        return _get_static_fallback_roles([])