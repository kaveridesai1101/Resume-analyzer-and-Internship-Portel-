from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional, Any
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "student" # student, recruiter, admin

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

# --- Recruiter Schemas ---
class RecruiterProfileBase(BaseModel):
    organization_name: Optional[str] = None
    recruiter_id_code: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class RecruiterProfileCreate(RecruiterProfileBase):
    pass

class RecruiterProfileResponse(RecruiterProfileBase):
    id: int
    user_id: int
    verification_status: str
    account_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Student Schemas ---
class StudentProfileBase(BaseModel):
    name: Optional[str] = None
    skills: List[str] = []
    experience: List[dict] = []
    education: List[dict] = []
    bio: Optional[str] = None

class StudentCreate(StudentProfileBase):
    pass

class StudentUpdate(StudentProfileBase):
    pass

class StudentResponse(StudentProfileBase):
    id: int
    user_id: int
    resume_url: Optional[str] = None
    latest_score: Optional[int] = None
    last_analyzed: Optional[Any] = None
    completeness: str = "Awaiting Resume"
    
    model_config = ConfigDict(from_attributes=True)

class StudentProfessionalResponse(BaseModel):
    """Restricted view for Recruiters - AICTE Privacy Rules."""
    id: int
    name: Optional[str] = None
    skills: List[str] = []
    experience: List[dict] = []
    education: List[dict] = []
    bio: Optional[str] = None # Summary
    completeness: str = "Awaiting Resume" # Available status
    latest_score: Optional[int] = None
    # MASKED: No phone, email, or address for privacy (AICTE Rule)

    model_config = ConfigDict(from_attributes=True)

# Legacy alias for backward compatibility
CandidateResponse = StudentResponse
CandidateProfessionalResponse = StudentProfessionalResponse

class ActivityLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    details: Optional[dict] = None
    created_at: datetime
    user: UserInDB

    model_config = ConfigDict(from_attributes=True)

