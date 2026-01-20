import requests
import json

url = "http://127.0.0.1:8001/api/v1/applications/"
payload = {
    "job_id": 1,
    "candidate_id": 1
}
headers = {
    "Content-Type": "application/json"
}

try:
    print(f"Sending POST to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        data = response.json()
        print(f"Error Detail: {data.get('detail')}")
        print("Traceback snippet:")
        print(data.get('trace')[-500:]) # Print last 500 chars
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
