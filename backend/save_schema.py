import sqlite3

def check_schema():
    with open('schema_check.txt', 'w') as f:
        conn = sqlite3.connect('skillmatch.db')
        cursor = conn.cursor()
        
        f.write("--- candidate_profiles ---\n")
        cursor.execute("PRAGMA table_info(candidate_profiles)")
        for col in cursor.fetchall():
            f.write(f"{col[1]} ({col[2]})\n")
            
        f.write("\n--- activity_logs ---\n")
        cursor.execute("PRAGMA table_info(activity_logs)")
        for col in cursor.fetchall():
            f.write(f"{col[1]} ({col[2]})\n")
            
        conn.close()

if __name__ == "__main__":
    check_schema()
