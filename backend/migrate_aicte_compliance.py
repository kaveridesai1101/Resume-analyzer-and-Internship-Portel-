"""
AICTE Compliance Migration Script
Renames tables and columns to match AICTE Internship Portal terminology
"""
import sqlite3
from pathlib import Path

def migrate_to_aicte_compliance():
    db_path = Path(__file__).parent / "resume_analyzer.db"
    
    if not db_path.exists():
        print("Database not found. Will be created with new schema on first run.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Starting AICTE compliance migration...")
        
        # Step 1: Rename jobs table to internships
        print("1. Renaming 'jobs' table to 'internships'...")
        cursor.execute("ALTER TABLE jobs RENAME TO internships;")
        
        # Step 2: Rename columns in internships table
        print("2. Renaming columns in 'internships' table...")
        cursor.execute("""
            CREATE TABLE internships_new (
                id INTEGER PRIMARY KEY,
                recruiter_id INTEGER,
                title VARCHAR,
                organization VARCHAR DEFAULT 'Organization Name',
                description VARCHAR,
                internship_type VARCHAR,
                mode VARCHAR,
                duration VARCHAR,
                stipend_salary VARCHAR,
                eligibility_criteria VARCHAR,
                required_skills JSON,
                location VARCHAR,
                deadline DATETIME,
                created_at DATETIME,
                is_active BOOLEAN DEFAULT 1,
                status VARCHAR DEFAULT 'Active',
                FOREIGN KEY (recruiter_id) REFERENCES users(id)
            );
        """)
        
        cursor.execute("""
            INSERT INTO internships_new 
            SELECT id, recruiter_id, title, company, description, job_type, mode, 
                   duration, stipend_salary, eligibility_criteria, required_skills, 
                   location, deadline, created_at, is_active, status
            FROM internships;
        """)
        
        cursor.execute("DROP TABLE internships;")
        cursor.execute("ALTER TABLE internships_new RENAME TO internships;")
        
        # Step 3: Update applications table
        print("3. Updating 'applications' table columns...")
        cursor.execute("""
            CREATE TABLE applications_new (
                id INTEGER PRIMARY KEY,
                internship_id INTEGER,
                student_id INTEGER,
                status VARCHAR DEFAULT 'Applied',
                match_score INTEGER,
                recruiter_notes VARCHAR,
                interview_date DATETIME,
                interview_mode VARCHAR,
                feedback VARCHAR,
                applied_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY (internship_id) REFERENCES internships(id),
                FOREIGN KEY (student_id) REFERENCES candidate_profiles(id)
            );
        """)
        
        cursor.execute("""
            INSERT INTO applications_new 
            SELECT id, job_id, candidate_id, status, match_score, recruiter_notes,
                   interview_date, interview_mode, feedback, applied_at, updated_at
            FROM applications;
        """)
        
        cursor.execute("DROP TABLE applications;")
        cursor.execute("ALTER TABLE applications_new RENAME TO applications;")
        
        # Step 4: Remove non-AICTE fields from recruiter_profiles
        print("4. Removing non-AICTE fields from 'recruiter_profiles'...")
        cursor.execute("""
            CREATE TABLE recruiter_profiles_new (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                organization_name VARCHAR,
                recruiter_id_code VARCHAR UNIQUE,
                verification_status VARCHAR DEFAULT 'Pending',
                contact_email VARCHAR,
                account_status VARCHAR DEFAULT 'Active',
                created_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        
        cursor.execute("""
            INSERT INTO recruiter_profiles_new 
            SELECT id, user_id, organization_name, recruiter_id_code, 
                   verification_status, contact_email, account_status, created_at
            FROM recruiter_profiles;
        """)
        
        cursor.execute("DROP TABLE recruiter_profiles;")
        cursor.execute("ALTER TABLE recruiter_profiles_new RENAME TO recruiter_profiles;")
        
        conn.commit()
        print("\n✅ AICTE compliance migration completed successfully!")
        print("   - jobs → internships")
        print("   - company → organization")
        print("   - job_type → internship_type")
        print("   - job_id → internship_id")
        print("   - candidate_id → student_id")
        print("   - Removed: industry, address, contact_role from recruiter_profiles")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        print("Rolling back changes...")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_to_aicte_compliance()
