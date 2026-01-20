import sqlite3
import os

db_path = "skillmatch.db" # Corrected from database.py

def migrate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN company VARCHAR")
        print("Added company column to jobs table.")
    except Exception as e:
        print(f"Column 'company' might already exist: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
