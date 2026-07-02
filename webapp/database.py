from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./resume_ranker.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class JobRun(Base):
    __tablename__ = "job_runs"
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    job_description = Column(Text)
    jd_requirements = Column(Text)   # JSON string
    shortlist_count = Column(Integer)
    total_resumes = Column(Integer, default=0)
    processed_resumes = Column(Integer, default=0)
    time_taken_seconds = Column(Float, default=0)
    status = Column(String, default="pending")  # pending, processing, done, error
    error_message = Column(Text, nullable=True)

class ResumeResult(Base):
    __tablename__ = "resume_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_run_id = Column(String)
    filename = Column(String)
    file_path = Column(String)
    rank = Column(Integer)
    score = Column(Float)
    skills_match = Column(Float)
    experience_match = Column(Float)
    education_match = Column(Float)
    missing_skills = Column(Text)   # JSON string
    strengths = Column(Text)        # JSON string
    summary = Column(Text)
    is_shortlisted = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

