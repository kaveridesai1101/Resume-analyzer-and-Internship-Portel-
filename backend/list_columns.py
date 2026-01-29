import sqlite3

def check_schema():
    conn = sqlite3.connect('skillmatch.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(candidate_profiles)")
    columns = cursor.fetchall()
    names = [col[1] for col in columns]
    print("COLUMNS: " + ", ".join(names))
    conn.close()

if __name__ == "__main__":
    check_schema()
