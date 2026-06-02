import time
from fastapi import APIRouter, Depends, status
from typing import Dict, Any, List
from database.firebase import db_client
from app.dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notification Engine"])


@router.get("", status_code=status.HTTP_200_OK)
async def list_notifications(current_user: Dict[str, Any] = Depends(get_current_user)):
    uid = current_user["uid"]
    
    # Retrieve alerts targeted to this grower specifically, or all-responders general alerts
    notif_docs = db_client.collection("notifications").get()
    
    alerts = []
    for doc in notif_docs:
        data = doc.to_dict()
        recipient = data.get("recipient_uid", "")
        if recipient in [uid, "all_regional_responders", "all_farmers", "all"]:
            # Parse simple timestamp
            alerts.append({
                "notification_id": doc.id,
                "type": data.get("type", "general"),
                "title": data.get("title", "Notice"),
                "message": data.get("message", ""),
                "timestamp": data.get("timestamp", time.time())
            })
            
    # Sort chronologically (newest first)
    return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)


@router.post("/trigger-alert", status_code=status.HTTP_201_CREATED)
async def trigger_system_alert(
    type: str,
    title: str,
    message: str,
    recipient_uid: str = "all_farmers",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    # Only admins can broadcast custom global system warnings
    if current_user["role"] != "admin" and recipient_uid in ["all_farmers", "all"]:
        # Simulate simple log or limit to farmers own scopes
        recipient_uid = current_user["uid"]

    alert_data = {
        "type": type,
        "title": title,
        "message": message,
        "recipient_uid": recipient_uid,
        "timestamp": time.time()
    }
    
    db_client.collection("notifications").add(alert_data)
    return {"message": "Notification broadcast successfully integrated", "data": alert_data}
