import requests
import json

def test_job_post():
    url = "http://127.0.0.1:8000/api/v1/internships/?recruiter_id=1"
    payload = {
        "title": "Test Title",
        "description": "Test Description",
        "location": "Test Location",
        "company": "Test Company",
        "internship_type": "Internship",
        "mode": "Office",
        "duration": "3 Months",
        "stipend_salary": "Unpaid",
        "eligibility_criteria": "Test Eligibility",
        "deadline": None,
        "required_skills": ["Python"]
    }
    
    # Try to login first to get a token if needed, or if the endpoint requires auth
    # The frontend uses getAuthHeaders() which includes Bearer token.
    # Let's see if the backend @router.post("/") has a Depends(get_current_user).
    # It DOES NOT in internships.py! It only takes recruiter_id.
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_job_post()
