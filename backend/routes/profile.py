from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from models.profile import ProfileUpdate, ProfileResponse
from database.firebase import db_client
from app.dependencies import get_current_user
from app.exceptions import NotFoundException

router = APIRouter(prefix="/profile", tags=["Farmer Profile"])


@router.get("", response_model=ProfileResponse)
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    uid = current_user["uid"]
    user_snap = db_client.collection("users").document(uid).get()
    if not user_snap.exists:
        user_data = {
            "uid": uid,
            "name": current_user.get("name") or current_user.get("email", "").split("@")[0].capitalize() or "Grower",
            "phone": "",
            "email": current_user.get("email") or f"{uid}@terrava.ai",
            "state": "Karnataka",
            "district": "Bengaluru",
            "farm_size": 4.2,
            "role": current_user.get("role", "farmer"),
            "crops": [],
            "livestock": [],
            "location": None
        }
        db_client.collection("users").document(uid).set(user_data)
    else:
        user_data = user_snap.to_dict()
    return ProfileResponse(
        uid=uid,
        name=user_data.get("name", ""),
        phone=user_data.get("phone", ""),
        email=user_data.get("email", ""),
        state=user_data.get("state", ""),
        district=user_data.get("district", ""),
        farm_size=user_data.get("farm_size", 0.0),
        crops=user_data.get("crops", []),
        location=user_data.get("location"),
        livestock=user_data.get("livestock", [])
    )


@router.put("", response_model=ProfileResponse)
async def update_profile(
    payload: ProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    user_ref = db_client.collection("users").document(uid)
    user_snap = user_ref.get()
    
    if not user_snap.exists:
        # Create a new profile document if it does not exist yet
        initial_data = {
            "uid": uid,
            "name": payload.name or current_user.get("name") or "Grower",
            "phone": payload.phone or "",
            "email": payload.email or current_user.get("email") or f"{uid}@terrava.ai",
            "state": payload.state or "Karnataka",
            "district": payload.district or "Bengaluru",
            "farm_size": payload.farm_size or 4.2,
            "role": current_user.get("role", "farmer"),
            "crops": [],
            "livestock": [],
            "location": None
        }
        user_ref.set(initial_data)
        user_snap = user_ref.get()

    # Filter out None values in update payload
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    
    # Standardize crop and livestock models to dict for Firestore compatibility
    if "crops" in update_data:
        update_data["crops"] = [c.model_dump() for c in payload.crops]
    if "livestock" in update_data:
        update_data["livestock"] = [l.model_dump() for l in payload.livestock]
    if "location" in update_data and payload.location:
        update_data["location"] = payload.location.model_dump()

    user_ref.update(update_data)
    
    # Return updated profile snapshot
    fresh_data = user_ref.get().to_dict()
    return ProfileResponse(
        uid=uid,
        name=fresh_data.get("name", ""),
        phone=fresh_data.get("phone", ""),
        email=fresh_data.get("email", ""),
        state=fresh_data.get("state", ""),
        district=fresh_data.get("district", ""),
        farm_size=fresh_data.get("farm_size", 0.0),
        crops=fresh_data.get("crops", []),
        location=fresh_data.get("location"),
        livestock=fresh_data.get("livestock", [])
    )
