import requests
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

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
        with open("error_trace.txt", "w", encoding="utf-8") as f:
            f.write(data.get('trace', 'No trace provided'))
        print("Trace written to error_trace.txt")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
