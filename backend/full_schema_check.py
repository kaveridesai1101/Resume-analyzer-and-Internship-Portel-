import sqlite3

def check_schema():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    curr.execute("PRAGMA table_info(internships)")
    columns = curr.fetchall()
    print("Columns in internships:")
    for col in columns:
        print(f"ID: {col[0]}, Name: {col[1]}, Type: {col[2]}")
    conn.close()

if __name__ == "__main__":
    check_schema()
