from datetime import datetime, timedelta
import traceback
import json
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import User
from app.core import security
# Use standard schemas
from app.schemas.all import UserCreate, UserInDB, UserBase, StudentCreate, RecruiterProfileCreate
from app.models.all_models import CandidateProfile, RecruiterProfile
from app.utils.logging import log_activity

router = APIRouter()

# Define response model in-file or import it. I'll define it clearly here.
from pydantic import BaseModel, EmailStr
class AuthResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    role: str
    access_token: str
    token_type: str = "bearer"

class StudentRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    skills: Optional[str] = None
    experience_years: Optional[int] = 0

class RecruiterRegisterRequest(BaseModel):
    company_name: str
    email: EmailStr
    password: str
    location: Optional[str] = "Not Specified"

from sqlalchemy import text

import sqlite3

@router.post("/register/student", response_model=AuthResponse)
def register_student(user_in: StudentRegisterRequest):
    hashed_password = security.get_password_hash(user_in.password)
    try:
        conn = sqlite3.connect('skillmatch.db')
        curr = conn.cursor()
        
        # Email Check
        curr.execute("SELECT id FROM users WHERE email = ?", (user_in.email,))
        if curr.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Insert User
        curr.execute(
            "INSERT INTO users (email, hashed_password, full_name, role) VALUES (?, ?, ?, ?)",
            (user_in.email, hashed_password, user_in.full_name, "student")
        )
        user_id = curr.lastrowid
        
        # Create Profile
        skills_json = json.dumps(user_in.skills.split(",") if user_in.skills else [])
        curr.execute(
            "INSERT INTO candidate_profiles (user_id, name, skills) VALUES (?, ?, ?)",
            (user_id, user_in.full_name, skills_json)
        )
        
        # Log Activity (Raw)
        log_details = json.dumps({"action": "Registration"})
        curr.execute(
            "INSERT INTO activity_logs (user_id, action, entity_type, entity_id, details, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, "Student Registered", "User", user_id, log_details, datetime.utcnow())
        )
        
        conn.commit()
        conn.close()
        
        access_token = security.create_access_token(data={"sub": user_in.email, "role": "student", "id": user_id})
        return {
            "id": user_id,
            "email": user_in.email,
            "full_name": user_in.full_name,
            "role": "student",
            "access_token": access_token,
            "token_type": "bearer",
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register/recruiter", response_model=AuthResponse)
def register_recruiter(user_in: RecruiterRegisterRequest):
    hashed_password = security.get_password_hash(user_in.password)
    try:
        conn = sqlite3.connect('skillmatch.db')
        curr = conn.cursor()
        
        curr.execute("SELECT id FROM users WHERE email = ?", (user_in.email,))
        if curr.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="User already exists")
        
        curr.execute(
            "INSERT INTO users (email, hashed_password, full_name, role) VALUES (?, ?, ?, ?)",
            (user_in.email, hashed_password, user_in.company_name, "recruiter")
        )
        user_id = curr.lastrowid
        
        curr.execute(
            "INSERT INTO recruiter_profiles (user_id, organization_name) VALUES (?, ?)",
            (user_id, user_in.company_name)
        )
        
        # Log Activity (Raw)
        curr.execute(
            "INSERT INTO activity_logs (user_id, action, entity_type, entity_id, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, "Recruiter Registered", "User", user_id, datetime.utcnow())
        )
        
        conn.commit()
        conn.close()
        
        access_token = security.create_access_token(data={"sub": user_in.email, "role": "recruiter", "id": user_id})
        return {
            "id": user_id,
            "email": user_in.email,
            "full_name": user_in.company_name,
            "role": "recruiter",
            "access_token": access_token,
            "token_type": "bearer",
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(login_data: LoginRequest):
    try:
        conn = sqlite3.connect('skillmatch.db')
        curr = conn.cursor()
        
        curr.execute(
            "SELECT id, email, hashed_password, full_name, role FROM users WHERE email = ?", 
            (login_data.username,)
        )
        user_row = curr.fetchone()
        conn.close()
        
        if not user_row or not security.verify_password(login_data.password, user_row[2]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id, email, hashed_pwd, full_name, role = user_row
        
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": email, "role": role, "id": user_id},
            expires_delta=access_token_expires,
        )
        
        return {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "role": role,
            "access_token": access_token,
            "token_type": "bearer",
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        print(f"CRASH IN LOGIN: {e}")
        raise HTTPException(status_code=500, detail=str(e))
