import logging
import re
from typing import Dict, Any, List, Set

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from services.skill_extractor import extract_skills

# Exact aliases
EXACT_ALIASES = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "cv": "computer vision",
    "js": "javascript",
    "ts": "typescript",
    "k8s": "kubernetes",
    "rest": "rest apis",
    "api": "rest apis",
    "apis": "rest apis",
    "react.js": "react",
    "node.js": "node",
    "vue.js": "vue",
    "postgres": "postgresql",
    "genai": "generative ai",
    "llm": "generative ai",
    "llms": "generative ai",
    "nlp": "natural language processing",
    "github": "git",
    "py": "python",
}

DISPLAY_NAMES = {
    "machine learning": "Machine Learning",
    "artificial intelligence": "Artificial Intelligence",
    "deep learning": "Deep Learning",
    "computer vision": "Computer Vision",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "kubernetes": "Kubernetes",
    "rest apis": "REST APIs",
    "react": "React.js",
    "node": "Node.js",
    "postgresql": "PostgreSQL",
    "generative ai": "Generative AI",
    "aws": "AWS",
    "docker": "Docker",
    "python": "Python",
    "fastapi": "FastAPI",
    "sql": "SQL",
}

def normalize_skill(skill: str) -> str:
    if not isinstance(skill, str):
        return ""

    s = skill.lower().strip()
    s = re.sub(r'[^\w\s\.\-]', '', s)

    return EXACT_ALIASES.get(s, s)

def get_display_name(skill: str) -> str:
    s = skill.lower().strip()
    return DISPLAY_NAMES.get(s, skill.title())

def extract_normalized_skills_from_text(text: str) -> Set[str]:
    skills_dict = extract_skills(text)

    skills = set(
        skill
        for category in skills_dict.values()
        for skill in category
    )

    text_lower = text.lower()

    for alias, normalized in EXACT_ALIASES.items():
        if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
            skills.add(normalized)

    return set(normalize_skill(s) for s in skills if s)

def get_flattened_resume_skills(resume_intelligence: Dict) -> List[str]:
    """
    Safely and recursively extracts all string items from nested lists and dicts
    within the resume intelligence JSON to build a flattened list of skills.
    """
    if not resume_intelligence:
        return []

    flattened = set()

    def safe_extract(node):
        if isinstance(node, dict):
            for val in node.values():
                safe_extract(val)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, str):
                    flattened.add(item)
                elif isinstance(item, (dict, list)):
                    safe_extract(item)

    # Optionally target just the skills dict if strictness is needed,
    # but full traversal handles unstructured or fallback schemas safely.
    safe_extract(resume_intelligence)

    return list(flattened)

def calculate_semantic_score(resume_text: str, jd_text: str) -> float:
    try:
        vectorizer = TfidfVectorizer(stop_words="english")

        vectors = vectorizer.fit_transform([
            resume_text,
            jd_text
        ])

        score = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return float(score) * 100

    except Exception as e:
        logging.error(f"Semantic score error: {e}")
        return 0.0

def match_resume_to_jd(
    resume_text: str,
    job_description: str,
    resume_intelligence: Dict = None,
    file_hash: str = None
) -> Dict[str, Any]:

    if not resume_text or not job_description:
        return {
            "status": "error",
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "recommendations": [
                "Resume text and JD required."
            ]
        }

    logging.info(f"Matching started for {file_hash}")

    # Resume skills
    if resume_intelligence:
        raw_skills = get_flattened_resume_skills(
            resume_intelligence
        )

        resume_skills = set(
            normalize_skill(s)
            for s in raw_skills if s
        )

    else:
        resume_skills = extract_normalized_skills_from_text(
            resume_text
        )

    # JD skills
    jd_skills = extract_normalized_skills_from_text(
        job_description
    )

    matching = resume_skills.intersection(jd_skills)

    missing = jd_skills.difference(resume_skills)

    # Skill overlap score
    total_skills = len(matching) + len(missing)

    if total_skills > 0:
        skill_score = (
            len(matching) / total_skills
        ) * 100
    else:
        skill_score = 0

    # Lightweight semantic score
    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    # Final score
    final_score = (
        (skill_score * 0.7) +
        (semantic_score * 0.3)
    )

    final_score = int(round(final_score))

    ui_matching = [
        get_display_name(s)
        for s in matching
    ]

    ui_missing = [
        get_display_name(s)
        for s in missing
    ]

    recommendations = []

    if ui_missing:
        recommendations.append(
            f"Add missing skills like {', '.join(ui_missing[:3])}."
        )

    if final_score < 60:
        recommendations.append(
            "Improve resume wording to better align with JD."
        )

    if ui_matching:
        recommendations.append(
            "Highlight matching skills clearly in projects and experience."
        )

    return {
        "status": "success",
        "match_score": final_score,
        "matching_skills": sorted(ui_matching),
        "missing_skills": sorted(ui_missing),
        "recommendations": recommendations[:4]
    }