import sqlite3

def check_schema():
    conn = sqlite3.connect('skillmatch.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(candidate_profiles)")
    columns = cursor.fetchall()
    print("Columns in candidate_profiles:")
    for col in columns:
        print(f"Index: {col[0]}, Name: {col[1]}, Type: {col[2]}")
    conn.close()

if __name__ == "__main__":
    check_schema()
