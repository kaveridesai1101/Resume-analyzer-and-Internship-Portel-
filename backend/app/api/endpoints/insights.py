from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/market-trends")
def get_market_trends() -> List[Dict[str, Any]]:
    # In a real app, this would aggregate job data
    return [
        {"role": "Frontend", "demand": 85, "growth": "+12%"},
        {"role": "Backend", "demand": 92, "growth": "+15%"},
        {"role": "Full Stack", "demand": 78, "growth": "+8%"},
        {"role": "ML Engineer", "demand": 95, "growth": "+25%"},
    ]

@router.get("/salary-data")
def get_salary_data() -> List[Dict[str, Any]]:
    return [
        {"role": "Junior", "salary": 60000},
        {"role": "Mid-Level", "salary": 95000},
        {"role": "Senior", "salary": 140000},
        {"role": "Lead", "salary": 180000},
    ]

@router.get("/top-skills")
def get_top_skills() -> List[Dict[str, Any]]:
    return [
        {"name": "React", "count": 120},
        {"name": "Python", "count": 115},
        {"name": "AWS", "count": 90},
        {"name": "TypeScript", "count": 85},
    ]
