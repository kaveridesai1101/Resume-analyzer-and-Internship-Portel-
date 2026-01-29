from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from app.services.resume_parser import ResumeParser
from app.services.internship_analyzer import InternshipAnalyzer
from app.services.matcher import MatchingEngine
from datetime import datetime
from app.utils.text_extractor import extract_text_from_binary

router = APIRouter()
parser = ResumeParser()
analyzer = InternshipAnalyzer()
matcher = MatchingEngine()

class InternshipDescriptionRequest(BaseModel):
    description: str

class MatchRequest(BaseModel):
    resume_data: dict
    internship_data: dict

from app.database import get_db
from sqlalchemy.orm import Session
from app.models.all_models import CandidateProfile, User
from app.core.security import get_current_user
from fastapi import Depends

from app.utils.logging import log_activity
import sqlite3
import json
import os

@router.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...), 
    current_user: any = Depends(get_current_user)
):
    try:
        print(f"DEBUG: analyze_resume started for user {current_user.id}")
        content = await file.read()
        print(f"DEBUG: File read. Size: {len(content)}")
        
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
            
        # Save the physical file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        uploads_dir = os.path.join(base_dir, "uploads")
        
        if not os.path.exists(uploads_dir):
            try:
                os.makedirs(uploads_dir)
                print(f"DEBUG: Created uploads directory at {uploads_dir}")
            except Exception as e:
                print(f"DEBUG: Failed to create uploads folder: {e}")
                
        # Sanitize filename
        raw_filename = file.filename or "resume.pdf"
        clean_filename = "".join([c for c in raw_filename if c.isalnum() or c in "._- "])
        if not clean_filename: clean_filename = "resume.bin"
        
        save_path = os.path.join(uploads_dir, clean_filename)
        print(f"DEBUG: Saving file to {save_path}")
        
        file_saved = False
        try:
            with open(save_path, "wb") as f:
                f.write(content)
            file_saved = True
            print("DEBUG: Physical file saved successfully")
        except Exception as e:
            print(f"DEBUG: File save error: {e}")
            
        print("DEBUG: Starting text extraction")
        text = extract_text_from_binary(content, clean_filename)
        print(f"DEBUG: Extracted text length: {len(text)}")
        
        print("DEBUG: Starting parser")
        data = parser.parse(text)
        print(f"DEBUG: Parsed data: {list(data.keys())}")
        
        # Calculate completeness
        score = data.get("score", 50)
        
        if score >= 80: completeness = "Strong"
        elif score >= 60: completeness = "Moderate"
        else: completeness = "Basic"

        now = datetime.utcnow().isoformat()
        db_path = os.path.join(base_dir, 'skillmatch.db')
        
        print(f"DEBUG: Connecting to DB at {db_path}")
        conn = sqlite3.connect(db_path)
        curr = conn.cursor()
        
        # Check if profile exists
        curr.execute("SELECT id FROM candidate_profiles WHERE user_id = ?", (current_user.id,))
        profile_row = curr.fetchone()
        
        skills_json = json.dumps(data.get("skills", []))
        exp_json = json.dumps(data.get("experience", []))
        edu_json = json.dumps(data.get("education", []))
        resume_url = f"/uploads/{clean_filename}" if file_saved else None
        
        if not profile_row:
            print("DEBUG: Creating new candidate profile")
            curr.execute(
                """INSERT INTO candidate_profiles 
                   (user_id, name, skills, experience, education, latest_score, completeness, last_analyzed, resume_url, summary, improvement_tips) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (current_user.id, data.get("name", "Student"), skills_json, exp_json, edu_json, score, completeness, now, resume_url, data.get("summary"), json.dumps(data.get("improvement_tips", [])))
            )
            profile_id = curr.lastrowid
        else:
            profile_id = profile_row[0]
            print(f"DEBUG: Updating existing profile {profile_id}")
            curr.execute(
                """UPDATE candidate_profiles SET 
                   name = ?, skills = ?, experience = ?, education = ?, latest_score = ?, 
                   completeness = ?, last_analyzed = ?, resume_url = ?, summary = ?, improvement_tips = ? 
                   WHERE id = ?""",
                (data.get("name", "Student"), skills_json, exp_json, edu_json, score, completeness, now, resume_url, data.get("summary"), json.dumps(data.get("improvement_tips", [])), profile_id)
            )
        
        # Log activity
        details_json = json.dumps({"score": score, "completeness": completeness})
        curr.execute(
            """INSERT INTO activity_logs (user_id, action, entity_type, entity_id, details, created_at) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (current_user.id, "Analyzed Resume", "CandidateProfile", profile_id, details_json, now)
        )
        
        conn.commit()
        conn.close()
        print("DEBUG: DB operations completed successfully")
        
        data["student_id"] = profile_id
        return data
        
    except Exception as e:
        print(f"CRITICAL AI ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {str(e)}")

@router.post("/analyze-internship")
async def analyze_internship(request: InternshipDescriptionRequest):
    data = analyzer.analyze(request.description)
    return data

@router.post("/match")
async def match_student_internship(request: MatchRequest):
    result = matcher.calculate_score(request.resume_data, request.internship_data)
    return result

@router.delete("/resume", status_code=204)
async def delete_resume(
    current_user: User = Depends(get_current_user)
):
    try:
        db_path = os.path.join(os.getcwd(), 'skillmatch.db') # Fallback to cwd
        conn = sqlite3.connect(db_path)
        curr = conn.cursor()
        
        curr.execute("SELECT id FROM candidate_profiles WHERE user_id = ?", (current_user.id,))
        profile_row = curr.fetchone()
        
        if not profile_row:
            conn.close()
            raise HTTPException(status_code=404, detail="Profile not found")
        
        profile_id = profile_row[0]
        empty_json = json.dumps([])
        
        curr.execute(
            """UPDATE candidate_profiles SET 
               skills = ?, experience = ?, education = ?, latest_score = NULL, 
               completeness = 'Awaiting Resume', last_analyzed = NULL, resume_url = NULL 
               WHERE id = ?""",
            (empty_json, empty_json, empty_json, profile_id)
        )
        
        now = datetime.utcnow().isoformat()
        curr.execute(
            """INSERT INTO activity_logs (user_id, action, entity_type, entity_id, created_at) 
               VALUES (?, ?, ?, ?, ?)""",
            (current_user.id, "Removed Resume", "CandidateProfile", profile_id, now)
        )
        
        conn.commit()
        conn.close()
        return None
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))
