from app.database import SessionLocal
from app.models.all_models import User, CandidateProfile

db = SessionLocal()
users = db.query(User).all()
profiles = db.query(CandidateProfile).all()

print(f"Total Users: {len(users)}")
for u in users:
    print(f"User ID: {u.id}, Email: {u.email}, Role: {u.role}")

print(f"\nTotal Profiles: {len(profiles)}")
for p in profiles:
    print(f"Profile ID: {p.id}, User ID: {p.user_id}, Score: {p.latest_score}, Completeness: {p.completeness}")

db.close()
