from app.database import SessionLocal
from app.models.all_models import Job, User
from datetime import datetime
import random

def seed_jobs():
    db = SessionLocal()
    # Find a recruiter to assign jobs to
    recruiter = db.query(User).filter(User.role == 'recruiter').first()
    if not recruiter:
        # Create a mock recruiter if none exists
        recruiter = User(email="recruiter@example.com", full_name="John Recruiter", role="recruiter")
        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

    jobs = [
        {
            "title": "Backend Developer (Python/FastAPI)",
            "company": "DataStream Solutions",
            "location": "Ahmadabad, India",
            "salary": "₹12L - ₹18L",
            "description": "We are looking for a Python expert to build scalable APIs using FastAPI.",
            "requirements": "Python, FastAPI, PostgreSQL, Redis",
            "skills": "Python, FastAPI, PostgreSQL, Redis, Docker"
        },
        {
            "title": "Frontend React Engineer",
            "company": "PixelPerfect UI",
            "location": "Bangalore, India",
            "salary": "₹15L - ₹22L",
            "description": "Join our team to build beautiful, responsive user interfaces with React and Tailwind CSS.",
            "requirements": "React, TypeScript, Tailwind CSS, Next.js",
            "skills": "React, TypeScript, Tailwind CSS, Next.js, Framer Motion"
        },
        {
            "title": "Full Stack Developer",
            "company": "InnovateHub",
            "location": "Remote",
            "salary": "₹10L - ₹15L",
            "description": "Looking for a versatile developer who can handle both frontend and backend tasks.",
            "requirements": "React, Node.js, Express, MongoDB",
            "skills": "React, Node.js, Express, MongoDB, AWS"
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudNative Systems",
            "location": "Mumbai, India",
            "salary": "₹18L - ₹25L",
            "description": "Help us automate our infrastructure and deployment pipelines.",
            "requirements": "AWS, Kubernetes, Terraform, CI/CD",
            "skills": "AWS, Kubernetes, Terraform, CI/CD, Jenkins"
        },
        {
            "title": "Data Scientist",
            "company": "Insightful AI",
            "location": "Pune, India",
            "salary": "₹20L - ₹30L",
            "description": "Analyze large datasets and build predictive models to drive business decisions.",
            "requirements": "Python, Scikit-learn, Pandas, TensorFlow",
            "skills": "Python, Scikit-learn, Pandas, TensorFlow, SQL"
        },
        {
            "title": "UI/UX Designer",
            "company": "CreativeMinds",
            "location": "Ahmadabad, India",
            "salary": "₹8L - ₹12L",
            "description": "Design intuitive and visually appealing user experiences for web and mobile apps.",
            "requirements": "Figma, Adobe XD, User Research, Prototyping",
            "skills": "Figma, Adobe XD, User Research, Prototyping, CSS"
        },
        {
            "title": "Mobile App Developer (Flutter)",
            "company": "AppForge",
            "location": "Remote",
            "salary": "₹12L - ₹17L",
            "description": "Build high-performance cross-platform mobile apps using Flutter.",
            "requirements": "Flutter, Dart, Firebase, State Management",
            "skills": "Flutter, Dart, Firebase, State Management, REST APIs"
        }
    ]

    for job_data in jobs:
        existing = db.query(Job).filter(Job.title == job_data["title"], Job.company == job_data["company"]).first()
        if not existing:
            job = Job(
                recruiter_id=recruiter.id,
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                salary_range=job_data["salary"],
                description=job_data["description"],
                required_skills=job_data["skills"].split(", "),
                created_at=datetime.utcnow()
            )
            db.add(job)
    
    db.commit()
    print("Seeded 7 additional jobs.")
    db.close()

if __name__ == "__main__":
    seed_jobs()
