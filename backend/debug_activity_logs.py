import sqlite3
import json
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class UserInDB(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool = True
    model_config = ConfigDict(from_attributes=True)

class ActivityLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    details: Optional[dict] = None
    created_at: datetime
    user: UserInDB
    model_config = ConfigDict(from_attributes=True)

def check_logs():
    conn = sqlite3.connect('skillmatch.db')
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    
    curr.execute("""
        SELECT a.id, a.user_id, a.action, a.entity_type, a.entity_id, a.details, a.created_at,
               u.id as u_id, u.email, u.full_name, u.role, u.is_active
        FROM activity_logs a
        JOIN users u ON a.user_id = u.id
    """)
    rows = curr.fetchall()
    
    for row in rows:
        d = dict(row)
        details_processed = d['details']
        if isinstance(details_processed, str):
            try:
                details_processed = json.loads(details_processed)
            except:
                pass # keep as string if fail

        # Force handling of non-dict
        if details_processed is not None and not isinstance(details_processed, dict):
            print(f"ID {d['id']} INVALID DETAILS TYPE: {type(details_processed)} Val: {details_processed}")

        user_obj = UserInDB(
            id=d['u_id'], email=d['email'], full_name=d['full_name'], 
            role=d['role'], is_active=bool(d['is_active'])
        )
        
        log_data = {
            "id": d['id'],
            "user_id": d['user_id'],
            "action": d['action'],
            "entity_type": d['entity_type'],
            "entity_id": d['entity_id'],
            "details": details_processed,
            "created_at": d['created_at'],
            "user": user_obj
        }
        
        try:
            model = ActivityLogResponse(**log_data)
        except Exception as e:
            print(f"ID {d['id']} VALIDATION FAIL: {e}")

    conn.close()

if __name__ == "__main__":
    check_logs()
