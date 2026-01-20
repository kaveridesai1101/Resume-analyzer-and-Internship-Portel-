from app.database import SessionLocal
from app.models.all_models import Job, User
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

print(f"Adding job for Recruiter ID: {recruiter.id}")

test_job = Job(
    recruiter_id=recruiter.id,
    title="Test Job for Visibility",
    company="Visibility Check Inc.",
    description="This is a test job to verify candidate dashboard visibility. It requires basic skills.",
    location="Remote",
    salary_range="$50k - $80k",
    required_skills=["Python", "Communication", "Teamwork"], # Generic skills
    is_active=True,
    created_at=datetime.utcnow()
)

db.add(test_job)
db.commit()
db.refresh(test_job)

print(f"Created Job ID: {test_job.id} | Title: {test_job.title} | Skills: {test_job.required_skills}")
