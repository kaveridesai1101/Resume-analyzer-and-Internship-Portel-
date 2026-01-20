from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional, Any
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "candidate" # candidate, recruiter, admin

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

# --- Candidate Schemas ---
class CandidateProfileBase(BaseModel):
    name: Optional[str] = None
    skills: List[str] = []
    experience: List[dict] = []
    education: List[dict] = []
    bio: Optional[str] = None

class CandidateCreate(CandidateProfileBase):
    pass

class CandidateUpdate(CandidateProfileBase):
    pass

class CandidateResponse(CandidateProfileBase):
    id: int
    user_id: int
    resume_url: Optional[str] = None
    latest_score: Optional[int] = None
    last_analyzed: Optional[Any] = None
    completeness: str = "Awaiting Resume"
    
    model_config = ConfigDict(from_attributes=True)

class CandidateProfessionalResponse(BaseModel):
    """Restricted view for Recruiters as per Master Prompt."""
    id: int
    name: Optional[str] = None
    skills: List[str] = []
    experience: List[dict] = []
    education: List[dict] = []
    bio: Optional[str] = None # Summary
    completeness: str = "Awaiting Resume" # Available status
    latest_score: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

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

