from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .all import CandidateResponse, StudentProfessionalResponse

class InternshipBase(BaseModel):
    title: str
    description: str
    location: str
    company: Optional[str] = "Organization Name"
    salary_range: Optional[str] = None
    internship_type: str = "Internship" # Internship, Training Program
    mode: str = "Office"        # Online, Offline, Hybrid
    duration: str = "3 Months"  # e.g., 6 months
    stipend_salary: str = "Unpaid"
    eligibility_criteria: Optional[str] = None
    deadline: Optional[datetime] = None
    required_skills: List[str] = []
    status: str = "Active"      # Draft, Active, Closed

class InternshipCreate(InternshipBase):
    pass

class InternshipUpdate(InternshipBase):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    is_active: Optional[bool] = None

class InternshipResponse(InternshipBase):
    id: int
    recruiter_id: int
    created_at: datetime
    is_active: bool
    
    application_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class ApplicationResponse(BaseModel):
    id: int
    internship_id: int
    student_id: int
    status: str
    match_score: int
    recruiter_notes: Optional[str] = None # Internal
    interview_date: Optional[datetime] = None
    interview_mode: Optional[str] = None
    feedback: Optional[str] = None        # Shared
    applied_at: datetime
    updated_at: datetime
    student: Optional[StudentProfessionalResponse] = None
    internship: Optional[InternshipResponse] = None

    model_config = ConfigDict(from_attributes=True)

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    recruiter_notes: Optional[str] = None
    feedback: Optional[str] = None
    interview_date: Optional[datetime] = None
    interview_mode: Optional[str] = None
