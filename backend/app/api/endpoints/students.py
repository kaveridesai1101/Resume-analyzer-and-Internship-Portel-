from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import CandidateProfile, User
from app.schemas.all import StudentCreate, StudentResponse, StudentUpdate
from app.core.security import get_current_user

router = APIRouter()

import sqlite3
import json

@router.get("/me/stats")
async def get_my_stats(current_user: any = Depends(get_current_user)):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        # Get candidate profile
        curr.execute("SELECT id, skills, latest_score FROM candidate_profiles WHERE user_id = ?", (current_user.id,))
        profile = curr.fetchone()
        
        if not profile:
            conn.close()
            return {
                "resume_score": 0,
                "total_applications": 0,
                "total_matches": 0,
                "skills_count": 0
            }
        
        profile_id = profile['id']
        skills = json.loads(profile['skills']) if profile['skills'] else []
        
        # Count applications
        curr.execute("SELECT COUNT(*) FROM applications WHERE student_id = ?", (profile_id,))
        app_count = curr.fetchone()[0]
        
        # Count matches
        curr.execute("SELECT COUNT(*) FROM internships") 
        match_count = curr.fetchone()[0]
        
        conn.close()
        return {
            "resume_score": profile['latest_score'] or 0,
            "total_applications": app_count,
            "total_matches": match_count,
            "skills_count": len(skills)
        }
    except Exception as e:
        print(f"Stats Error: {e}")
        return {"resume_score": 0, "total_applications": 0, "total_matches": 0, "skills_count": 0}

@router.get("/me/applications")
async def get_my_applications(current_user: any = Depends(get_current_user)):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        # Get candidate profile ID
        curr.execute("SELECT id FROM candidate_profiles WHERE user_id = ?", (current_user.id,))
        profile = curr.fetchone()
        if not profile:
            conn.close()
            return []
            
        profile_id = profile['id']
        
        # Fetch applications with internship details
        query = """
            SELECT a.*, i.title as internship_title, i.company as company
            FROM applications a
            JOIN internships i ON a.internship_id = i.id
            WHERE a.student_id = ?
            ORDER BY a.applied_at DESC
        """
        curr.execute(query, (profile_id,))
        rows = curr.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            d = dict(row)
            # Map status
            status_map = {
                "Applied": "pending",
                "Shortlisted": "accepted",
                "Interview Call": "under_review",
                "Rejected": "rejected"
            }
            d['status'] = status_map.get(row['status'], "pending")
            d['internship'] = {
                "title": row['internship_title'],
                "company": row['company'] or "TalentMatch AI"
            }
            d['created_at'] = row['applied_at']
            results.append(d)
        return results
    except Exception as e:
        print(f"My Apps Error: {e}")
        return []

@router.get("/me/matches")
async def get_my_matches(current_user: any = Depends(get_current_user)):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        curr.execute("SELECT id, title, company as company FROM internships LIMIT 5")
        rows = curr.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                "id": row['id'],
                "title": row['title'],
                "company": row['company'] or "TalentMatch AI",
                "match_score": 85
            })
        return results
    except Exception as e:
        print(f"Matches Error: {e}")
        return []

@router.get("/{user_id}")
def get_student_profile(user_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        curr.execute("SELECT * FROM candidate_profiles WHERE user_id = ?", (user_id,))
        row = curr.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        data = dict(row)
        data['skills'] = json.loads(data['skills']) if data['skills'] else []
        data['experience'] = json.loads(data['experience']) if data['experience'] else []
        data['education'] = json.loads(data['education']) if data['education'] else []
        data['improvement_tips'] = json.loads(data['improvement_tips']) if data['improvement_tips'] else []
        
        return data
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/applications")
def get_student_applications(user_id: int):
    try:
        conn = sqlite3.connect('skillmatch.db')
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        
        curr.execute("SELECT id FROM candidate_profiles WHERE user_id = ?", (user_id,))
        profile_row = curr.fetchone()
        if not profile_row:
            conn.close()
            return []
            
        student_id = profile_row[0]
        
        query = """
            SELECT a.id, i.title as internship_title, i.company, a.applied_at, a.status, a.match_score
            FROM applications a
            JOIN internships i ON a.internship_id = i.id
            WHERE a.student_id = ?
        """
        curr.execute(query, (student_id,))
        rows = curr.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                "id": row['id'],
                "internship_title": row['internship_title'],
                "role": row['internship_title'],
                "company": row['company'] or "Organization",
                "applied_at": row['applied_at'],
                "status": row['status'],
                "match_score": row['match_score']
            })
        return results
    except Exception as e:
        print(f"Students API Error: {e}")
        return []

@router.put("/{user_id}")
def update_student_profile(user_id: int, data: dict):
    try:
        conn = sqlite3.connect('skillmatch.db')
        curr = conn.cursor()
        
        if "full_name" in data:
            curr.execute("UPDATE users SET full_name = ? WHERE id = ?", (data["full_name"], user_id))
            
        curr.execute("SELECT id FROM candidate_profiles WHERE user_id = ?", (user_id,))
        profile_row = curr.fetchone()
        
        if profile_row:
            updates = []
            params = []
            if "phone" in data:
                updates.append("phone = ?")
                params.append(data["phone"])
            if "address" in data:
                updates.append("address = ?")
                params.append(data["address"])
            
            if updates:
                params.append(user_id)
                query = f"UPDATE candidate_profiles SET {', '.join(updates)} WHERE user_id = ?"
                curr.execute(query, params)
        
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
