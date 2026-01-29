import requests

def test_admin_routes():
    base_url = "http://localhost:8000/api/v1/admin"
    routes = [
        "/stats",
        "/activity",
        "/users",
        "/internships",
        "/me" # PATCH, but GET might 405 or 404. It's only PATCH.
    ]
    
    print("Testing Admin API Routes...")
    
    for route in routes:
        url = f"{base_url}{route}"
        print(f"Checking {url} ...")
        try:
            # We use PATCH for /me, GET for others
            if route == "/me":
                # Just check if it exists (405 Method Not Allowed is good, 404 is bad)
                res = requests.get(url) 
                if res.status_code == 405:
                    print(f"  [OK] Exists (Method Not Allowed for GET)")
                elif res.status_code == 404:
                    print(f"  [FAIL] 404 Not Found")
                else:
                    print(f"  [?] Status: {res.status_code}")
            else:
                res = requests.get(url)
                if res.status_code == 200:
                    print(f"  [OK] 200 OK")
                else:
                    print(f"  [FAIL] Status: {res.status_code}")
                    print(f"  Response: {res.text[:100]}")
        except Exception as e:
            print(f"  [ERROR] {e}")

if __name__ == "__main__":
    test_admin_routes()
