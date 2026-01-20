import sqlite3
import os

db_path = "skillmatch.db"
if not os.path.exists(db_path):
    print(f"Database {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check columns
    cursor.execute("PRAGMA table_info(candidate_profiles);")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Current columns in candidate_profiles: {columns}")
    
    new_columns = [
        ("latest_score", "INTEGER"),
        ("last_analyzed", "DATETIME"),
        ("completeness", "TEXT DEFAULT 'Awaiting Resume'")
    ]
    
    for col_name, col_type in new_columns:
        if col_name not in columns:
            try:
                print(f"Adding column {col_name} to candidate_profiles...")
                cursor.execute(f"ALTER TABLE candidate_profiles ADD COLUMN {col_name} {col_type};")
                print(f"Successfully added {col_name}")
            except Exception as e:
                print(f"Error adding {col_name}: {e}")
        else:
            print(f"Column {col_name} already exists.")
            
    conn.commit()
    conn.close()
    print("Database check complete.")
