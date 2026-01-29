from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Internship, User, CandidateProfile, Application
from app.schemas.internships import InternshipCreate, InternshipResponse, ApplicationResponse
from app.utils.logging import log_activity

router = APIRouter()

import sqlite3
import json
from datetime import datetime

@router.post("/")
def create_internship(internship: InternshipCreate, recruiter_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        curr = conn.cursor()
        
        curr.execute("SELECT role, full_name FROM users WHERE id = ?", (recruiter_id,))
        user_row = curr.fetchone()
        if not user_row:
            conn.close()
            raise HTTPException(status_code=404, detail="Recruiter not found")
        
        if user_row[0] not in ["recruiter", "admin"]:
            conn.close()
            raise HTTPException(status_code=403, detail="Only recruiters can post internships")

        now = datetime.utcnow().isoformat()
        dead_str = internship.deadline.isoformat() if internship.deadline else None
        
        curr.execute(
            """INSERT INTO internships 
               (recruiter_id, title, company, location, description, required_skills, duration, stipend_salary, internship_type, mode, eligibility_criteria, deadline, created_at, is_active, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (recruiter_id, internship.title, internship.company or user_row[1], internship.location, 
             internship.description, json.dumps(getattr(internship, 'required_skills', [])), internship.duration, 
             getattr(internship, 'stipend_salary', 'N/A'), getattr(internship, 'internship_type', 'Internship'), 
             getattr(internship, 'mode', 'Remote'), getattr(internship, 'eligibility_criteria', ''), 
             dead_str, now, 1, 'Active')
        )
        internship_id = curr.lastrowid
        
        # Log activity
        curr.execute(
            "INSERT INTO activity_logs (user_id, action, entity_type, entity_id, created_at) VALUES (?, ?, ?, ?, ?)",
            (recruiter_id, "Created Internship", "Internship", internship_id, now)
        )
        
        conn.commit()
        conn.close()
        return {"id": internship_id, "title": internship.title, **internship.dict()}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def read_internships(skip: int = 0, limit: int = 100):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        curr.execute("SELECT * FROM internships ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, skip))
        rows = curr.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recruiter/{recruiter_id}")
def read_recruiter_internships(recruiter_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        curr.execute("SELECT * FROM internships WHERE recruiter_id = ?", (recruiter_id,))
        rows = curr.fetchall()
        
        results = []
        for row in rows:
            d = dict(row)
            curr.execute("SELECT COUNT(*) FROM applications WHERE internship_id = ?", (d['id'],))
            d['application_count'] = curr.fetchone()[0]
            results.append(d)
        
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{internship_id}")
def read_internship(internship_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        curr.execute("SELECT * FROM internships WHERE id = ?", (internship_id,))
        row = curr.fetchone()
        
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Internship not found")
        
        d = dict(row)
        curr.execute("SELECT COUNT(*) FROM applications WHERE internship_id = ?", (internship_id,))
        d['application_count'] = curr.fetchone()[0]
        
        conn.close()
        return d
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{internship_id}")
def delete_internship(internship_id: int, recruiter_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        curr = conn.cursor()
        
        curr.execute("SELECT recruiter_id FROM internships WHERE id = ?", (internship_id,))
        row = curr.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Internship not found")
        
        if row[0] != recruiter_id:
            conn.close()
            raise HTTPException(status_code=403, detail="Not authorized")
            
        curr.execute("DELETE FROM internships WHERE id = ?", (internship_id,))
        
        # Log deletion
        now = datetime.utcnow().isoformat()
        curr.execute(
            "INSERT INTO activity_logs (user_id, action, entity_type, entity_id, created_at) VALUES (?, ?, ?, ?, ?)",
            (recruiter_id, "Deleted Internship", "Internship", internship_id, now)
        )
        
        conn.commit()
        conn.close()
        return {"message": "Internship deleted successfully"}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))
