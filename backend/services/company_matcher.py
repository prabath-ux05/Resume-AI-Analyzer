from typing import Dict, List, Any

# Map categories to specific types of companies and roles
COMPANY_PROFILES = {
    "AI_ML": [
        {
            "company": "OpenAI",
            "recommended_roles": ["AI Engineer", "Research Scientist", "Machine Learning Engineer"],
            "reason": "Strong focus on generative AI, LLMs, and advanced deep learning."
        },
        {
            "company": "NVIDIA",
            "recommended_roles": ["Deep Learning Engineer", "Computer Vision Researcher"],
            "reason": "Excellent match for deep learning and high-performance computing skills."
        },
        {
            "company": "Hugging Face",
            "recommended_roles": ["NLP Engineer", "MLOps Engineer"],
            "reason": "Ideal for NLP capabilities and experience with transformer architectures."
        },
        {
            "company": "Google AI",
            "recommended_roles": ["Machine Learning Engineer", "AI Researcher"],
            "reason": "Broad AI capabilities match well with advanced machine learning expertise."
        },
        {
            "company": "Anthropic",
            "recommended_roles": ["AI Safety Researcher", "Machine Learning Engineer"],
            "reason": "Aligns with advanced AI/LLM experience."
        }
    ],
    "Full_Stack": [
        {
            "company": "Stripe",
            "recommended_roles": ["Backend Engineer", "Full Stack Engineer", "API Developer"],
            "reason": "Strong backend framework and database knowledge fits their API-first culture."
        },
        {
            "company": "Vercel",
            "recommended_roles": ["Frontend Engineer", "Developer Relations", "Full Stack Engineer"],
            "reason": "Matches well with modern frontend capabilities like React and Next.js."
        },
        {
            "company": "Shopify",
            "recommended_roles": ["Backend Engineer", "Infrastructure Engineer"],
            "reason": "Solid mix of backend and database skills suits their scale."
        },
        {
            "company": "Atlassian",
            "recommended_roles": ["Full Stack Developer", "Cloud Engineer"],
            "reason": "Good balance of cloud, backend, and collaborative tools."
        }
    ],
    "Cloud_DevOps": [
        {
            "company": "AWS",
            "recommended_roles": ["Cloud Architect", "DevOps Engineer", "Backend Engineer"],
            "reason": "Extensive cloud and infrastructure skills align with their core services."
        },
        {
            "company": "HashiCorp",
            "recommended_roles": ["Infrastructure Engineer", "DevOps Engineer"],
            "reason": "Strong Kubernetes, Docker, and automation skills detected."
        },
        {
            "company": "Datadog",
            "recommended_roles": ["SRE", "Backend Engineer"],
            "reason": "Systems-level understanding and cloud deployment expertise."
        }
    ],
    "Data_Engineering": [
        {
            "company": "Snowflake",
            "recommended_roles": ["Data Engineer", "Backend Engineer"],
            "reason": "Strong database and backend knowledge aligns with data warehousing."
        },
        {
            "company": "Databricks",
            "recommended_roles": ["Data Scientist", "MLOps Engineer", "Data Engineer"],
            "reason": "Mix of database, ML, and scalable data processing."
        }
    ]
}

def determine_primary_domains(skills_data: Dict[str, List[str]]) -> List[str]:
    """Determine the strongest technical domains based on extracted skills."""
    domains = []
    
    # Calculate counts
    ai_count = len(skills_data.get("ai_ml", []))
    backend_count = len(skills_data.get("languages", [])) + len(skills_data.get("frameworks", []))
    cloud_count = len(skills_data.get("cloud_devops", []))
    db_count = len(skills_data.get("databases", []))
    
    if ai_count >= 2:
        domains.append("AI_ML")
    if backend_count >= 4 and db_count >= 1:
        domains.append("Full_Stack")
    if cloud_count >= 2:
        domains.append("Cloud_DevOps")
    if db_count >= 2 and backend_count >= 2:
        domains.append("Data_Engineering")
        
    return domains

def generate_company_matches(skills_data: Dict[str, List[str]], ats_score: int) -> List[Dict[str, Any]]:
    """Generate realistic company matches based on skills and score."""
    domains = determine_primary_domains(skills_data)
    
    if not domains:
        # Default fallback for generic resumes
        return [
            {
                "company": "Tech Startups",
                "match_score": 75,
                "recommended_roles": ["Junior Developer", "Software Engineer"],
                "reason": "General programming skills are suitable for agile startup environments."
            }
        ]
        
    matches = []
    # Base match score derived from overall ATS score but customized
    base_match_score = min(98, max(60, ats_score + 5))
    
    for domain in domains:
        domain_companies = COMPANY_PROFILES.get(domain, [])
        for i, company_info in enumerate(domain_companies):
            if len(matches) >= 3:
                break
            
            # Vary the score slightly based on the company's position in the list
            match_score = base_match_score - (i * 2)
            
            matches.append({
                "company": company_info["company"],
                "match_score": match_score,
                "recommended_roles": company_info["recommended_roles"],
                "reason": company_info["reason"]
            })
            
    # Ensure uniqueness and return top 3
    seen = set()
    unique_matches = []
    for m in matches:
        if m["company"] not in seen:
            seen.add(m["company"])
            unique_matches.append(m)
            
    return sorted(unique_matches[:3], key=lambda x: x["match_score"], reverse=True)
