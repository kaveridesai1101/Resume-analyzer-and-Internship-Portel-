import sqlite3
import json

def diagnostic():
    conn = sqlite3.connect('skillmatch.db')
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    
    data = {}
    
    # Check users
    curr.execute("SELECT id, email, role FROM users")
    data['users'] = [dict(r) for r in curr.fetchall()]
    
    # Check internships
    curr.execute("SELECT id, title, recruiter_id FROM internships")
    data['internships'] = [dict(r) for r in curr.fetchall()]
    
    # Check applications
    curr.execute("SELECT * FROM applications")
    data['applications'] = [dict(r) for r in curr.fetchall()]
    
    # Check candidate profiles
    curr.execute("SELECT id, user_id, name FROM candidate_profiles")
    data['candidate_profiles'] = [dict(r) for r in curr.fetchall()]
    
    with open('diagnostic_final.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    conn.close()

if __name__ == "__main__":
    diagnostic()
