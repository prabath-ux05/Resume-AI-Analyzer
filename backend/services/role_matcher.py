import json
import os
import asyncio
import re

from groq import AsyncGroq
from typing import Dict, Any, List

from utils.logger import logger
from services.jd_matcher import get_flattened_resume_skills


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = AsyncGroq(api_key=GROQ_API_KEY)


ROLE_MATCH_PROMPT = """
You are an expert career advisor and recruiter.

Analyze the following resume intelligence data and generate the best-fit job roles for this candidate.

Resume Intelligence:
{resume_json}

Extracted Skills:
{skills_list}

You must output ONLY valid JSON in the exact following format. Do not include markdown formatting like ```json, do not include any conversational text, just the raw JSON object.

{{
  "matches": [
    {{
      "role": "Job Title (string)",
      "score": 85,
      "matching_skills": ["skill1", "skill2"],
      "missing_skills": ["skill3"],
      "reason": "Detailed string explaining the fit",
      "recommendations": ["Actionable advice 1", "Actionable advice 2"]
    }}
  ]
}}

Generate exactly 6 role matches.
"""


def clean_json_response(raw_text: str) -> Dict[str, Any]:

    raw_json = raw_text.strip()

    if raw_json.startswith("```json"):
        raw_json = raw_json.replace("```json", "", 1)
        if raw_json.endswith("```"):
            raw_json = raw_json[:-3]
    elif raw_json.startswith("```"):
        raw_json = raw_json.replace("```", "", 1)
        if raw_json.endswith("```"):
            raw_json = raw_json[:-3]
            
    raw_json = raw_json.strip()

    match = re.search(r"\{.*\}", raw_json, re.DOTALL)

    if match:
        raw_json = match.group(0)

    logger.debug(f"RAW ROLE MATCH RESPONSE: {raw_json[:500]}")

    return json.loads(raw_json)


def _get_static_fallback_roles(skills_list: List[str]) -> Dict[str, Any]:
    """Provides a safe static fallback if the AI completely fails, avoiding 20/100 UI bugs."""
    return {
        "matches": [
            {
                "role": "General Software Professional",
                "score": 75,
                "matching_skills": skills_list[:5] if skills_list else ["General Tech"],
                "missing_skills": ["Advanced Domain Specific Skills"],
                "reason": "Based on a general profile match. High-precision AI matching was temporarily unavailable.",
                "recommendations": ["Ensure your resume contains highly specific keywords", "Tailor your resume precisely to the Job Description"]
            }
        ]
    }


async def generate_role_matches(
    intelligence_result: Dict[str, Any]
) -> Dict[str, Any]:

    logger.info("Role matcher started")

    skills_list = get_flattened_resume_skills(
        intelligence_result
    )

    resume_summary = {
        "ats_score": intelligence_result.get("ats_score"),
        "experience_level": intelligence_result.get("experience_level"),
        "strengths": intelligence_result.get("strengths", []),
        "weaknesses": intelligence_result.get("weaknesses", []),
        "projects": intelligence_result.get("projects", []),
        "summary": intelligence_result.get("summary", ""),
        "semantic_summary": intelligence_result.get(
            "semantic_summary",
            ""
        ),
    }

    prompt = ROLE_MATCH_PROMPT.format(
        resume_json=json.dumps(
            resume_summary,
            default=str
        ),
        skills_list=", ".join(skills_list)
    )

    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    temperature=0.1,  # Lower temperature for strict JSON
                    response_format={"type": "json_object"},
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert AI recruiter. You ONLY output valid JSON. No conversational text."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                ),
                timeout=45.0
            )

            raw_response = response.choices[0].message.content
            result = clean_json_response(raw_response)

            if (
                "matches" not in result
                or not isinstance(result["matches"], list)
            ):
                raise ValueError("Invalid response structure: 'matches' key missing")

            if not result["matches"]:
                raise ValueError("AI returned an empty matches list")

            result["matches"].sort(
                key=lambda x: x.get("score", 0),
                reverse=True
            )

            logger.info("Role matcher succeeded")
            return result

        except Exception as e:
            logger.warning(f"Role matcher attempt {attempt + 1} failed: {e}")
            if attempt == max_retries:
                logger.error("Role matcher exhausted all retries. Falling back to static data.")
                return _get_static_fallback_roles(skills_list)