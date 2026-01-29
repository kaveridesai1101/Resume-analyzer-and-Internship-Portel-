import sqlite3
import os

db_path = 'skillmatch.db'
if not os.path.exists(db_path):
    print("Database not found")
else:
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    
    print("--- Users ---")
    curr.execute("SELECT id, email, role FROM users")
    for row in curr.fetchall():
        print(row)
        
    print("\n--- Internships ---")
    curr.execute("SELECT id, recruiter_id, title FROM internships")
    for row in curr.fetchall():
        print(row)
    
    conn.close()
