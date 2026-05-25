from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedSkills(BaseModel):
    languages: Optional[List[str]] = Field(default_factory=list, description="Programming Languages")
    frameworks: Optional[List[str]] = Field(default_factory=list, description="Frameworks & Libraries")
    cloud_devops: Optional[List[str]] = Field(default_factory=list, description="Cloud & DevOps")
    databases: Optional[List[str]] = Field(default_factory=list, description="Databases")
    ai_ml: Optional[List[str]] = Field(default_factory=list, description="AI / ML")
    tools_platforms: Optional[List[str]] = Field(default_factory=list, description="Tools & Platforms")

class ProjectEvaluation(BaseModel):
    project_name: str
    technical_depth_score: int = Field(..., description="Score out of 10")
    project_quality_rating: int = Field(..., description="Score out of 10")
    innovation_score: int = Field(..., description="Score out of 10")
    production_readiness: str = Field(..., description="e.g., 'Prototype', 'Production-Ready'")
    complexity_level: str = Field(..., description="'Beginner', 'Intermediate', 'Advanced'")

class ProjectPortfolioIntelligence(BaseModel):
    projects: List[ProjectEvaluation] = Field(default_factory=list)
    ai_impact_evaluation: str = Field(default="Not evaluated")
    recruiter_interpretation: str = Field(default="Not evaluated")

class CompanyMatch(BaseModel):
    company_type: str = Field(..., description="e.g. 'Startup', 'MNC', 'AI Company', 'Cloud Company'")
    match_reason: str = Field(...)
    match_score: int = Field(..., description="Score out of 100")

class RoleAlignmentIntelligence(BaseModel):
    best_fit_roles: List[str] = Field(default_factory=list)
    strongest_domain: str = Field(default="Not provided")
    career_alignment_score: int = Field(default=0, description="Score out of 100")
    industry_fit_analysis: str = Field(default="Not provided")
    company_matches: List[CompanyMatch] = Field(default_factory=list)

class ImprovementRoadmap(BaseModel):
    prioritized_suggestions: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    recruiter_keyword_gaps: List[str] = Field(default_factory=list)
    learning_roadmap: List[str] = Field(default_factory=list)
    next_career_steps: List[str] = Field(default_factory=list)

class ATSScoreBreakdown(BaseModel):
    resume_structure: Optional[int] = Field(default=0, description="Score out of 20")
    skills: Optional[int] = Field(default=0, description="Score out of 25")
    projects: Optional[int] = Field(default=0, description="Score out of 25")
    experience: Optional[int] = Field(default=0, description="Score out of 15")
    ats_keywords: Optional[int] = Field(default=0, description="Score out of 10")
    education: Optional[int] = Field(default=0, description="Score out of 5")

class ResumeIntelligenceResponse(BaseModel):
    ats_score: Optional[int] = Field(default=0, description="Total ATS score from 0 to 100")
    score_breakdown: Optional[ATSScoreBreakdown] = Field(default_factory=ATSScoreBreakdown, description="Detailed breakdown of the ATS score")
    skills: Optional[ExtractedSkills] = Field(default_factory=ExtractedSkills, description="Categorized extracted skills")
    semantic_profile_summary: Optional[str] = Field(default="Not provided", description="A professional 2-sentence recruiter summary")
    candidate_summary: Optional[str] = Field(default="Not provided", description="AI-generated broader candidate summary")
    domain_specialization: Optional[str] = Field(default="Not provided", description="Domain specialization detection, e.g., 'Full Stack Web Development'")
    recruiter_interpretation: Optional[str] = Field(default="Not provided", description="A candid, concise recruiter-style interpretation")
    hiring_confidence_level: Optional[str] = Field(default="Medium", description="e.g., 'High', 'Medium', 'Low'")
    profile_competitiveness: Optional[str] = Field(default="Average", description="e.g., 'Top 10%', 'Top 25%', 'Average'")
    hiring_risks: Optional[List[str]] = Field(default_factory=list, description="List of potential red flags for recruiters")
    recruiter_impression: Optional[str] = Field(default="Not provided", description="A sharp, paragraph-style evaluation of the candidate")
    strengths: Optional[List[str]] = Field(default_factory=list, description="3-5 strong points in the candidate's profile")
    weaknesses: Optional[List[str]] = Field(default_factory=list, description="2-3 areas for improvement in the profile")
    project_portfolio: Optional[ProjectPortfolioIntelligence] = Field(default_factory=ProjectPortfolioIntelligence, description="Deep evaluation of all projects")
    missing_keywords: Optional[List[str]] = Field(default_factory=list, description="Keywords generally expected for this type of profile that are missing")
    role_alignment_intelligence: Optional[RoleAlignmentIntelligence] = Field(default_factory=RoleAlignmentIntelligence, description="Career and company matching")
    improvement_roadmap: Optional[ImprovementRoadmap] = Field(default_factory=ImprovementRoadmap, description="Actionable tips for the candidate to improve their resume")
