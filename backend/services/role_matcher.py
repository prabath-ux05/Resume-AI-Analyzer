import json
import os
import asyncio
import re
import google.generativeai as genai
from typing import Dict, Any, List
from utils.logger import logger
from services.jd_matcher import get_flattened_resume_skills

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    genai.configure(api_key=GROQ_API_KEY)

ROLE_MATCH_PROMPT = """You are an expert career advisor and recruiter. Analyze the following resume intelligence data and generate the best-fit job roles for this candidate.

## Resume Intelligence:
{resume_json}

## Extracted Skills:
{skills_list}

## Instructions:
Based on the candidate's skills, projects, experience level, strengths, and weaknesses, evaluate their fit for 6 different job roles.

Return valid JSON only in this exact format:
{{
  "matches": [
    {{
      "role": "string",
      "score": integer,
      "matching_skills": ["string"],
      "missing_skills": ["string"],
      "reason": "string",
      "recommendations": ["string"]
    }}
  ]
}}
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


def _generate_fallback_matches(skills_list: List[str], summary_text: str) -> Dict[str, Any]:
    logger.info("Role Matcher - Using local fallback role matching")

    skills_lower = [s.lower() for s in skills_list]
    summary_lower = summary_text.lower()

    roles_def = {
        "AI/ML Engineer": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "nlp", "ai", "llms"],
        "Full Stack Developer": ["react", "node", "javascript", "typescript", "express", "mongodb", "postgresql", "html", "css", "next.js"],
        "Backend Developer": ["python", "java", "go", "node", "sql", "postgresql", "fastapi", "spring boot", "docker", "api"],
        "Frontend Developer": ["react", "vue", "javascript", "typescript", "html", "css", "tailwind", "ui", "ux"],
        "Data Scientist": ["python", "sql", "pandas", "numpy", "statistics", "machine learning", "data analysis", "r"],
        "Cloud Engineer": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "linux"]
    }

    matches = []

    for role_name, target_skills in roles_def.items():
        matching = []
        missing = []

        for ts in target_skills:
            if any(ts in sl for sl in skills_lower) or ts in summary_lower:
                matching.append(ts.title() if len(ts) > 3 else ts.upper())
            else:
                missing.append(ts.title() if len(ts) > 3 else ts.upper())

        score = int((len(matching) / max(len(target_skills), 1)) * 100)
        score = max(20, min(95, score))

        matches.append({
            "role": role_name,
            "score": score,
            "matching_skills": matching[:5],
            "missing_skills": missing[:5],
            "reason": f"Based on your profile, you have a {score}% overlap with core requirements for {role_name}.",
            "recommendations": [f"Gain experience in {m}" for m in missing[:2]] if missing else ["Continue building advanced projects in this stack."]
        })

    matches.sort(key=lambda x: x["score"], reverse=True)
    return {"matches": matches}


async def generate_role_matches(intelligence_result: Dict[str, Any]) -> Dict[str, Any]:
    import time

    start_time = time.time()
    logger.info("Role Matcher - Backend endpoint hit: AI role match requested")

    skills_list = []
    summary_text = ""

    try:
        skills_list = get_flattened_resume_skills(intelligence_result)
        logger.info(f"Role Matcher - Extracted {len(skills_list)} skills for matching")

        resume_summary = {
            "ats_score": intelligence_result.get("ats_score"),
            "experience_level": intelligence_result.get("experience_level"),
            "strengths": intelligence_result.get("strengths", []),
            "weaknesses": intelligence_result.get("weaknesses", []),
            "recommendations": intelligence_result.get("recommendations", []),
            "projects": intelligence_result.get("projects", []),
            "work_experience": intelligence_result.get("work_experience", []),
            "education": intelligence_result.get("education", []),
            "certifications": intelligence_result.get("certifications", []),
            "summary": intelligence_result.get("summary", ""),
            "semantic_summary": intelligence_result.get("semantic_summary", ""),
        }

        summary_text = str(resume_summary.get("semantic_summary", "")) + " " + str(resume_summary.get("summary", ""))

        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY is not configured. Falling back to local matching.")
            return _generate_fallback_matches(skills_list, summary_text)

        prompt = ROLE_MATCH_PROMPT.format(
            resume_json=json.dumps(resume_summary, indent=2, default=str),
            skills_list=", ".join(skills_list) if skills_list else "No skills extracted"
        )

        generation_config = genai.types.GenerationConfig(
            temperature=0.4,
            response_mime_type="application/json"
        )

        model = genai.GenerativeModel(
            model_name="llama-3.1-8b-instant",
            generation_config=generation_config
        )

        logger.info("Role Matcher - Groq request started")

        response = await asyncio.wait_for(
            model.generate_content_async(prompt),
            timeout=90.0
        )

        latency = time.time() - start_time
        logger.info(f"Role Matcher - Groq request completed successfully in {latency:.2f}s")

        result = clean_json_response(response.text)

        if "matches" not in result or not isinstance(result["matches"], list):
            logger.info("Role Matcher - Fallback used: Invalid AI structure returned")
            return _generate_fallback_matches(skills_list, summary_text)

        for match in result["matches"]:
            match["score"] = max(0, min(100, int(match.get("score", 0))))

        result["matches"].sort(key=lambda x: x["score"], reverse=True)

        logger.info(f"Role Matcher - Generated {len(result['matches'])} role matches.")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Role Matcher - JSON parse error: {e}")
        return _generate_fallback_matches(skills_list, summary_text)

    except asyncio.TimeoutError:
        logger.error("Role Matcher - Groq request timed out")
        return _generate_fallback_matches(skills_list, summary_text)

    except Exception as e:
        logger.error(f"Role Matcher - Groq request failed: {e}")
        return _generate_fallback_matches(skills_list, summary_text)