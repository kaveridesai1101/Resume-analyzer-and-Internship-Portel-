import sqlite3
import json
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_candidate():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    
    # Test credentials
    email = "student@test.com"
    password = "password123"
    full_name = "Test Student"
    
    # Check if user exists
    curr.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing = curr.fetchone()
    
    if existing:
        print(f"✅ User already exists: {email}")
        user_id = existing[0]
    else:
        # Create user
        hashed_password = pwd_context.hash(password)
        curr.execute(
            "INSERT INTO users (email, hashed_password, full_name, role, is_active) VALUES (?, ?, ?, ?, ?)",
            (email, hashed_password, full_name, "candidate", 1)
        )
        user_id = curr.lastrowid
        
        # Create candidate profile
        curr.execute(
            "INSERT INTO candidate_profiles (user_id, name, skills, completeness) VALUES (?, ?, ?, ?)",
            (user_id, full_name, json.dumps(["Python", "JavaScript"]), "Basic")
        )
        
        conn.commit()
        print(f"✅ Created test candidate account")
    
    conn.close()
    
    print(f"\n🔐 Test Credentials:")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Role: candidate")
    print(f"\n📍 Login at: http://localhost:3000/auth/login")

if __name__ == "__main__":
    create_test_candidate()
