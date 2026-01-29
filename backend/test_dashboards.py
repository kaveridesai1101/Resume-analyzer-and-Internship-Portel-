
import requests
import json

API_BASE = "http://127.0.0.1:8000/api/v1"

def test_dashboards():
    print("Verifying Dashboard Endpoints...")
    
    # login as student
    print("\nLogging in as student...")
    login_resp = requests.post(f"{API_BASE}/auth/login", json={"username": "student@test.com", "password": "password123"})
    if login_resp.status_code == 200:
        token = login_resp.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test student stats
        print("Testing student stats...")
        resp = requests.get(f"{API_BASE}/students/me/stats", headers=headers)
        print(f"Stats: {resp.status_code} - {resp.json()}")
        
        # Test student applications
        print("Testing student applications...")
        resp = requests.get(f"{API_BASE}/students/me/applications", headers=headers)
        apps = resp.json()
        print(f"Applications count: {len(apps)}")
        if len(apps) > 0:
            print(f"Sample app status: {apps[0]['status']}")
            
        # Test student matches
        print("Testing student matches...")
        resp = requests.get(f"{API_BASE}/students/me/matches", headers=headers)
        print(f"Matches count: {len(resp.json())}")
    else:
        print(f"Student login failed: {login_resp.status_code} - {login_resp.text}")

    # login as recruiter
    print("\nLogging in as recruiter...")
    login_resp = requests.post(f"{API_BASE}/auth/login", json={"username": "recruiter@test.com", "password": "password123"})
    if login_resp.status_code == 200:
        token = login_resp.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test recruiter stats
        print("Testing recruiter stats...")
        resp = requests.get(f"{API_BASE}/recruiters/me/stats", headers=headers)
        print(f"Stats: {resp.status_code} - {resp.json()}")
        
        # Test recruiter applications
        print("Testing recruiter applications...")
        resp = requests.get(f"{API_BASE}/recruiters/me/applications", headers=headers)
        apps = resp.json()
        print(f"Applications count: {len(apps)}")
        
        # Test recruiter jobs
        print("Testing recruiter jobs...")
        resp = requests.get(f"{API_BASE}/recruiters/me/jobs", headers=headers)
        print(f"Jobs count: {len(resp.json())}")
    else:
        print(f"Recruiter login failed: {login_resp.status_code} - {login_resp.text}")

if __name__ == "__main__":
    test_dashboards()
