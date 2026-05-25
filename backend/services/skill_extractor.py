import re
import spacy
from typing import Dict, List

# Try loading spaCy model. It's useful for more advanced NLP processing (lemmatization, etc.)
# If it fails, we fall back to simple keyword matching using Regex.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import logging
    logging.warning("Spacy model 'en_core_web_sm' not found. We will use simple regex matching.")
    nlp = None

# Define skill categories with properly cased names for display
SKILL_CATEGORIES = {
    "languages": ["Python", "Java", "C", "C++", "JavaScript", "TypeScript", "Go", "SQL"],
    "frameworks": ["React", "Next.js", "FastAPI", "Flask", "Django", "Spring Boot", "TensorFlow", "PyTorch", "OpenCV", "Scikit-learn", "Pandas", "NumPy"],
    "cloud_devops": ["AWS", "Docker", "Kubernetes", "Azure", "GCP", "Jenkins", "GitHub Actions"],
    "databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
    "ai_ml": ["Machine Learning", "Deep Learning", "NLP", "LLMs", "YOLO", "HuggingFace", "Generative AI", "Computer Vision"],
    "tools_platforms": ["Git", "GitHub", "Linux", "VS Code", "Jupyter", "Kaggle", "Ollama"]
}

def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extracts technical skills from text and categorizes them.
    Uses basic keyword matching with robust word boundaries to prevent false positives.
    Ensures duplicate removal and case-insensitive matching.
    """
    extracted_skills = {
        "languages": set(),
        "frameworks": set(),
        "cloud_devops": set(),
        "databases": set(),
        "ai_ml": set(),
        "tools_platforms": set()
    }

    if not text:
        # Return empty lists if there is no text
        return {k: list(v) for k, v in extracted_skills.items()}

    # Normalize text to lowercase for case-insensitive matching
    text_lower = text.lower()

    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            skill_lower = skill.lower()
            
            # Escape the skill for regex to correctly handle symbols like C++, Next.js, etc.
            skill_pattern = re.escape(skill_lower)
            
            # Construct a regex pattern with custom word boundaries.
            # \b can struggle with special characters at the edges (like C++ or .js).
            # (?<![a-z]) ensures no letter precedes the skill.
            # (?![a-z]) ensures no letter follows the skill.
            pattern = r'(?<![a-z])' + skill_pattern + r'(?![a-z])'
            
            if re.search(pattern, text_lower):
                # Add the correctly formatted original skill name
                extracted_skills[category].add(skill)

    # Convert sets to sorted lists for consistent and clean API response formatting
    return {k: sorted(list(v)) for k, v in extracted_skills.items()}
