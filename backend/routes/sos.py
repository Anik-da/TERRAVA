import uuid
import time
from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from models.sos import SOSRequest, SOSResponse
from database.firebase import db_client
from app.dependencies import get_current_user
from app.exceptions import NotFoundException

router = APIRouter(prefix="/sos", tags=["Emergency SOS Operations"])


@router.post("", response_model=SOSResponse, status_code=status.HTTP_201_CREATED)
async def trigger_sos(
    payload: SOSRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    
    # Retrieve user contact records
    user_snap = db_client.collection("users").document(uid).get()
    if not user_snap.exists:
        raise NotFoundException("Farmer profile details could not be found to launch emergency SOS dispatch")
        
    user_data = user_snap.to_dict()
    sos_id = str(uuid.uuid4())
    
    sos_data = {
        "sos_id": sos_id,
        "farmer_uid": uid,
        "farmer_name": user_data.get("name", "Unknown Grower"),
        "farmer_phone": user_data.get("phone", "N/A"),
        "location": payload.location.model_dump(),
        "emergency_type": payload.emergency_type,
        "status": "dispatched",
        "created_at": float(time.time())
    }

    # Store emergency state
    db_client.collection("sos_requests").document(sos_id).set(sos_data)
    
    # Broadcast alert instantly (simulate notification log insertion)
    db_client.collection("notifications").add({
        "type": "sos_alert",
        "title": f"🚨 EMERGENCY: {payload.emergency_type.upper()}",
        "message": f"SOS signal received from farmer {user_data.get('name')} at GPS coordinate {payload.location.latitude}, {payload.location.longitude}",
        "recipient_uid": "all_regional_responders",
        "timestamp": time.time()
    })

    return SOSResponse(
        sos_id=sos_id,
        farmer_uid=uid,
        farmer_name=user_data.get("name", "Unknown Grower"),
        farmer_phone=user_data.get("phone", "N/A"),
        location=payload.location,
        emergency_type=payload.emergency_type,
        status="dispatched",
        created_at=time.time()
    )


@router.get("/active", response_model=list[SOSResponse])
async def get_active_sos_alerts(current_user: Dict[str, Any] = Depends(get_current_user)):
    # Returns all unresolved emergency alerts in the region
    sos_docs = db_client.collection("sos_requests").where("status", "==", "dispatched").get()
    
    active_alerts = []
    for doc in sos_docs:
        data = doc.to_dict()
        active_alerts.append(SOSResponse(**data))
        
    return active_alerts
