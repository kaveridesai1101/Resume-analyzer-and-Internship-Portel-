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
    recruiter_profile = relationship("RecruiterProfile", back_populates="user", uselist=False)
    internships = relationship("Internship", back_populates="recruiter")

class RecruiterProfile(Base):
    __tablename__ = "recruiter_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization_name = Column(String)
    recruiter_id_code = Column(String, unique=True) # Official ID
    verification_status = Column(String, default="Pending") # Pending, Verified, Rejected
    contact_email = Column(String)
    account_status = Column(String, default="Active") # Active, Suspended
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recruiter_profile")

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    skills = Column(JSON, default=[])      # Store as JSON array
    experience = Column(JSON, default=[])  # Store structured experience
    education = Column(JSON, default=[])
    resume_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latest_score = Column(Integer, nullable=True)
    last_analyzed = Column(DateTime, nullable=True)
    summary = Column(String, nullable=True)
    improvement_tips = Column(JSON, default=[])
    completeness = Column(String, default="Awaiting Resume") # Awaiting Resume, Basic, Moderate, Strong

    user = relationship("User", back_populates="candidate_profile")
    applications = relationship("Application", back_populates="student")

class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    company = Column(String, index=True, default="Organization Name")
    description = Column(String)
    internship_type = Column(String) # Internship, Training Program
    mode = Column(String)     # Online, Offline, Hybrid
    duration = Column(String) # e.g., 6 months
    stipend_salary = Column(String)
    eligibility_criteria = Column(String)
    required_skills = Column(JSON, default=[])
    location = Column(String)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="Active") # Draft, Active, Closed

    recruiter = relationship("User", back_populates="internships")
    applications = relationship("Application", back_populates="internship")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    internship_id = Column(Integer, ForeignKey("internships.id"))
    student_id = Column(Integer, ForeignKey("candidate_profiles.id"))
    status = Column(String, default="Applied") # Applied, Under Review, Shortlisted, Interview Scheduled, Interview Completed, Selected, Rejected
    match_score = Column(Integer, nullable=True)
    recruiter_notes = Column(String, nullable=True) # Internal
    interview_date = Column(DateTime, nullable=True)
    interview_mode = Column(String, nullable=True)
    feedback = Column(String, nullable=True)        # Visible to candidate
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    internship = relationship("Internship", back_populates="applications")
    student = relationship("CandidateProfile", back_populates="applications")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String) # e.g., "Applied to Internship", "Shortlisted Student"
    entity_type = Column(String) # e.g., "Application", "Internship", "Resume"
    entity_id = Column(Integer)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
