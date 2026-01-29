from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import CandidateProfile, User, Application, Internship
from app.schemas.all import CandidateCreate, CandidateResponse, CandidateUpdate

router = APIRouter()

@router.post("/", response_model=CandidateResponse)
def create_candidate_profile(candidate: CandidateCreate, user_id: int, db: Session = Depends(get_db)):
    db_candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    if db_candidate:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    new_candidate = CandidateProfile(**candidate.dict(), user_id=user_id)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

@router.get("/{user_id}", response_model=CandidateResponse)
def get_candidate_profile(user_id: int, db: Session = Depends(get_db)):
    candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Profile not found")
    return candidate

@router.get("/{user_id}/applications")
def get_candidate_applications(user_id: int, db: Session = Depends(get_db)):
    candidate = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    if not candidate:
        return []
    
    apps = db.query(Application).filter(Application.student_id == candidate.id).all()
    
    results = []
    for app in apps:
        results.append({
            "id": app.id,
            "job_title": app.internship.title,
            "role": app.internship.title, 
            "company": app.internship.company or (app.internship.recruiter.full_name if app.internship.recruiter else "Company"),
            "applied_at": app.applied_at.isoformat() if hasattr(app.applied_at, 'isoformat') else str(app.applied_at),
            "status": app.status,
            "match_score": app.match_score
        })
    return results
