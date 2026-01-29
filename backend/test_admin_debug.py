import requests

def test_user_detail():
    user_id = 1 # Admin or any user
    url = f"http://localhost:8000/api/v1/admin/users/{user_id}"
    print(f"Testing {url}...")
    try:
        res = requests.get(url)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_user_detail()
