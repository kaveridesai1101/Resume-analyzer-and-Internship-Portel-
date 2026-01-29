import requests

url = "http://127.0.0.1:8000/api/v1/auth/login"
data = {
    "username": "student@test.com",
    "password": "password123"
}

try:
    print(f"Testing POST to {url}...")
    # Send as JSON
    response = requests.post(url, json=data) 
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
