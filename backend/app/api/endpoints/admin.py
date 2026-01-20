from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import User, Job, Application, CandidateProfile
from pydantic import BaseModel, ConfigDict
from app.schemas.all import ActivityLogResponse
from app.models.all_models import ActivityLog

router = APIRouter()

class SystemStats(BaseModel):
    total_candidates: int
    total_recruiters: int
    total_jobs: int
    total_applications: int
    total_resumes: int

class UserList(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

@router.get("/stats", response_model=SystemStats)
def get_system_stats(db: Session = Depends(get_db)):
    # TODO: In real app, check for Admin role here!
    
    t_candidates = db.query(User).filter(User.role == "candidate").count()
    t_recruiters = db.query(User).filter(User.role == "recruiter").count()
    t_jobs = db.query(Job).count()
    t_apps = db.query(Application).count()
    t_resumes = db.query(CandidateProfile).filter(CandidateProfile.resume_url != None).count()
    
    return {
        "total_candidates": t_candidates,
        "total_recruiters": t_recruiters,
        "total_jobs": t_jobs,
        "total_applications": t_apps,
        "total_resumes": t_resumes # Added
    }

@router.get("/activity", response_model=List[ActivityLogResponse])
def get_activity_logs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    # TODO: Admin only check
    logs = db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/users", response_model=List[UserList])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Admin only check
    users = db.query(User).offset(skip).limit(limit).all()
    return users
