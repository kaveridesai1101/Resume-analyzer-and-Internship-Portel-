import sqlite3
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
from app.core.socket import manager

router = APIRouter()

async def notify_recruiter(recruiter_id: int, message: str):
    try:
        await manager.send_personal_message(message, str(recruiter_id))
    except:
        pass

class ApplicationCreate(BaseModel):
    internship_id: int
    student_id: int

@router.post("/")
async def apply_to_internship(
    application: ApplicationCreate, 
    background_tasks: BackgroundTasks
):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        curr.execute("SELECT id, recruiter_id, title FROM internships WHERE id = ?", (application.internship_id,))
        internship = curr.fetchone()
        if not internship:
            conn.close()
            raise HTTPException(status_code=404, detail="Internship not found")
            
        curr.execute("SELECT id, user_id FROM candidate_profiles WHERE user_id = ?", (application.student_id,))
        profile_row = curr.fetchone()
        if not profile_row:
            curr.execute("SELECT id, user_id FROM candidate_profiles WHERE id = ?", (application.student_id,))
            profile_row = curr.fetchone()
            
        if not profile_row:
            conn.close()
            raise HTTPException(status_code=404, detail="User profile not found")
            
        profile_id = profile_row[0]
        student_user_id = profile_row[1]

        curr.execute(
            "SELECT id FROM applications WHERE internship_id = ? AND student_id = ?", 
            (application.internship_id, profile_id)
        )
        existing = curr.fetchone()
        
        match_score = 85 
        now = datetime.utcnow().isoformat()
        
        if existing:
            app_id = existing[0]
            curr.execute(
                """UPDATE applications SET status = 'Applied', match_score = ?, applied_at = ?, updated_at = ? 
                   WHERE id = ?""",
                (match_score, now, now, app_id)
            )
        else:
            curr.execute(
                """INSERT INTO applications (internship_id, student_id, status, match_score, applied_at, updated_at) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (application.internship_id, profile_id, "Applied", match_score, now, now)
            )
            app_id = curr.lastrowid
            
        log_details = json.dumps({"internship_title": internship['title']})
        curr.execute(
            """INSERT INTO activity_logs (user_id, action, entity_type, entity_id, details, created_at) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (student_user_id, "Applied to Internship", "Application", app_id, log_details, now)
        )
        
        conn.commit()
        conn.close()
        
        background_tasks.add_task(
            notify_recruiter, 
            internship['recruiter_id'], 
            f"New application for {internship['title']}"
        )
        
        return {"id": app_id, "status": "Applied", "match_score": match_score}
        
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        print(f"Apply Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_applications(skip: int = 0, limit: int = 100):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        curr.execute("SELECT * FROM applications LIMIT ? OFFSET ?", (limit, skip))
        rows = curr.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/internship/{internship_id}")
def get_internship_applications(internship_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        query = """
            SELECT 
                a.*, 
                cp.name as student_name,
                u.email as student_email,
                cp.skills as student_skills,
                cp.experience as student_experience,
                cp.education as student_education,
                cp.resume_url
            FROM applications a
            JOIN candidate_profiles cp ON a.student_id = cp.id
            JOIN users u ON cp.user_id = u.id
            WHERE a.internship_id = ?
        """
        curr.execute(query, (internship_id,))
        rows = curr.fetchall()
        
        results = []
        for row in rows:
            d = dict(row)
            d['student'] = {
                "name": d['student_name'],
                "email": d['student_email'],
                "skills": json.loads(d['student_skills']) if d['student_skills'] else [],
                "experience": json.loads(d['student_experience']) if d['student_experience'] else [],
                "education": json.loads(d['student_education']) if d['student_education'] else [],
                "resume_url": d['resume_url']
            }
            results.append(d)
            
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recruiter/{recruiter_id}/all")
def get_recruiter_applications(recruiter_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        query = """
            SELECT 
                a.*, 
                i.title as internship_title,
                cp.name as student_name,
                u.email as student_email,
                cp.skills as student_skills,
                cp.resume_url
            FROM applications a
            JOIN internships i ON a.internship_id = i.id
            JOIN candidate_profiles cp ON a.student_id = cp.id
            JOIN users u ON cp.user_id = u.id
            WHERE i.recruiter_id = ?
            ORDER BY a.applied_at DESC
        """
        curr.execute(query, (recruiter_id,))
        rows = curr.fetchall()
        
        results = []
        for row in rows:
            d = dict(row)
            if d['student_skills']:
                try:
                    d['student_skills'] = json.loads(d['student_skills'])
                except:
                    d['student_skills'] = []
            else:
                d['student_skills'] = []
            results.append(d)
            
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
