from app.database import SessionLocal
from app.models.all_models import User, CandidateProfile

db = SessionLocal()
user = db.query(User).filter(User.id == 1).first()
if user:
    print(f"User: {user.email} (ID: {user.id})")
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()
    if profile:
        print(f"Profile found: ID {profile.id}")
        print(f"Score: {profile.latest_score}")
        print(f"Completeness: {profile.completeness}")
        print(f"Skills: {profile.skills}")
    else:
        print("No profile found for this user.")
else:
    print("User 1 not found.")
db.close()
