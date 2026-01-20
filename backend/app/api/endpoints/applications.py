from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Application, Job, CandidateProfile, User
from pydantic import BaseModel, ConfigDict
from datetime import datetime

router = APIRouter()

class ApplicationCreate(BaseModel):
    job_id: int
    candidate_id: int # In real auth, this comes from token

from app.schemas.jobs import ApplicationResponse, ApplicationUpdate
from app.utils.logging import log_activity

from fastapi import BackgroundTasks
from app.core.socket import manager
import asyncio

async def notify_recruiter(recruiter_id: int, message: str):
    await manager.send_personal_message(message, str(recruiter_id))

@router.post("/", response_model=ApplicationResponse)
def apply_to_job(
    application: ApplicationCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        # Check if already applied
        existing = db.query(Application).filter(
            Application.job_id == application.job_id,
            Application.candidate_id == application.candidate_id
        ).first()
        
        # Verify job and candidate exist
        job = db.query(Job).filter(Job.id == application.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        candidate = db.query(CandidateProfile).filter(CandidateProfile.id == application.candidate_id).first()
        if not candidate:
             raise HTTPException(status_code=404, detail="Candidate profile not found")

        # Mock Match Score Logic
        match_score = 85 

        if existing:
            # Re-apply mode
            existing.applied_at = datetime.utcnow()
            existing.match_score = match_score
            existing.status = "Applied"
            db.commit()
            db.refresh(existing)
            db_app = existing
            log_activity(db, candidate.user_id, "Re-applied to Job", "Application", db_app.id, {"job_title": job.title})
        else:
            db_app = Application(
                job_id=application.job_id,
                candidate_id=application.candidate_id,
                match_score=match_score,
                status="Applied"
            )
            db.add(db_app)
            db.commit()
            db.refresh(db_app)
            log_activity(db, candidate.user_id, "Applied to Job", "Application", db_app.id, {"job_title": job.title})
        
        # Schedule notification in background (non-blocking)
        message = f"New application received for {job.title} from {candidate.name}"
        background_tasks.add_task(notify_recruiter, job.recruiter_id, message)
        
        return db_app
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print("CRASH IN APPLY_TO_JOB:", error_msg)
        return JSONResponse(status_code=400, content={"detail": f"Backend Crash: {str(e)}", "trace": error_msg})

@router.get("/job/{job_id}", response_model=List[ApplicationResponse])
def get_job_applications(job_id: int, db: Session = Depends(get_db)):
    apps = db.query(Application).filter(Application.job_id == job_id).all()
    return apps

@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application_status(
    application_id: int, 
    update_data: ApplicationUpdate, 
    recruiter_id: int, # Should come from current_user in real auth
    db: Session = Depends(get_db)
):
    db_app = db.query(Application).filter(Application.id == application_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update fields
    if update_data.status:
        db_app.status = update_data.status
    if update_data.recruiter_notes is not None:
        db_app.recruiter_notes = update_data.recruiter_notes
    if update_data.feedback is not None:
        db_app.feedback = update_data.feedback
    
    db_app.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_app)
    
    # Log the action (Recruiter action)
    log_activity(
        db, 
        recruiter_id, 
        f"Updated Application Status to {db_app.status}", 
        "Application", 
        db_app.id, 
        {"candidate_id": db_app.candidate_id, "job_id": db_app.job_id}
    )
    
    return db_app
