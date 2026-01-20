from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from app.services.resume_parser import ResumeParser
from app.services.job_analyzer import JobAnalyzer
from app.services.matcher import MatchingEngine
from datetime import datetime
from app.utils.text_extractor import extract_text_from_binary

router = APIRouter()
parser = ResumeParser()
analyzer = JobAnalyzer()
matcher = MatchingEngine()

class JobDescriptionRequest(BaseModel):
    description: str

class MatchRequest(BaseModel):
    resume_data: dict
    job_data: dict

from app.database import get_db
from sqlalchemy.orm import Session
from app.models.all_models import CandidateProfile, User
from app.core.security import get_current_user # Need to implement get_current_user in security.py first or use a simple extraction
from fastapi import Depends

from app.utils.logging import log_activity
# ... (imports)

@router.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = await file.read()
    text = extract_text_from_binary(content, file.filename)
    
    data = parser.parse(text)
    
    # Calculate completeness
    score = data.get("score")
    if score is None:
        score = 0
    
    print(f"DEBUG: Analyzed resume for user {current_user.id}, score: {score}")

    if score >= 80: completeness = "Strong"
    elif score >= 60: completeness = "Moderate"
    else: completeness = "Basic"

    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(
            user_id=current_user.id,
            name=data.get("name", "Candidate"),
            skills=data.get("skills", []),
            experience=data.get("experience", []),
            education=data.get("education", []),
            latest_score=score,
            completeness=completeness,
            last_analyzed=datetime.utcnow()
        )
        db.add(profile)
    else:
        profile.name = data.get("name", profile.name)
        profile.skills = data.get("skills", [])
        profile.experience = data.get("experience", [])
        profile.education = data.get("education", [])
        profile.latest_score = score
        profile.completeness = completeness
        profile.last_analyzed = datetime.utcnow()
    
    db.commit()
    db.refresh(profile)

    # Log activity
    log_activity(db, current_user.id, "Analyzed Resume", "Resume", profile.id, {"score": score, "completeness": completeness})
    
    # Add profile ID to response for convenience
    data["candidate_id"] = profile.id
    return data

@router.post("/analyze-job")
async def analyze_job(request: JobDescriptionRequest):
    data = analyzer.analyze(request.description)
    return data

@router.post("/match")
async def match_candidate_job(request: MatchRequest):
    result = matcher.calculate_score(request.resume_data, request.job_data)
    return result

@router.delete("/resume", status_code=204)
async def delete_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Reset profile fields
    profile.skills = []
    profile.experience = []
    profile.education = []
    profile.latest_score = None
    profile.completeness = "Awaiting Resume"
    profile.last_analyzed = None
    profile.resume_url = None
    
    db.commit()
    
    # Log activity
    log_activity(db, current_user.id, "Removed Resume", "Resume", profile.id)
    
    return None
