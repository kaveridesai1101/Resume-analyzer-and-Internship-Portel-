from sqlalchemy.orm import Session
from app.models.all_models import ActivityLog
from typing import Optional, Any

def log_activity(
    db: Session, 
    user_id: int, 
    action: str, 
    entity_type: str, 
    entity_id: int, 
    details: Optional[dict] = None
):
    """
    Creates a new activity log entry in the database.
    """
    try:
        log_entry = ActivityLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print(f"Failed to log activity: {e}")
        db.rollback()
