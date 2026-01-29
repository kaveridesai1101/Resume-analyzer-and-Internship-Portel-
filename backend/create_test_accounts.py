import sys
import os
import traceback

# Add current directory to path so it can find 'app'
sys.path.append(os.getcwd())

try:
    from app.database import SessionLocal, engine
    from app.models.all_models import User, CandidateProfile, RecruiterProfile, Base
    from app.core.security import get_password_hash
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def setup_users():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Standard Password
        pwd = get_password_hash("password123")
        
        test_users = [
            {"email": "student@test.com", "name": "Kaveri Student", "role": "candidate"},
            {"email": "recruiter@test.com", "name": "Global Tech Corp", "role": "recruiter"},
            {"email": "admin@test.com", "name": "System Administrator", "role": "admin"}
        ]
        
        for u_data in test_users:
            # Check if exists
            user = db.query(User).filter(User.email == u_data["email"]).first()
            if not user:
                print(f"Creating {u_data['role']}: {u_data['email']}")
                user = User(
                    email=u_data["email"],
                    hashed_password=pwd,
                    full_name=u_data["name"],
                    role=u_data["role"]
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                
                # Create Profiles
                if u_data["role"] == "candidate":
                    profile = CandidateProfile(user_id=user.id, name=u_data["name"])
                    db.add(profile)
                elif u_data["role"] == "recruiter":
                    profile = RecruiterProfile(user_id=user.id, organization_name=u_data["name"])
                    db.add(profile)
                db.commit()
            else:
                # Reset password to password123 for convenience
                user.hashed_password = pwd
                db.commit()
                print(f"Updated password for: {u_data['email']}")
    except Exception as e:
        print(f"Error during setup: {e}")
        traceback.print_exc()
    finally:
        db.close()
        
    print("\n--- Setup Complete ---")
    print("Student: student@test.com / password123")
    print("Recruiter: recruiter@test.com / password123")
    print("Admin: admin@test.com / password123")

if __name__ == "__main__":
    setup_users()
