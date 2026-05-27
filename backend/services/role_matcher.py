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

Return valid JSON only in this format:

{{
  "matches": [
    {{
      "role": "string",
      "score": 85,
      "matching_skills": ["string"],
      "missing_skills": ["string"],
      "reason": "string",
      "recommendations": ["string"]
    }}
  ]
}}

Generate exactly 6 role matches.
"""


def clean_json_response(raw_text: str) -> Dict[str, Any]:

    raw_json = raw_text.strip()

    if raw_json.startswith("```json"):
        raw_json = raw_json.replace("```json", "").replace("```", "").strip()

    elif raw_json.startswith("```"):
        raw_json = raw_json.replace("```", "").strip()

    match = re.search(r"\{.*\}", raw_json, re.DOTALL)

    if match:
        raw_json = match.group(0)

    logger.info(f"RAW ROLE MATCH RESPONSE: {raw_json[:500]}")

    return json.loads(raw_json)


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
            indent=2,
            default=str
        ),
        skills_list=", ".join(skills_list)
    )

    try:

        response = await asyncio.wait_for(
            client.chat.completions.create(
                model="llama-3.1-8b-instant",
                temperature=0.3,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI recruiter."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            ),
            timeout=90.0
        )

        raw_response = response.choices[0].message.content

        result = clean_json_response(raw_response)

        if (
            "matches" not in result
            or not isinstance(result["matches"], list)
        ):
            raise ValueError("Invalid response structure")

        result["matches"].sort(
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        return result

    except Exception as e:

        logger.error(f"Role matcher failed: {e}")

        return {
            "matches": []
        }