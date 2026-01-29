import sqlite3

def fix_resumes():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    
    # Prepend /uploads/ if it doesn't already have it and isn't null
    curr.execute("""
        UPDATE candidate_profiles 
        SET resume_url = '/uploads/' || resume_url 
        WHERE resume_url IS NOT NULL 
        AND resume_url != '' 
        AND resume_url NOT LIKE '/uploads/%'
        AND resume_url NOT LIKE 'http%'
    """)
    
    print(f"Updated {curr.rowcount} resume URLs.")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_resumes()
