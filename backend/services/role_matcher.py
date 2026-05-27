import json
import os
import asyncio
import google.generativeai as genai
from typing import Dict, Any, List
from utils.logger import logger
from services.jd_matcher import get_flattened_resume_skills

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

ROLE_MATCH_PROMPT = """You are an expert career advisor and recruiter. Analyze the following resume intelligence data and generate the best-fit job roles for this candidate.

## Resume Intelligence:
{resume_json}

## Extracted Skills:
{skills_list}

## Instructions:
Based on the candidate's skills, projects, experience level, strengths, and weaknesses, evaluate their fit for 6 different job roles. You should select roles that represent a range of matches (e.g., strong fit, moderate fit, stretch goal). 
Consider roles such as AI/ML Engineer, Full Stack Developer, Backend Developer, Data Scientist, Cloud Engineer, Frontend Developer, or other relevant titles.

For each role, you MUST use a hybrid scoring system. Evaluate the candidate out of 100 on the following criteria:
- Skill Overlap (How well do their extracted skills match the role requirements?)
- Project Relevance (Are their projects relevant to this domain?)
- Experience Relevance (Does their work history align with the role?)
- Domain Fit (Does their overall profile and semantic summary fit the industry domain?)
- Resume Strengths (Do their identified strengths support this role?)

Then, deduct points for critical Missing Skills.
Calculate the final overall `score` as a weighted average of these factors. The score must strictly reflect the resume's contents. Different resumes must produce distinctly different role rankings and scores. Be brutally honest. A score of 90+ means near-perfect fit. 50-70 means partial fit with gaps.

Return exactly 6 roles, ranked by match score (highest first).

For each role provide:
1. "role": A specific, realistic job title
2. "score": The final calculated integer score (0-100)
3. "matching_skills": List of skills from the candidate's resume that directly match this role's requirements
4. "missing_skills": List of important skills for this role that the candidate is missing
5. "reason": A 1-2 sentence explanation of why they match (or don't) for this role, explicitly referencing the semantic AI reasoning and hybrid scoring factors.
6. "recommendations": 2-3 specific, actionable tips to improve their fit for this role

Return valid JSON in this exact format:
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


def _generate_fallback_matches(skills_list: List[str], summary_text: str) -> Dict[str, Any]:
    """
    Fallback method to generate role matches locally if the AI service fails.
    Uses simple keyword matching and heuristics.
    """
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
            # Check if skill in flattened skills or mentioned in summary
            if any(ts in sl for sl in skills_lower) or ts in summary_lower:
                # Add proper capitalization back
                matching.append(ts.title() if len(ts) > 3 else ts.upper())
            else:
                missing.append(ts.title() if len(ts) > 3 else ts.upper())
                
        # Calculate a base score
        total = len(target_skills)
        match_count = len(matching)
        score = int((match_count / max(total, 1)) * 100)
        
        # Add slight randomness so scores aren't identical flat numbers if tied
        score = max(20, min(95, score))
        
        # Generate generic reasoning
        reason = f"Based on your profile, you have a {score}% overlap with core requirements for {role_name}."
        if score > 70:
            reason = f"Strong fit for {role_name} based on your technical stack."
            
        matches.append({
            "role": role_name,
            "score": score,
            "matching_skills": matching[:5],
            "missing_skills": missing[:5],
            "reason": reason,
            "recommendations": [f"Gain experience in {m}" for m in missing[:2]] if missing else ["Continue building advanced projects in this stack."]
        })
        
    matches.sort(key=lambda x: x["score"], reverse=True)
    return {"matches": matches}


async def generate_role_matches(intelligence_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Uses Gemini AI to generate best-fit role matches from stored resume intelligence.
    No mock data — fully dynamic based on resume content.
    """
    import time
    start_time = time.time()
    logger.info("Role Matcher - Backend endpoint hit: AI role match requested")
    
    # Initialize defaults in case setup fails
    skills_list = []
    summary_text = ""

    try:
        # Extract skills for the prompt
        skills_list = get_flattened_resume_skills(intelligence_result)
        logger.info(f"Role Matcher - Extracted {len(skills_list)} skills for matching")

        # Build a focused subset of the intelligence for the prompt
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

        if not GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is not configured. Falling back to local matching.")
            return _generate_fallback_matches(skills_list, summary_text)

        logger.info("Role Matcher - Resume analysis loaded successfully from database")

        prompt = ROLE_MATCH_PROMPT.format(
            resume_json=json.dumps(resume_summary, indent=2, default=str),
            skills_list=", ".join(skills_list) if skills_list else "No skills extracted"
        )

        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            response_mime_type="application/json"
        )

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=generation_config
        )

        logger.info("Role Matcher - Gemini request started")

        response = await asyncio.wait_for(
            model.generate_content_async(prompt),
            timeout=90.0
        )
        
        latency = time.time() - start_time
        logger.info(f"Role Matcher - Gemini request completed successfully in {latency:.2f}s")

        raw_json = response.text
        result = json.loads(raw_json)

        # Validate structure
        if "matches" not in result or not isinstance(result["matches"], list):
            logger.info("Role Matcher - Fallback used: Invalid AI structure returned")
            return _generate_fallback_matches(skills_list, summary_text)

        # Ensure scores are clamped and sorted
        for match in result["matches"]:
            match["score"] = max(0, min(100, int(match.get("score", 0))))

        result["matches"].sort(key=lambda x: x["score"], reverse=True)

        logger.info(f"Role Matcher - Generated {len(result['matches'])} role matches. Total latency: {latency:.2f}s")
        return result

    except json.JSONDecodeError as e:
        latency = time.time() - start_time
        logger.error(f"Role Matcher - Gemini request failed with JSON parse error after {latency:.2f}s: {e}")
        logger.info("Role Matcher - Fallback used: JSON parsing failed")
        return _generate_fallback_matches(skills_list, summary_text)
    except asyncio.TimeoutError:
        latency = time.time() - start_time
        logger.error(f"Role Matcher - Gemini request failed (timed out) after {latency:.2f}s")
        logger.info("Role Matcher - Fallback used: Request timed out")
        return _generate_fallback_matches(skills_list, summary_text)
    except Exception as e:
        latency = time.time() - start_time
        logger.error(f"Role Matcher - Gemini request failed with unexpected error after {latency:.2f}s: {e}")
        logger.info("Role Matcher - Fallback used: Unexpected error")
        return _generate_fallback_matches(skills_list, summary_text)
