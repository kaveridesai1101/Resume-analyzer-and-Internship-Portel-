from app.database import SessionLocal
from app.models.all_models import Internship, User
from datetime import datetime

db = SessionLocal()

# Find a recruiter
recruiter = db.query(User).filter(User.role == "recruiter").first()
if not recruiter:
    print("No recruiter found. Creating one.")
    # In a real scenario we'd hash password etc, but for test:
    recruiter = User(email="testrecruiter@example.com", hashed_password="hashed_secret", role="recruiter", full_name="Test Recruiter")
    db.add(recruiter)
    db.commit()

print(f"Adding internship for Recruiter ID: {recruiter.id}")

test_internship = Internship(
    recruiter_id=recruiter.id,
    title="Test Internship for Visibility",
    company="Visibility Check Inc.",
    description="This is a test internship to verify student dashboard visibility. It requires basic skills.",
    location="Remote",
    salary_range="$50k - $80k",
    required_skills=["Python", "Communication", "Teamwork"], # Generic skills
    is_active=True,
    created_at=datetime.utcnow()
)

db.add(test_internship)
db.commit()
db.refresh(test_internship)

print(f"Created Internship ID: {test_internship.id} | Title: {test_internship.title} | Skills: {test_internship.required_skills}")
