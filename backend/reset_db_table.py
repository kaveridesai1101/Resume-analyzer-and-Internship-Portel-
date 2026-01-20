from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL

# Adjust URL for direct script usage if needed, or assume app package is resolvable
# app.database uses "sqlite:///./sql_app.db" (typically)

if __name__ == "__main__":
    db_url = "sqlite:///./skillmatch.db" # Correct DB file matching database.py
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("Dropping tables...")
        conn.execute(text("DROP TABLE IF EXISTS activity_logs"))
        conn.execute(text("DROP TABLE IF EXISTS applications"))
        print("Dropped.")
