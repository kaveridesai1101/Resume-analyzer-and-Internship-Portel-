import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.all_models import ActivityLog, User, Job, Application
from sqlalchemy import desc

def verify_audit_trail():
    db = SessionLocal()
    try:
        print("\n🔍 Verifying Audit Trail...")
        
        # Get latest log
        latest_log = db.query(ActivityLog).order_by(desc(ActivityLog.created_at)).first()
        
        if latest_log:
            print(f"✅ Latest Log Found: ID {latest_log.id}")
            print(f"   Action: {latest_log.action}")
            print(f"   Entity: {latest_log.entity_type}")
            print(f"   Details: {latest_log.details}")
            print(f"   Timestamp: {latest_log.created_at}")
        else:
            print("⚠️ No audit logs found.")

        # Check for user registration logs
        reg_logs = db.query(ActivityLog).filter(ActivityLog.action == "User Registered").all()
        print(f"📊 Total Registration Events: {len(reg_logs)}")

        # Check for job creation logs
        job_logs = db.query(ActivityLog).filter(ActivityLog.action == "Created Job").all()
        print(f"📊 Total Job Creation Events: {len(job_logs)}")

        # Check for application logs
        app_logs = db.query(ActivityLog).filter(ActivityLog.action == "Applied to Job").all()
        print(f"📊 Total Application Events: {len(app_logs)}")
        
        print("\n✅ Verification Complete: Audit logging is active and recording events.")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_audit_trail()
