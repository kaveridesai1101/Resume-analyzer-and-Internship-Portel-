import requests
import sqlite3

def test_patch_status():
    # 1. Get an existing application ID
    conn = sqlite3.connect('skillmatch.db')
    curr = conn.cursor()
    curr.execute("SELECT id FROM applications LIMIT 1")
    row = curr.fetchone()
    conn.close()
    
    if not row:
        print("No applications found to test.")
        return

    app_id = row[0]
    print(f"Testing PATCH status for App ID: {app_id}")
    
    url = f"http://localhost:8000/api/v1/applications/{app_id}/status"
    payload = {"status": "Shortlisted"}
    
    try:
        response = requests.patch(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_patch_status()
