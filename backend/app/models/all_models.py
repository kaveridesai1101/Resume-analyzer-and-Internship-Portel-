from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="candidate") # candidate, recruiter, admin
    is_active = Column(Boolean, default=True)

    candidate_profile = relationship("CandidateProfile", back_populates="user", uselist=False)
    jobs = relationship("Job", back_populates="recruiter")

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    skills = Column(JSON, default=[])      # Store as JSON array
    experience = Column(JSON, default=[])  # Store structured experience
    education = Column(JSON, default=[])
    resume_url = Column(String, nullable=True)
    latest_score = Column(Integer, nullable=True)
    last_analyzed = Column(DateTime, nullable=True)
    completeness = Column(String, default="Awaiting Resume") # Awaiting Resume, Basic, Moderate, Strong

    user = relationship("User", back_populates="candidate_profile")
    applications = relationship("Application", back_populates="candidate")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    company = Column(String, index=True, default="Innovative Tech")
    description = Column(String)
    required_skills = Column(JSON, default=[])
    location = Column(String)
    salary_range = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    recruiter = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("candidate_profiles.id"))
    status = Column(String, default="Applied") # Applied, Under Review, Shortlisted, Interview Call, Selected, Rejected
    match_score = Column(Integer, nullable=True)
    recruiter_notes = Column(String, nullable=True) # Internal
    feedback = Column(String, nullable=True)        # Visible to candidate
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = relationship("Job", back_populates="applications")
    candidate = relationship("CandidateProfile", back_populates="applications")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String) # e.g., "Applied to Job", "Shortlisted Candidate"
    entity_type = Column(String) # e.g., "Application", "Job", "Resume"
    entity_id = Column(Integer)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
