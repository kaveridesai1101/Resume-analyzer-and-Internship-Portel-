import sqlite3
import json
from datetime import datetime

def add_internships():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    
    # Recruiter ID is 2 for recruiter@test.com based on previous check
    recruiter_id = 2
    now = datetime.utcnow().isoformat()
    
    internships = [
        (
            recruiter_id, "Frontend Developer Intern", "Global Tech Corp", "Remote", 
            "Design and build beautiful user interfaces using React and Tailwind. You will work on production systems and learn modern frontend practices.",
            json.dumps(["React", "TypeScript", "Tailwind CSS"]), "3 Months", "₹15,000 / month", 
            "Internship", "Remote", "B.Tech/B.CA Students with React knowledge", "2026-03-01", now, 1, 'Active'
        ),
        (
            recruiter_id, "UI/UX Designer", "Global Tech Corp", "Bangalore / Hybrid", 
            "Create stunning wireframes and high-fidelity mockups. Focus on user-centric design and accessibility.",
            json.dumps(["Figma", "Adobe XD", "User Research"]), "6 Months", "₹20,000 / month", 
            "Internship", "Hybrid", "Design students or portfolio holders", "2026-02-15", now, 1, 'Active'
        ),
        (
            recruiter_id, "Backend API Intern", "Global Tech Corp", "Remote", 
            "Scale our backend systems using Python and FastAPI. Learn about database optimization and real-time processing.",
            json.dumps(["Python", "FastAPI", "PostgreSQL"]), "4 Months", "₹18,000 / month", 
            "Internship", "Remote", "CS Students with Python experience", "2026-04-10", now, 1, 'Active'
        )
    ]
    
    curr.executemany(
        """INSERT INTO internships 
           (recruiter_id, title, organization, location, description, required_skills, duration, stipend_salary, internship_type, mode, eligibility_criteria, deadline, created_at, is_active, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        internships
    )
    
    conn.commit()
    conn.close()
    print("Added 3 internships for recruiter@test.com")

if __name__ == "__main__":
    add_internships()
