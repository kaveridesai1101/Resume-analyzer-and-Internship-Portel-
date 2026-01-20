from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Job, User, CandidateProfile, Application
from app.models.all_models import Job, User, CandidateProfile, Application
from app.schemas.jobs import JobCreate, JobResponse, ApplicationResponse
from app.utils.logging import log_activity

router = APIRouter()

# TODO: Add proper dependency to get current user ID from token
# For MVP demo, we might pass a header or just use a mock recruiter ID if not fully authenticated yet
# But since we have Auth, let's try to use it or expect the frontend to send the user_id for now if we want to skip complex dep injection setup in one go.
# ideally: def create_job(job: JobCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, recruiter_id: int, db: Session = Depends(get_db)):
    # Verify recruiter exists
    recruiter = db.query(User).filter(User.id == recruiter_id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    # Simple check for role (optional but good)
    if recruiter.role != "recruiter" and recruiter.role != "admin":
         raise HTTPException(status_code=403, detail="Only recruiters can post jobs")

    db_job = Job(
        **job.dict(),
        recruiter_id=recruiter_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Log Job Creation
    log_activity(db, recruiter_id, "Created Job", "Job", db_job.id, {"title": db_job.title})
    
    return db_job

@router.get("/", response_model=List[JobResponse])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs

@router.get("/recruiter/{recruiter_id}", response_model=List[JobResponse])
def read_recruiter_jobs(recruiter_id: int, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.recruiter_id == recruiter_id).all()
    # Populate application count
    for job in jobs:
        job.application_count = len(job.applications)
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/match/{candidate_id}")
def match_jobs(candidate_id: int, db: Session = Depends(get_db)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.id == candidate_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    candidate_skills = [s.lower() for s in (profile.skills or [])]
    all_jobs = db.query(Job).filter(Job.is_active == True).all()
    
    matches = []
    for job in all_jobs:
        job_skills = [s.lower() for s in (job.required_skills or [])]
        if not job_skills:
            score = 50
        else:
            intersection = set(candidate_skills).intersection(set(job_skills))
            score = int((len(intersection) / len(job_skills)) * 100) if job_skills else 50
        
        # Boost score slightly if they have at least one skill
        if score > 0: score = min(100, score + 10)

        if score >= 0: # Show all matches for now, sorted by score
            # Align with frontend expectations
            matches.append({
                "id": job.id,
                "title": job.title,
                "company": job.company or (job.recruiter.full_name if job.recruiter else "Innovative Tech"),
                "location": job.location,
                "salary": job.salary_range or "Not Disclosed",
                "score": score,
                "match_reasons": [f"Matched {len(set(candidate_skills).intersection(set(job_skills)))} key skills."] if job_skills else ["General match based on profile."],
                "missing_skills": list(set(job_skills) - set(candidate_skills))[:3],
                "tags": job.required_skills[:3] if job.required_skills else ["General"],
                "mode": "Remote" if "remote" in (job.location or "").lower() else "On-site",
                "duration": "Permanent"
            })
    
    # Sort by match percentage
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:10] # Top 10 matches

@router.get("/{job_id}/applications", response_model=List[ApplicationResponse])
def read_job_applications(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    applications = db.query(Application).filter(Application.job_id == job_id).all()
    return applications
