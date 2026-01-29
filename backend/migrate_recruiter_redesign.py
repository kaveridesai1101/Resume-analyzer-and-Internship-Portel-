import sqlite3
import os

db_path = "skillmatch.db"
if not os.path.exists(db_path):
    print(f"Database {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create recruiter_profiles table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recruiter_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        organization_name TEXT,
        recruiter_id_code TEXT UNIQUE,
        verification_status TEXT DEFAULT 'Pending',
        contact_email TEXT,
        account_status TEXT DEFAULT 'Active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)
    print("Checked/Created recruiter_profiles table.")

    # 2. Update candidate_profiles
    cursor.execute("PRAGMA table_info(candidate_profiles);")
    candidate_cols = [col[1] for col in cursor.fetchall()]
    for col_name, col_type in [("phone", "TEXT"), ("address", "TEXT")]:
        if col_name not in candidate_cols:
            cursor.execute(f"ALTER TABLE candidate_profiles ADD COLUMN {col_name} {col_type};")
            print(f"Added column {col_name} to candidate_profiles.")

    # 3. Update jobs
    cursor.execute("PRAGMA table_info(jobs);")
    job_cols = [col[1] for col in cursor.fetchall()]
    job_updates = [
        ("job_type", "TEXT DEFAULT 'Internship'"),
        ("mode", "TEXT DEFAULT 'Office'"),
        ("duration", "TEXT DEFAULT '3 Months'"),
        ("stipend_salary", "TEXT DEFAULT 'Unpaid'"),
        ("eligibility_criteria", "TEXT"),
        ("deadline", "DATETIME"),
        ("status", "TEXT DEFAULT 'Active'")
    ]
    for col_name, col_type in job_updates:
        if col_name not in job_cols:
            cursor.execute(f"ALTER TABLE jobs ADD COLUMN {col_name} {col_type};")
            print(f"Added column {col_name} to jobs.")

    # 4. Update applications
    cursor.execute("PRAGMA table_info(applications);")
    app_cols = [col[1] for col in cursor.fetchall()]
    for col_name, col_type in [("interview_date", "DATETIME"), ("interview_mode", "TEXT")]:
        if col_name not in app_cols:
            cursor.execute(f"ALTER TABLE applications ADD COLUMN {col_name} {col_type};")
            print(f"Added column {col_name} to applications.")

    conn.commit()
    conn.close()
    print("Migration complete.")
