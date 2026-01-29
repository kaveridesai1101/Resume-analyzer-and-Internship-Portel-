import sqlite3

def check_resumes():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    curr.execute("SELECT id, name, resume_url FROM candidate_profiles")
    rows = curr.fetchall()
    print("Candidate Resumes:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, URL: {row[2]}")
    conn.close()

if __name__ == "__main__":
    check_resumes()
