import sqlite3

def check_schema():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    curr.execute("PRAGMA table_info(internships)")
    columns = curr.fetchall()
    print("Table: internships")
    for col in columns:
        print(f" - {col[1]} ({col[2]})")
    
    curr.execute("PRAGMA table_info(candidate_profiles)")
    columns = curr.fetchall()
    print("\nTable: candidate_profiles")
    for col in columns:
        print(f" - {col[1]} ({col[2]})")
        
    conn.close()

if __name__ == "__main__":
    check_schema()
