"""
Quick test script to verify status updates work correctly
"""
import requests
import json

API_BASE = "http://127.0.0.1:8000/api/v1"

# Test updating an existing application's status
def test_status_update():
    print("Testing Status Update Functionality...")
    
    # First, let's get an existing application
    response = requests.get(f"{API_BASE}/applications/")
    if response.status_code == 200:
        apps = response.json()
        if apps and len(apps) > 0:
            app_id = apps[0]['id']
            print(f"✓ Found application ID: {app_id}, current status: {apps[0].get('status', 'Unknown')}")
            
            # Test 1: Update to Shortlisted
            print("\nTest 1: Updating to 'Shortlisted'...")
            resp = requests.patch(
                f"{API_BASE}/applications/{app_id}/status",
                json={"status": "Shortlisted"}
            )
            if resp.status_code == 200:
                print(f"✓ Status updated successfully: {resp.json()}")
            else:
                print(f"✗ Failed: {resp.status_code} - {resp.text}")
            
            # Test 2: Update to Interview Call
            print("\nTest 2: Updating to 'Interview Call'...")
            resp = requests.patch(
                f"{API_BASE}/applications/{app_id}/status",
                json={"status": "Interview Call"}
            )
            if resp.status_code == 200:
                print(f"✓ Status updated successfully: {resp.json()}")
            else:
                print(f"✗ Failed: {resp.status_code} - {resp.text}")
            
            # Test 3: Update to Rejected
            print("\nTest 3: Updating to 'Rejected'...")
            resp = requests.patch(
                f"{API_BASE}/applications/{app_id}/status",
                json={"status": "Rejected"}
            )
            if resp.status_code == 200:
                print(f"✓ Status updated successfully: {resp.json()}")
            else:
                print(f"✗ Failed: {resp.status_code} - {resp.text}")
            
            # Verify the change
            print("\nVerifying final status...")
            verify_resp = requests.get(f"{API_BASE}/applications/{app_id}")
            if verify_resp.status_code == 200:
                final_status = verify_resp.json().get('status')
                print(f"✓ Final status: {final_status}")
            
        else:
            print("✗ No applications found to test")
    else:
        print(f"✗ Failed to fetch applications: {response.status_code}")

if __name__ == "__main__":
    test_status_update()
