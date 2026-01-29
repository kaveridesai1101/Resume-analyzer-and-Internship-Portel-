import sqlite3

def check_schema():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    
    tables = ['applications', 'internships', 'candidate_profiles', 'users']
    for table in tables:
        print(f"\n--- Schema for {table} ---")
        try:
            curr.execute(f"PRAGMA table_info({table})")
            for row in curr.fetchall():
                print(row)
        except Exception as e:
            print(f"Error checking {table}: {e}")
            
    conn.close()

if __name__ == "__main__":
    check_schema()
