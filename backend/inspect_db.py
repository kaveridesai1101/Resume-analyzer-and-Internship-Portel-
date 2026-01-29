from app.database import SessionLocal
from app.models.all_models import Internship, StudentProfile, User

db = SessionLocal()

print("--- USERS ---")
users = db.query(User).all()
for u in users:
    print(f"ID: {u.id}, Name: {u.full_name}, Email: {u.email}, Role: {u.role}")

print("\n--- CANDIDATE PROFILES ---")
profiles = db.query(StudentProfile).all()
for p in profiles:
    print(f"ID: {p.id}, UserID: {p.user_id}, Name: {p.name}, Score: {p.latest_score}, Skills: {p.skills}")

print("\n--- JOBS ---")
internships = db.query(Internship).all()
for j in internships:
    print(f"ID: {j.id}, Title: {j.title}, RecruiterID: {j.recruiter_id}, Active: {j.is_active}, Skills: {j.required_skills}")
