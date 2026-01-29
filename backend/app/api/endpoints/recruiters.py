from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import RecruiterProfile, User
from app.schemas.all import RecruiterProfileResponse, RecruiterProfileBase
from app.utils.logging import log_activity
from app.core.security import get_current_user
import sqlite3
import json

router = APIRouter()

@router.get("/me/stats")
async def get_recruiter_stats(current_user: any = Depends(get_current_user)):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        # Count active jobs
        curr.execute("SELECT COUNT(*) FROM internships WHERE recruiter_id = ?", (current_user.id,))
        active_jobs = curr.fetchone()[0]
        
        # Count total applications
        curr.execute("""
            SELECT COUNT(*) FROM applications a
            JOIN internships i ON a.internship_id = i.id
            WHERE i.recruiter_id = ?
        """, (current_user.id,))
        total_apps = curr.fetchone()[0]
        
        # Count reviewed candidates (status is not 'Applied')
        curr.execute("""
            SELECT COUNT(*) FROM applications a
            JOIN internships i ON a.internship_id = i.id
            WHERE i.recruiter_id = ? AND a.status != 'Applied'
        """, (current_user.id,))
        reviewed = curr.fetchone()[0]
        
        # Count scheduled interviews
        curr.execute("""
            SELECT COUNT(*) FROM applications a
            JOIN internships i ON a.internship_id = i.id
            WHERE i.recruiter_id = ? AND a.status = 'Interview Call'
        """, (current_user.id,))
        interviews = curr.fetchone()[0]
        
        conn.close()
        return {
            "active_jobs": active_jobs,
            "total_applications": total_apps,
            "reviewed_candidates": reviewed,
            "scheduled_interviews": interviews
        }
    except Exception as e:
        print(f"Recruiter Stats Error: {e}")
        return {"active_jobs": 0, "total_applications": 0, "reviewed_candidates": 0, "scheduled_interviews": 0}

@router.get("/me/applications")
async def get_recent_applications(current_user: any = Depends(get_current_user)):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        query = """
            SELECT a.*, i.title as internship_title, cp.name as student_name
            FROM applications a
            JOIN internships i ON a.internship_id = i.id
            JOIN candidate_profiles cp ON a.student_id = cp.id
            WHERE i.recruiter_id = ?
            ORDER BY a.applied_at DESC
            LIMIT 5
        """
        curr.execute(query, (current_user.id,))
        rows = curr.fetchall()
        
        results = []
        for row in rows:
            d = dict(row)
            d['student'] = {"full_name": row['student_name']}
            d['internship'] = {"title": row['internship_title']}
            d['created_at'] = row['applied_at']
            results.append(d)
            
        conn.close()
        return results
    except Exception as e:
        print(f"Recruiter Apps Error: {e}")
        return []

@router.get("/me/jobs")
async def get_my_jobs(current_user: any = Depends(get_current_user)):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        query = """
            SELECT i.*, (SELECT COUNT(*) FROM applications WHERE internship_id = i.id) as applications_count
            FROM internships i
            WHERE i.recruiter_id = ?
            ORDER BY i.created_at DESC
        """
        curr.execute(query, (current_user.id,))
        rows = curr.fetchall()
        
        results = []
        for row in rows:
            d = dict(row)
            d['status'] = 'active' # Placeholder
            results.append(d)
            
        conn.close()
        return results
    except Exception as e:
        print(f"Recruiter Jobs Error: {e}")
        return []


@router.get("/me", response_model=RecruiterProfileResponse)
def get_my_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user_id).first()
    if not profile:
        # Create a default profile if it doesn't exist
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
             raise HTTPException(status_code=404, detail="User not found")
        
        profile = RecruiterProfile(
            user_id=user_id,
            organization_name=user.full_name,
            contact_email=user.email
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile

@router.patch("/me", response_model=RecruiterProfileResponse)
def update_my_profile(user_id: int, profile_data: RecruiterProfileBase, db: Session = Depends(get_db)):
    profile = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if profile_data.organization_name is not None:
        profile.organization_name = profile_data.organization_name
    if profile_data.recruiter_id_code is not None:
        profile.recruiter_id_code = profile_data.recruiter_id_code
    if profile_data.industry is not None:
        profile.industry = profile_data.industry
    if profile_data.address is not None:
        profile.address = profile_data.address
    if profile_data.contact_role is not None:
        profile.contact_role = profile_data.contact_role
    if profile_data.contact_email is not None:
        profile.contact_email = profile_data.contact_email
        
    db.commit()
    db.refresh(profile)
    
    log_activity(db, user_id, "Updated Recruiter Profile", "RecruiterProfile", profile.id)
    
    return profile
