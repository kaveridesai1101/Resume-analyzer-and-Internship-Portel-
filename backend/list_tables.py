import sqlite3

def list_tables():
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    curr.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = curr.fetchall()
    print("TABLES: " + ", ".join([t[0] for t in tables]))
    conn.close()

if __name__ == "__main__":
    list_tables()
