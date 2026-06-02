from fastapi import APIRouter, Depends, status
from typing import Dict, Any, List
from database.firebase import db_client
from app.dependencies import verify_admin
from app.exceptions import NotFoundException

router = APIRouter(prefix="/admin", tags=["Admin Operations Control Panel"])


@router.get("/users", status_code=status.HTTP_200_OK)
async def list_all_users(admin_user: Dict[str, Any] = Depends(verify_admin)):
    # Retrieve all users in the system
    users_docs = db_client.collection("users").get()
    
    users_list = []
    for doc in users_docs:
        data = doc.to_dict()
        # Remove passwords for security
        if "password" in data:
            del data["password"]
        users_list.append(data)
        
    return users_list


@router.put("/users/{user_id}/role", status_code=status.HTTP_200_OK)
async def modify_user_role(
    user_id: str,
    role: str,
    admin_user: Dict[str, Any] = Depends(verify_admin)
):
    user_ref = db_client.collection("users").document(user_id)
    user_snap = user_ref.get()
    
    if not user_snap.exists:
        raise NotFoundException("Grower account not found to modify role settings")
        
    user_ref.update({"role": role})
    return {"message": f"Successfully updated user role to: {role}"}


@router.get("/reports", status_code=status.HTTP_200_OK)
async def audit_system_reports(admin_user: Dict[str, Any] = Depends(verify_admin)):
    # Aggregates system alerts, active SOS metrics, and pathology reports
    sos_docs = db_client.collection("sos_requests").get()
    disease_docs = db_client.collection("disease_reports").get()
    
    return {
        "active_emergency_sos_signals": [doc.to_dict() for doc in sos_docs],
        "pathology_scans_logged": [doc.to_dict() for doc in disease_docs]
    }
