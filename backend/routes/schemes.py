from fastapi import APIRouter, Depends, status, Query
from typing import Dict, Any, Optional
from ai.scheme_search import scheme_search_engine
from database.firebase import db_client
from app.dependencies import get_current_user
from app.exceptions import NotFoundException

router = APIRouter(prefix="/schemes", tags=["Government Scheme Engine"])


@router.get("")
async def get_government_schemes(
    filter_by_profile: bool = Query(True, description="If true, filters matching current farmer profile"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    user_snap = db_client.collection("users").document(uid).get()
    
    if not user_snap.exists:
        # Auto-seed profile
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
    state = user_data.get("state", "")
    farm_size = user_data.get("farm_size", 0.0)
    
    # Retrieve all active schemes in Firestore
    schemes_docs = db_client.collection("government_schemes").get()
    all_schemes = [doc.to_dict() for doc in schemes_docs]

    if not filter_by_profile:
        return all_schemes

    # Filter schemes mathematically based on eligibility bounds
    eligible_schemes = []
    for s in all_schemes:
        # Check State Bounds
        if s.get("state") != "All" and s.get("state").lower() != state.lower():
            continue
        
        # Check Farm Size Bounds
        min_size = s.get("min_farm_size", 0.0)
        max_size = s.get("max_farm_size", 100.0)
        if not (min_size <= farm_size <= max_size):
            continue

        eligible_schemes.append(s)

    return eligible_schemes


@router.get("/search")
async def search_government_schemes(
    query: str = Query(..., description="Semantic search query for subsidies"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    # Fetch all schemes
    schemes_docs = db_client.collection("government_schemes").get()
    all_schemes = [doc.to_dict() for doc in schemes_docs]

    # Perform dense semantic search using BGE Small
    scored_results = await scheme_search_engine.search(query, all_schemes)
    return scored_results
