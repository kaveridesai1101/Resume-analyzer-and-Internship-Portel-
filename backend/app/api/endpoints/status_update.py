@router.patch("/{application_id}/status")
def update_application_status(application_id: int, status: dict):
    """Update the status of an application (for recruiters)"""
    try:
        conn = sqlite3.connect('skillmatch.db')
        curr = conn.cursor()
        
        new_status = status.get('status')
        if not new_status:
            conn.close()
            raise HTTPException(status_code=400, detail="Status is required")
        
        # Verify application exists
        curr.execute("SELECT id FROM applications WHERE id = ?", (application_id,))
        if not curr.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Update status
        now = datetime.utcnow().isoformat()
        curr.execute(
            "UPDATE applications SET status = ?, updated_at = ? WHERE id = ?",
            (new_status, now, application_id)
        )
        
        conn.commit()
        conn.close()
        
        return {"message": "Status updated successfully", "status": new_status}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))
