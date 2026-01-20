import requests
import json

url = "http://127.0.0.1:8000/api/v1/applications/"
# Using verified IDs from DB: Candidate 1 (User 8), Job 1
data = {
    "job_id": 1,
    "candidate_id": 1
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success! Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed! Detail: {response.text}")
except Exception as e:
    print(f"Error: {e}")
