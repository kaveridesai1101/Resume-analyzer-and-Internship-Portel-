import requests
import random

url = "http://127.0.0.1:8000/api/v1/auth/register/student"
data = {
    "full_name": "Test Student",
    "email": f"tester_{random.randint(1000, 9999)}@test.com",
    "password": "password123",
    "skills": "Python, React"
}

try:
    print(f"Testing Student Register to {url}...")
    response = requests.post(url, json=data) 
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
