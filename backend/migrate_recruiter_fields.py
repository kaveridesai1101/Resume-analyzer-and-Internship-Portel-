import sqlite3

def migrate():
    conn = sqlite3.connect('resume_analyser.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE recruiter_profiles ADD COLUMN industry TEXT")
    except sqlite3.OperationalError:
        print("Column industry already exists")
        
    try:
        cursor.execute("ALTER TABLE recruiter_profiles ADD COLUMN address TEXT")
    except sqlite3.OperationalError:
        print("Column address already exists")
        
    try:
        cursor.execute("ALTER TABLE recruiter_profiles ADD COLUMN contact_role TEXT")
    except sqlite3.OperationalError:
        print("Column contact_role already exists")
        
    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate()
