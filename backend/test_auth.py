import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_auth():
    print("Testing Registration...")
    reg_data = {
        "email": "test@candidate.com",
        "password": "password123",
        "full_name": "Test Candidate",
        "role": "candidate"
    }
    try:
        r = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
        if r.status_code == 200:
            print("✅ Registration Successful:", r.json())
        else:
            print("❌ Registration Failed:", r.text)
    except Exception as e:
        print(f"❌ Connection Error (Register): {e}")

    print("\nTesting Login...")
    login_data = {
        "username": "test@candidate.com", # OAuth2 form uses username field for email
        "password": "password123"
    }
    try:
        r = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if r.status_code == 200:
            print("✅ Login Successful:", r.json())
            token = r.json().get("access_token")
            print(f"🔑 Token received (len={len(token)})")
        else:
            print("❌ Login Failed:", r.text)
    except Exception as e:
        print(f"❌ Connection Error (Login): {e}")

if __name__ == "__main__":
    test_auth()
