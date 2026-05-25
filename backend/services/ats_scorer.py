import re
from typing import Dict, Any, List, Tuple
from services.skill_extractor import extract_skills

def calculate_structure_score(text_lower: str) -> int:
    """Scores based on the presence of standard sections (Max 15)"""
    score = 0
    sections = {
        "Summary": ["summary", "objective", "profile", "about me"],
        "Skills": ["skills", "technologies", "core competencies", "technical skills"],
        "Experience": ["experience", "employment", "work history", "professional experience"],
        "Education": ["education", "academic", "degree"],
        "Projects": ["projects", "personal projects", "academic projects"]
    }
    for keywords in sections.values():
        if any(re.search(r'\b' + kw + r'\b', text_lower) for kw in keywords):
            score += 3
    return min(score, 15)

def calculate_technical_depth_score(skills_data: Dict[str, List[str]], text_lower: str) -> int:
    """Scores based on depth of technologies (Max 20)"""
    score = 0
    total_skills = sum(len(skills) for skills in skills_data.values())
    
    # Base points for volume
    if total_skills >= 12:
        score += 10
    elif total_skills >= 6:
        score += 5
        
    # Bonus for complex categories
    if len(skills_data.get("cloud_devops", [])) >= 2:
        score += 3
    if len(skills_data.get("ai_ml", [])) >= 2:
        score += 4
    if len(skills_data.get("databases", [])) >= 1:
        score += 3
        
    # Check for deployment mentions
    deployment_terms = ["deployed", "production", "ci/cd", "pipeline", "scaled", "infrastructure"]
    if sum(1 for term in deployment_terms if term in text_lower) >= 2:
        score += 5
        
    return min(score, 20)

def calculate_project_quality_score(text_lower: str) -> int:
    """Scores based on action verbs (Max 20)"""
    score = 10  # Base score
    
    strong_verbs = ["engineered", "optimized", "developed", "architected", "implemented", "deployed", "designed", "spearheaded", "orchestrated"]
    weak_verbs = ["worked on", "helped with", "familiar with", "assisted", "responsible for"]
    
    strong_count = sum(1 for verb in strong_verbs if re.search(r'\b' + verb + r'\b', text_lower))
    weak_count = sum(1 for verb in weak_verbs if re.search(r'\b' + verb + r'\b', text_lower))
    
    score += (strong_count * 2)
    score -= (weak_count * 2)
    
    return max(0, min(score, 20))

def calculate_quantified_impact_score(text_lower: str) -> int:
    """Scores based on measurable outcomes (Max 15)"""
    score = 0
    
    # Detect percentages, metrics, monetary values
    percent_matches = len(re.findall(r'\d+%', text_lower))
    score += (percent_matches * 3)
    
    measurable_terms = ["latency", "accuracy", "real-time", "scalability", "reduced", "increased", "faster", "millisecond"]
    measure_count = sum(1 for term in measurable_terms if term in text_lower)
    score += (measure_count * 2)
    
    return min(score, 15)

def calculate_role_relevance_score(skills_data: Dict[str, List[str]]) -> int:
    """Scores based on overall tech alignment (Max 20)"""
    score = 0
    
    # Assess if it's a solid AI/Backend/Cloud profile
    has_backend = len(skills_data.get("languages", [])) > 0 and len(skills_data.get("frameworks", [])) > 0
    has_data = len(skills_data.get("databases", [])) > 0
    has_advanced = len(skills_data.get("ai_ml", [])) > 0 or len(skills_data.get("cloud_devops", [])) > 0
    
    if has_backend:
        score += 8
    if has_data:
        score += 6
    if has_advanced:
        score += 6
        
    return min(score, 20)

def calculate_readability_score(text: str) -> int:
    """Scores based on length and formatting (Max 10)"""
    score = 10
    word_count = len(text.split())
    
    if word_count < 200:
        score -= 5
    elif word_count > 1000:
        score -= 3
        
    special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s.,\-()|/]', text)) / max(len(text), 1)
    if special_char_ratio > 0.05:
        score -= 4
        
    return max(0, min(score, 10))

def generate_insights(text_lower: str, skills_data: Dict[str, List[str]], scores: Dict[str, int]) -> Tuple[List[str], List[str], List[str], List[str]]:
    """Generates dynamic NLP feedback based on resume content."""
    impact = []
    impression = []
    optimization = []
    risk = []
    
    # --- Impact Analysis ---
    if scores["quantified_impact"] >= 10:
        impact.append("Projects demonstrate strong measurable outcomes and engineering impact.")
    if len(skills_data.get("ai_ml", [])) >= 2:
        impact.append("Technical stack aligns well with modern ML engineering roles.")
    elif len(skills_data.get("cloud_devops", [])) >= 2:
        impact.append("Resume showcases practical deployment-oriented and cloud experience.")
    elif len(skills_data.get("frameworks", [])) >= 3:
        impact.append("Strong demonstration of application development and framework usage.")
        
    if "api" in text_lower or "rest" in text_lower or "graphql" in text_lower:
        impact.append("Clear experience with backend API architecture and integration.")

    # --- Recruiter Impression ---
    if scores["project_quality"] >= 15:
        impression.append("Project descriptions appear implementation-focused and production-aware.")
    if sum(scores.values()) >= 80:
        impression.append("Resume creates a strong technical first impression.")
    elif sum(scores.values()) >= 60:
        impression.append("Solid technical foundation, but lacks deep specialization signals.")
    else:
        impression.append("Resume appears junior or lacks specific technical depth.")
        
    if len(skills_data.get("ai_ml", [])) > 0 or len(skills_data.get("languages", [])) >= 3:
        impression.append("Technical breadth is suitable for competitive engineering opportunities.")

    # --- Content Optimization ---
    if scores["quantified_impact"] < 8:
        optimization.append("Add quantified metrics (e.g., %, latency) to strengthen project impact.")
    if scores["project_quality"] < 12:
        optimization.append("Replace weak verbs ('worked on') with strong action verbs ('engineered', 'optimized').")
    if len(skills_data.get("cloud_devops", [])) == 0:
        optimization.append("Highlight cloud technologies or deployment experience more prominently.")
    if scores["ats_readability"] < 8:
        optimization.append("Improve text formatting or adjust length for better readability.")

    # --- ATS Risk Indicators ---
    if len(skills_data.get("cloud_devops", [])) == 0:
        risk.append("Limited cloud/devops technologies detected.")
    if scores["quantified_impact"] < 5:
        risk.append("Few measurable outcomes identified in project descriptions.")
    if scores["resume_structure"] < 12:
        risk.append("Missing standard resume sections (e.g., Summary, Projects).")
    if len(text_lower.split()) < 200:
        risk.append("Resume is unusually short, which may bypass keyword filters.")

    return impact, impression, optimization, risk

def determine_confidence(total_score: int) -> str:
    """Calculates recruiter confidence."""
    if total_score >= 80:
        return "High"
    elif total_score >= 60:
        return "Medium"
    else:
        return "Low"

def score_resume(text: str) -> Dict[str, Any]:
    """
    Main orchestrator function for ATS scoring using the new advanced AI Recruiter Engine logic.
    """
    if not text:
        return {
            "status": "error",
            "ats_score": 0,
            "score_breakdown": {},
            "recruiter_confidence": "Low",
            "resume_impact_analysis": [],
            "recruiter_impression": [],
            "content_optimization_suggestions": ["Upload a valid resume with readable text."],
            "ats_risk_indicators": [],
            "company_matches": []
        }
        
    text_lower = text.lower()
    extracted_skills = extract_skills(text)
    
    # Calculate Scores
    scores = {
        "resume_structure": calculate_structure_score(text_lower),
        "technical_depth": calculate_technical_depth_score(extracted_skills, text_lower),
        "project_quality": calculate_project_quality_score(text_lower),
        "quantified_impact": calculate_quantified_impact_score(text_lower),
        "role_relevance": calculate_role_relevance_score(extracted_skills),
        "ats_readability": calculate_readability_score(text)
    }
    
    total_score = sum(scores.values())
    confidence = determine_confidence(total_score)
    
    # Generate Insights
    impact, impression, optimization, risk = generate_insights(text_lower, extracted_skills, scores)
    
    # Import locally to avoid circular dependencies if any
    from services.company_matcher import generate_company_matches
    company_matches = generate_company_matches(extracted_skills, total_score)
    
    return {
        "status": "success",
        "ats_score": total_score,
        "score_breakdown": scores,
        "recruiter_confidence": confidence,
        "resume_impact_analysis": impact,
        "recruiter_impression": impression,
        "content_optimization_suggestions": optimization,
        "ats_risk_indicators": risk,
        "company_matches": company_matches
    }
