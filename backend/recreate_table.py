import sqlite3
from app.database import engine
from app.models.all_models import Base

def reset_applications_table():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    
    print("Dropping applications table...")
    curr.execute("DROP TABLE IF EXISTS applications")
    conn.commit()
    conn.close()
    
    print("Recreating table from models...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

    # Verify
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    curr.execute("PRAGMA table_info(applications)")
    print("\nNew Schema:")
    for row in curr.fetchall():
        print(row)
    conn.close()

if __name__ == "__main__":
    reset_applications_table()
