from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Internship, User, CandidateProfile, Application
from app.schemas.jobs import JobCreate, JobResponse, ApplicationResponse
from app.utils.logging import log_activity

router = APIRouter()

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, recruiter_id: int, db: Session = Depends(get_db)):
    # Verify recruiter exists
    recruiter = db.query(User).filter(User.id == recruiter_id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    if recruiter.role != "recruiter" and recruiter.role != "admin":
         raise HTTPException(status_code=403, detail="Only recruiters can post jobs")

    db_job = Internship(
        **job.dict(),
        recruiter_id=recruiter_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    log_activity(db, recruiter_id, "Created Job", "Internship", db_job.id, {"title": db_job.title})
    
    return db_job

@router.get("/", response_model=List[JobResponse])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Internship).offset(skip).limit(limit).all()
    return jobs

@router.get("/recruiter/{recruiter_id}", response_model=List[JobResponse])
def read_recruiter_jobs(recruiter_id: int, db: Session = Depends(get_db)):
    jobs = db.query(Internship).filter(Internship.recruiter_id == recruiter_id).all()
    for job in jobs:
        job.application_count = len(job.applications)
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Internship).filter(Internship.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/match/{candidate_id}")
def match_jobs(candidate_id: int, db: Session = Depends(get_db)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.id == candidate_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    candidate_skills = [s.lower() for s in (profile.skills or [])]
    all_jobs = db.query(Internship).filter(Internship.is_active == True).all()
    
    matches = []
    for job in all_jobs:
        job_skills = [s.lower() for s in (job.required_skills or [])]
        if not job_skills:
            score = 50
        else:
            intersection = set(candidate_skills).intersection(set(job_skills))
            score = int((len(intersection) / len(job_skills)) * 100) if job_skills else 50
        
        if score > 0: score = min(100, score + 10)

        if score >= 0:
            matches.append({
                "id": job.id,
                "title": job.title,
                "company": job.company or (job.recruiter.full_name if job.recruiter else "Innovative Tech"),
                "location": job.location,
                "salary": job.stipend_salary or "Not Disclosed",
                "score": score,
                "match_reasons": [f"Matched {len(set(candidate_skills).intersection(set(job_skills)))} key skills."] if job_skills else ["General match based on profile."],
                "missing_skills": list(set(job_skills) - set(candidate_skills))[:3],
                "tags": job.required_skills[:3] if job.required_skills else ["General"],
                "mode": job.mode or "On-site",
                "duration": job.duration or "Permanent",
                "job_type": job.internship_type,
                "deadline": job.deadline.isoformat() if job.deadline else None
            })
    
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:10]

@router.get("/{job_id}/applications", response_model=List[ApplicationResponse])
def read_job_applications(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Internship).filter(Internship.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    applications = db.query(Application).filter(Application.internship_id == job_id).all()
    return applications
