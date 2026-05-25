from sqlalchemy import Column, String, JSON, DateTime, Integer
import datetime
from database.postgres import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    # Primary key uses the file hash for easy deduplication
    file_hash = Column(String, primary_key=True, index=True)
    
    # Original filename
    filename = Column(String, nullable=True)
    
    # Original parsed structure
    parsed_json = Column(JSON, nullable=False)
    
    # AI generated results
    intelligence_result = Column(JSON, nullable=False)
    
    # Generated role matches cache
    role_matches = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Simple analytics
    tokens_used = Column(Integer, default=0)
    latency_seconds = Column(Integer, default=0)
