import sqlite3

def dump_table(table_name):
    print(f"\n--- {table_name.upper()} ---")
    conn = sqlite3.connect('skillmatch.db')
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    try:
        curr.execute(f"SELECT * FROM {table_name}")
        rows = curr.fetchall()
        if not rows:
            print("Empty table")
        for row in rows:
            print(dict(row))
    except Exception as e:
        print(f"Error: {e}")
    conn.close()

if __name__ == "__main__":
    dump_table("applications")
    dump_table("candidate_profiles")
    dump_table("internships")
    dump_table("users")
