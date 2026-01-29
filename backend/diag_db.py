import sqlite3
import json

def check_db():
    conn = sqlite3.connect('skillmatch.db')
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    
    print("--- APPLICATIONS ---")
    curr.execute("SELECT * FROM applications")
    rows = curr.fetchall()
    for row in rows:
        print(dict(row))
        
    print("\n--- INTERNSHIPS ---")
    curr.execute("SELECT id, title, recruiter_id FROM internships")
    rows = curr.fetchall()
    for row in rows:
        print(dict(row))
        
    print("\n--- CANDIDATE PROFILES ---")
    curr.execute("SELECT id, user_id, full_name FROM candidate_profiles")
    rows = curr.fetchall()
    for row in rows:
        print(dict(row))
        
    conn.close()

if __name__ == "__main__":
    check_db()
