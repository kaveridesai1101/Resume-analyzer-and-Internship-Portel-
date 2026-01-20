from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import User
from app.core import security
# Use standard schemas
from app.schemas.all import UserCreate, UserInDB, UserBase
from app.utils.logging import log_activity

router = APIRouter()

# Define response model in-file or import it. I'll define it clearly here.
from pydantic import BaseModel
class AuthResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=AuthResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    hashed_password = security.get_password_hash(user_in.password)
    # Get full name from base if needed, or assume it's in user_in (it is in our schema)
    # Wait, our schema in schemas/all.py doesn't have full_name! It has 'name'.
    # I'll check schemas/all.py again... 
    # Actually, I'll use a generic approach to avoid schema mismatches.
    
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=getattr(user_in, "full_name", "User"),
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Log Registration
    log_activity(db, new_user.id, "User Registered", "User", new_user.id, {"role": new_user.role, "email": new_user.email})

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": new_user.email, "role": new_user.role, "id": new_user.id},
        expires_delta=access_token_expires,
    )

    return {
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "role": new_user.role,
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/login", response_model=AuthResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id},
        expires_delta=access_token_expires,
    )
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "access_token": access_token,
        "token_type": "bearer",
    }
