import logging
import re
from typing import Dict, Any, List, Set
from services.skill_extractor import extract_skills

# Load the SentenceTransformer model for deep semantic similarity.
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    model = None
    logging.warning("SentenceTransformer or scikit-learn is not installed. Semantic matching will default to 0.")

# Exact aliases to handle common abbreviations and normalize them to canonical forms
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
    "tensorflow": "tensor flow",
    "pytorch": "py torch"
}

# Mapping canonical names back to display names for UI
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
    "vue": "Vue.js",
    "postgresql": "PostgreSQL",
    "generative ai": "Generative AI",
    "aws": "AWS",
    "gcp": "GCP",
    "docker": "Docker",
    "python": "Python",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "sql": "SQL",
    "natural language processing": "Natural Language Processing",
    "git": "Git",
    "tensor flow": "TensorFlow",
    "py torch": "PyTorch"
}

# Broad capabilities mapping to identify partial semantic matches and support synonyms
CAPABILITY_MAP = {
    "backend apis": ["fastapi", "flask", "django", "spring boot", "rest apis", "node"],
    "backend": ["fastapi", "flask", "django", "spring boot", "rest apis", "go", "java", "node"],
    "frontend development": ["react", "next.js", "javascript", "typescript", "vue", "angular", "html", "css"],
    "frontend": ["react", "next.js", "javascript", "typescript", "vue", "angular", "html", "css"],
    "devops": ["aws", "docker", "kubernetes", "azure", "gcp", "jenkins", "ci/cd", "git"],
    "cloud deployment": ["aws", "docker", "kubernetes", "azure", "gcp"],
    "cloud": ["aws", "docker", "kubernetes", "azure", "gcp"],
    "database systems": ["mysql", "postgresql", "mongodb", "redis", "sql"],
    "database": ["mysql", "postgresql", "mongodb", "redis", "sql"],
    "ai applications": ["deep learning", "natural language processing", "tensor flow", "py torch", "machine learning", "generative ai"],
    "ai engineer": ["deep learning", "natural language processing", "tensor flow", "py torch", "machine learning", "generative ai"],
    "machine learning": ["scikit-learn", "pandas", "numpy", "tensor flow", "py torch"]
}

def normalize_skill(skill: str) -> str:
    """Normalizes a skill by lowercasing, stripping, removing punctuation, and mapping aliases."""
    if not isinstance(skill, str):
        return ""
    # Lowercase and trim
    s = skill.lower().strip()
    # Remove punctuation except dots and hyphens that might be part of the name
    s = re.sub(r'[^\w\s\.\-]', '', s)
    return EXACT_ALIASES.get(s, s)

def get_display_name(skill: str) -> str:
    """Returns the properly cased name for UI display."""
    s = skill.lower().strip()
    return DISPLAY_NAMES.get(s, skill.title())

def extract_normalized_skills_from_text(text: str) -> Set[str]:
    """Extracts explicit skills from raw text and normalizes them."""
    skills_dict = extract_skills(text)
    skills = set(skill for category in skills_dict.values() for skill in category)
    
    # Text-based alias expansion (since extract_skills might miss acronyms)
    text_lower = text.lower()
    for alias, normalized in EXACT_ALIASES.items():
        # Only match word boundaries
        if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
            skills.add(normalized)
            
    return set(normalize_skill(s) for s in skills if s)

def get_flattened_resume_skills(resume_intelligence: Dict) -> List[str]:
    """
    Extracts skills from all possible structures in the intelligence object
    and flattens them into one list.
    """
    if not resume_intelligence or not isinstance(resume_intelligence, dict):
        return []
        
    possible_keys = [
        "skills",
        "extracted_skills", 
        "skill_categories",
        "skills_intelligence",
        "categorized_skills",
        "technical_skills",
        "semantic_skill_categories"
    ]
    
    flattened_skills = set()
    
    for key in possible_keys:
        skills_obj = resume_intelligence.get(key)
        if skills_obj:
            if isinstance(skills_obj, dict):
                # Handle nested category objects
                for category, skills_list in skills_obj.items():
                    if isinstance(skills_list, list):
                        for s in skills_list:
                            if isinstance(s, str):
                                flattened_skills.add(s)
            elif isinstance(skills_obj, list):
                # Handle flat list
                for s in skills_obj:
                    if isinstance(s, str):
                        flattened_skills.add(s)
                    
    return list(flattened_skills)

def match_resume_to_jd(resume_text: str, job_description: str, resume_intelligence: Dict = None, file_hash: str = None) -> Dict[str, Any]:
    """
    Implements a hybrid matching system combining:
    1. Single Source of Truth AI skills from database (if provided)
    2. Normalized Keyword Overlap (Handling synonyms like ML -> Machine Learning)
    3. Partial Semantic Capability Matching (e.g., 'backend' -> 'FastAPI')
    4. SentenceTransformer embeddings for full-text semantic similarity
    """
    if not resume_text or not job_description:
        return {
            "status": "error", "match_score": 0, "matching_skills": [], "missing_skills": [],
            "recommendations": ["Both resume text and job description must be provided."]
        }
    
    logging.info(f"--- JOB MATCH START (Resume ID: {file_hash}) ---")
    
    if resume_intelligence:
        logging.info(f"Raw Resume Intelligence Object: found with keys {list(resume_intelligence.keys())}")
    else:
        logging.info("Raw Resume Intelligence Object: None")
    
    # --- 1. Flatten and Normalize Pre-Extracted Resume Skills ---
    if resume_intelligence:
        raw_flattened_skills = get_flattened_resume_skills(resume_intelligence)
        logging.info(f"Flattened Resume Skills (Raw): {raw_flattened_skills}")
        resume_skills_norm = set(normalize_skill(s) for s in raw_flattened_skills if s)
        logging.info(f"Normalized Resume Skills: {resume_skills_norm}")
    else:
        resume_skills_norm = extract_normalized_skills_from_text(resume_text)
        logging.info(f"Fell back to text extraction for resume.")
        logging.info(f"Normalized Resume Skills: {resume_skills_norm}")

    # --- 2. Extract & Normalize JD Skills ---
    jd_skills_norm = extract_normalized_skills_from_text(job_description)
    logging.info(f"Extracted/Normalized JD Skills: {jd_skills_norm}")

    # --- 3. Base Overlap ---
    matching_skills_norm = set(resume_skills_norm.intersection(jd_skills_norm))
    missing_skills_norm = set(jd_skills_norm.difference(resume_skills_norm))
    
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()

    # --- 4. Capability-based Partial Semantic Match ---
    for cap, specifics in CAPABILITY_MAP.items():
        cap_in_jd = re.search(r'\b' + re.escape(cap) + r'\b', jd_lower) or (cap in jd_skills_norm)
        cap_in_resume = re.search(r'\b' + re.escape(cap) + r'\b', resume_lower) or (cap in resume_skills_norm)
        
        if cap_in_jd:
            provided = [s for s in specifics if normalize_skill(s) in resume_skills_norm]
            if provided:
                matching_skills_norm.update([normalize_skill(p) for p in provided])
                matching_skills_norm.add(normalize_skill(cap))
                if normalize_skill(cap) in missing_skills_norm:
                    missing_skills_norm.remove(normalize_skill(cap))
            elif not cap_in_resume:
                missing_skills_norm.add(normalize_skill(cap))

        if cap_in_resume:
            for specific in specifics:
                norm_spec = normalize_skill(specific)
                if norm_spec in missing_skills_norm:
                    missing_skills_norm.remove(norm_spec)
                    matching_skills_norm.add(norm_spec)

    logging.info(f"Final Matching Skills (Norm): {matching_skills_norm}")
    logging.info(f"Final Missing Skills (Norm): {missing_skills_norm}")

    # --- 5. Full-Text Semantic Similarity Match (Transformer Embeddings) ---
    semantic_score_pct = 0.0
    if model is not None:
        try:
            embeddings = model.encode([resume_text, job_description])
            sim_matrix = cosine_similarity([embeddings[0]], [embeddings[1]])
            semantic_score = float(sim_matrix[0][0])
            clamped = max(0.3, min(0.75, semantic_score))
            semantic_score_pct = ((clamped - 0.3) / 0.45) * 100
        except Exception as e:
            logging.error(f"Error during semantic embedding: {str(e)}")

    # --- 6. Final Scoring Logic (Hybrid Combined) ---
    if len(jd_skills_norm) > 0 or len(missing_skills_norm) > 0:
        total_target_skills = len(matching_skills_norm) + len(missing_skills_norm)
        skill_score_pct = (len(matching_skills_norm) / max(1, total_target_skills)) * 100
    else:
        skill_score_pct = semantic_score_pct 

    final_score = (semantic_score_pct * 0.3) + (skill_score_pct * 0.7)
    
    if final_score > 0:
        final_score = (final_score / 100.0) ** 0.6 * 100.0
        
    final_score = int(round(final_score))
    
    logging.info(f"Final Match Score Calculation: Semantic ({semantic_score_pct:.1f}%) * 0.3 + Overlap ({skill_score_pct:.1f}%) * 0.7 (Curved) = {final_score}%")

    # --- 7. Generate Specific Actionable Recommendations ---
    recommendations = []
    
    ui_missing = [get_display_name(s) for s in missing_skills_norm]
    ui_matching = [get_display_name(s) for s in matching_skills_norm]
    
    if ui_missing:
        cloud_missing = [s for s in ui_missing if s.lower() in ["aws", "docker", "kubernetes", "azure", "gcp", "cloud", "devops"]]
        backend_missing = [s for s in ui_missing if s.lower() in ["fastapi", "flask", "django", "spring boot", "go", "backend", "backend api", "rest apis", "node.js"]]
        ai_missing = [s for s in ui_missing if s.lower() in ["deep learning", "nlp", "tensorflow", "pytorch", "llms", "machine learning", "ai engineer", "generative ai", "natural language processing", "tensor flow", "py torch"]]
        
        if cloud_missing:
            recommendations.append(f"Add Cloud/DevOps experience like {', '.join(cloud_missing[:2])} if you have used them.")
        if backend_missing:
            recommendations.append(f"Include backend APIs or frameworks like {', '.join(backend_missing[:2])}.")
        if ai_missing:
            recommendations.append(f"Emphasize AI/ML capabilities, specifically {', '.join(ai_missing[:2])}.")
            
        other_missing = list(set(ui_missing) - set(cloud_missing + backend_missing + ai_missing))
        if other_missing and len(recommendations) < 3:
            recommendations.append(f"Consider explicitly mentioning these missing skills: {', '.join(other_missing[:3])}.")
            
    if final_score < 60 and semantic_score_pct < 50:
        recommendations.append("The overall context of your resume doesn't align well with the JD. Rewrite your bullet points to match the JD's tone and terminology.")
    elif len(ui_matching) > 0:
        recommendations.append("Good baseline! Ensure your matching skills are explicitly demonstrated in your project descriptions with measurable outcomes.")

    return {
        "status": "success",
        "match_score": final_score,
        "matching_skills": sorted(ui_matching),
        "missing_skills": sorted(ui_missing),
        "recommendations": recommendations[:4]
    }
