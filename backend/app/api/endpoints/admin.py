from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import User, Internship, Application, CandidateProfile, RecruiterProfile, ActivityLog
from pydantic import BaseModel, ConfigDict
from app.schemas.all import ActivityLogResponse
from app.utils.logging import log_activity

router = APIRouter()

class SystemStats(BaseModel):
    total_students: int
    total_recruiters: int
    total_internships: int
    total_applications: int
    total_resumes: int

class UserList(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class AdminProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

@router.get("/stats", response_model=SystemStats)
def get_system_stats(db: Session = Depends(get_db)):
    """Get system statistics (AICTE Compliance - Admin only)"""
    try:
        t_students = db.query(User).filter(User.role.in_(["student", "candidate"])).count()
        t_recruiters = db.query(User).filter(User.role == "recruiter").count()
        t_internships = db.query(Internship).count()
        t_apps = db.query(Application).count()
        t_resumes = db.query(CandidateProfile).filter(CandidateProfile.resume_url != None).count()
        
        return {
            "total_students": t_students,
            "total_recruiters": t_recruiters,
            "total_internships": t_internships,
            "total_applications": t_apps,
            "total_resumes": t_resumes
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Stats Error: {str(e)}")

@router.get("/activity", response_model=List[ActivityLogResponse])
def get_activity_logs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get activity logs (AICTE Compliance - Admin only)"""
    try:
        logs = db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).offset(skip).limit(limit).all()
        return logs
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Activity Error: {str(e)}")

@router.get("/users", response_model=List[UserList])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users (AICTE Compliance - Admin only)"""
    # TODO: Admin only check
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Users Error: {str(e)}")

@router.get("/internships", response_model=List[dict])
def get_all_internships(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all internships with details (AICTE Compliance - Admin only)"""
    # TODO: Admin only check
    internships = db.query(Internship).offset(skip).limit(limit).all()
    # Map to dict with application count
    result = []
    for internship in internships:
        app_count = db.query(Application).filter(Application.internship_id == internship.id).count()
        i_dict = {
            "id": internship.id,
            "title": internship.title,
            "location": internship.location,
            "internship_type": internship.internship_type,
            "status": internship.status,
            "is_active": internship.is_active,
            "created_at": internship.created_at,
            "application_count": app_count,
            "recruiter_email": internship.recruiter.email if internship.recruiter else "N/A"
        }
        result.append(i_dict)
    return result

@router.patch("/internships/{internship_id}/status")
def update_internship_status_admin(internship_id: int, status: str, is_active: bool, db: Session = Depends(get_db)):
    """Update internship status (AICTE Compliance - Admin only)"""
    # TODO: Admin only check
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    
    internship.status = status
    internship.is_active = is_active
    db.commit()
    
    log_activity(db, 1, f"Admin updated Internship {internship_id} status to {status}", "Internship", internship.id, {"is_active": is_active})
    
    return {"message": "Internship updated successfully", "status": internship.status, "is_active": internship.is_active}

from app.core import security
from typing import Optional

@router.patch("/me")
def update_admin_profile(profile_data: AdminProfileUpdate, db: Session = Depends(get_db)):
    """Update Admin Profile"""
    # Simplification for MVP: Update User ID 1 (The main Admin)
    # In production, use Depends(get_current_user)
    user_id = 1 
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Admin user not found")
        
    if profile_data.full_name:
        user.full_name = profile_data.full_name
    
    if profile_data.email:
        existing = db.query(User).filter(User.email == profile_data.email).filter(User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = profile_data.email
        
    if profile_data.password:
        user.hashed_password = security.get_password_hash(profile_data.password)
        
    db.commit()
    return {"message": "Profile updated successfully"}

@router.get("/users/{user_id}", response_model=dict)
def get_user_details_admin(user_id: int, db: Session = Depends(get_db)):
    """Get detailed user info for admin analysis"""
    try:
        # Authorization would go here
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Get Profile data based on role
        profile_data = {}
        if user.role == "candidate":
            candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()
            if candidate:
                profile_data = {
                    "name": candidate.name,
                    "skills": candidate.skills,
                    "resume_url": candidate.resume_url,
                    "experience": candidate.experience,
                    "education": candidate.education,
                    "bio": candidate.bio,
                    "score": candidate.latest_score
                }
        elif user.role == "recruiter":
            recruiter = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user.id).first()
            if recruiter:
                profile_data = {
                    "organization": recruiter.organization_name,
                    "department": recruiter.industry,
                    "contact_role": recruiter.contact_role,
                    "address": recruiter.address,
                    "website": recruiter.website
                }
                
        # Get Application History
        applications = []
        if user.role == "candidate":
            candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()
            if candidate:
                applications = db.query(Application).filter(Application.student_id == candidate.id).all()
        
        # Get Activity Log
        activities = db.query(ActivityLog).filter(ActivityLog.user_id == user.id).order_by(ActivityLog.created_at.desc()).limit(10).all()

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "profile": profile_data,
            "applications": [
                {"id": a.id, "status": a.status, "applied_at": a.applied_at, "internship_id": a.internship_id}
                for a in applications
            ],
            "activities": [
                {"action": log.action, "created_at": log.created_at}
                for log in activities
            ]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
