import requests

def test_admin_endpoints():
    base_url = "http://localhost:8000/api/v1/admin"
    
    print(f"Testing {base_url}/stats ...")
    try:
        res = requests.get(f"{base_url}/stats")
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:200]}")
    except Exception as e:
        print(f"Stats Error: {e}")

    print(f"\nTesting {base_url}/activity ...")
    try:
        res = requests.get(f"{base_url}/activity")
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:200]}")
    except Exception as e:
        print(f"Activity Error: {e}")

if __name__ == "__main__":
    test_admin_endpoints()
