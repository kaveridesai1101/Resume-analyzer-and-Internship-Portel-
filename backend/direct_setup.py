import sqlite3
from passlib.context import CryptContext

# Match security.py context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto", pbkdf2_sha256__rounds=1000)

def get_hash(password):
    return pwd_context.hash(password)

def setup():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    
    # 1. Clear existing test users to avoid integrity errors
    test_emails = ('student@test.com', 'recruiter@test.com', 'admin@test.com')
    curr.execute("DELETE FROM users WHERE email IN (?, ?, ?)", test_emails)
    
    # 2. Hashed Password
    hashed_pwd = get_hash("password123")
    
    # 3. Insert Users
    users = [
        ('student@test.com', hashed_pwd, 'Kaveri Student', 'candidate', 1),
        ('recruiter@test.com', hashed_pwd, 'Global Tech Corp', 'recruiter', 1),
        ('admin@test.com', hashed_pwd, 'System Administrator', 'admin', 1)
    ]
    
    for u in users:
        print(f"Inserting user: {u[0]}")
        curr.execute("""
            INSERT INTO users (email, hashed_password, full_name, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        """, u)
        user_id = curr.lastrowid
        
        # 4. Insert Profiles
        role = u[3]
        if role == 'candidate':
            curr.execute("DELETE FROM candidate_profiles WHERE user_id = ?", (user_id,))
            curr.execute("INSERT INTO candidate_profiles (user_id, name) VALUES (?, ?)", (user_id, u[2]))
        elif role == 'recruiter':
            curr.execute("DELETE FROM recruiter_profiles WHERE user_id = ?", (user_id,))
            id_code = f"REC-{user_id}"
            curr.execute("""
                INSERT INTO recruiter_profiles (user_id, organization_name, recruiter_id_code)
                VALUES (?, ?, ?)
            """, (user_id, u[2], id_code))
            
    conn.commit()
    conn.close()
    print("Setup done via SQLite.")

if __name__ == "__main__":
    setup()
