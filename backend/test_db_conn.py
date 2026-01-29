import sqlite3
import time

def test_db():
    print("Testing DB connection...")
    try:
        conn = sqlite3.connect('skillmatch.db', timeout=5)
        curr = conn.cursor()
        curr.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = curr.fetchall()
        print(f"Tables: {tables}")
        conn.close()
        print("DB Connection OK")
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == "__main__":
    test_db()
