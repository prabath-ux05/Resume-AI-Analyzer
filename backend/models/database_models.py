from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
import datetime
from database.postgres import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    # Primary key uses the file hash for easy deduplication
    file_hash = Column(String, primary_key=True, index=True)
    
    # Original filename
    filename = Column(String, nullable=True)
    
    # Original parsed structure
    parsed_json = Column(JSONB, nullable=False)
    
    # AI generated results
    intelligence_result = Column(JSONB, nullable=False)
    
    # DEPRECATED: Generated role matches cache (Use RoleMatchHistory instead)
    role_matches = Column(JSONB, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Simple analytics
    tokens_used = Column(Integer, default=0)
    latency_seconds = Column(Integer, default=0)


class RoleMatchHistory(Base):
    __tablename__ = "role_match_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_hash = Column(String, ForeignKey("resume_analysis.file_hash"), index=True, nullable=False)
    
    # Store exactly what the AI generated
    matches_json = Column(JSONB, nullable=False)
    
    # Model used (e.g., llama-3.1-8b-instant)
    model_version = Column(String, nullable=False, default="llama-3.1-8b-instant")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

