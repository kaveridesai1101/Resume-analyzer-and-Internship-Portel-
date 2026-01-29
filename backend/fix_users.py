import sqlite3

def fix_identities():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    
    print("Pre-fix Roles:")
    curr.execute("SELECT id, email, role FROM users WHERE id IN (1, 2)")
    for row in curr.fetchall():
        print(f" - ID {row[0]}: {row[1]} (Role: {row[2]})")
    
    # 1. Promote User 1 to Recruiter if they are still a candidate
    # This solves the 403 error for 'recruiter_id=1'
    curr.execute("UPDATE users SET role = 'recruiter' WHERE id = 1")
    
    # 2. Add Recruiter Profile for ID 1 if missing
    curr.execute("SELECT id FROM recruiter_profiles WHERE user_id = 1")
    if not curr.fetchone():
        print("Adding Recruiter Profile for User 1...")
        curr.execute(
            "INSERT INTO recruiter_profiles (user_id, organization_name) VALUES (1, 'Neural Career Hub')"
        )
    
    conn.commit()
    
    print("\nPost-fix Roles:")
    curr.execute("SELECT id, email, role FROM users WHERE id IN (1, 2)")
    for row in curr.fetchall():
        print(f" - ID {row[0]}: {row[1]} (Role: {row[2]})")
    
    conn.close()

if __name__ == "__main__":
    fix_identities()
