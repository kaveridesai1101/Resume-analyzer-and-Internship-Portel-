import sqlite3
import json

db_path = 'skillmatch.db'

def check_visibility():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    
    print("--- Recruiter Info ---")
    curr.execute("SELECT id, email, full_name role FROM users WHERE email = 'recruiter@test.com'")
    recruiter = curr.fetchone()
    if recruiter:
        print(dict(recruiter))
        r_id = recruiter['id']
    else:
        print("Recruiter not found")
        return

    print("\n--- Internships for this Recruiter ---")
    curr.execute("SELECT id, title FROM internships WHERE recruiter_id = ?", (r_id,))
    jobs = curr.fetchall()
    job_ids = [j['id'] for j in jobs]
    for j in jobs:
        print(dict(j))

    print("\n--- Applications in DB ---")
    curr.execute("SELECT * FROM applications")
    apps = curr.fetchall()
    for a in apps:
        print(dict(a))

    print("\n--- Applications for this Recruiter's Jobs ---")
    if job_ids:
        query = f"SELECT * FROM applications WHERE job_id IN ({','.join(['?']*len(job_ids))})"
        curr.execute(query, job_ids)
        r_apps = curr.fetchall()
        for ra in r_apps:
            print(dict(ra))
    else:
        print("No jobs found for this recruiter")

    conn.close()

if __name__ == "__main__":
    check_visibility()
