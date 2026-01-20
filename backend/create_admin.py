"""
Create an admin user for the application
"""
from app.database import SessionLocal
from app.models.all_models import User
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@skillmatch.ai").first()
        if existing_admin:
            print("Admin user already exists!")
            print(f"Email: admin@skillmatch.ai")
            return
        
        # Create admin user
        admin = User(
            email="admin@skillmatch.ai",
            hashed_password=get_password_hash("admin123"),
            full_name="System Administrator",
            role="Admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created successfully!")
        print("\n📧 Email: admin@skillmatch.ai")
        print("🔑 Password: admin123")
        print("\n⚠️  IMPORTANT: Change this password after first login!")
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
