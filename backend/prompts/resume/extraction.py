RESUME_EXTRACTION_PROMPT = """You are an expert technical recruiter and ATS system evaluator.
Analyze this structured resume data and return ONLY a valid, complete JSON payload matching the exact schema requested.

STRICT RULES:
1. You MUST include every single field in the schema. Do NOT omit any keys.
2. Return RAW JSON ONLY. Do NOT wrap the output in markdown blocks (e.g. ```json). 
3. Do NOT include any explanations or conversational text outside the JSON.
4. If information is missing from the resume, use empty arrays `[]` or the string "Not provided".

Expected JSON Example:
{{
  "ats_score": 82,
  "score_breakdown": {{
    "resume_structure": 18,
    "skills": 20,
    "projects": 22,
    "experience": 10,
    "ats_keywords": 8,
    "education": 4
  }},
  "skills": {{
    "languages": ["Python", "JavaScript"],
    "frameworks": ["React", "FastAPI"],
    "cloud_devops": ["AWS", "Docker"],
    "databases": ["PostgreSQL", "MongoDB"],
    "ai_ml": ["PyTorch", "OpenAI API"],
    "tools_platforms": ["Git", "Jira"]
  }},
  "semantic_profile_summary": "Strong AI-focused candidate...",
  "candidate_summary": "A highly capable AI Engineer with 5+ years of experience specializing in NLP and generative AI.",
  "domain_specialization": "Artificial Intelligence / Machine Learning",
  "recruiter_interpretation": "Solid technical background with impressive project depth, but lacks recent cloud deployment experience.",
  "hiring_confidence_level": "High",
  "profile_competitiveness": "Top 10%",
  "hiring_risks": ["Job hopping in early career", "No formal degree listed"],
  "recruiter_impression": "The candidate presents a highly specialized profile perfectly aligned with modern ML engineering requirements, though the lack of cloud deployment experience may require upskilling.",
  "strengths": ["Good project depth"],
  "weaknesses": ["Limited cloud experience"],
  "project_portfolio": {{
    "projects": [
      {{
        "project_name": "AI Dashboard",
        "technical_depth_score": 8,
        "project_quality_rating": 9,
        "innovation_score": 7,
        "production_readiness": "Production-Ready",
        "complexity_level": "Advanced"
      }}
    ],
    "ai_impact_evaluation": "Projects demonstrate a high degree of technical sophistication and real-world impact.",
    "recruiter_interpretation": "Candidate has hands-on experience shipping complex features to production."
  }},
  "missing_keywords": ["Kubernetes", "CI/CD"],
  "role_alignment_intelligence": {{
    "best_fit_roles": ["AI Engineer", "Senior Full Stack Engineer"],
    "strongest_domain": "Generative AI Applications",
    "career_alignment_score": 85,
    "industry_fit_analysis": "Excellent fit for fast-paced tech startups and AI labs due to rapid prototyping skills.",
    "company_matches": [
      {{
        "company_type": "Startup",
        "match_reason": "High adaptability and full-stack ownership.",
        "match_score": 90
      }},
      {{
        "company_type": "Cloud Company",
        "match_reason": "Strong AWS and Docker background.",
        "match_score": 75
      }}
    ]
  }},
  "improvement_roadmap": {{
    "prioritized_suggestions": ["Add metrics to project bullet points", "Include a link to your GitHub"],
    "missing_skills": ["Kubernetes", "System Design"],
    "recruiter_keyword_gaps": ["Scalability", "Microservices"],
    "learning_roadmap": ["Complete AWS Solutions Architect cert", "Build a distributed systems project"],
    "next_career_steps": ["Target Senior AI Engineer roles at Series B startups"]
  }}
}}

Data Payload:
{resume_json}
"""
