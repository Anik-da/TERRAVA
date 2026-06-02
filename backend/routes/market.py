from fastapi import APIRouter, Depends, status, Query
from typing import Dict, Any, Optional
from services.market_service import market_service
from app.dependencies import get_current_user
from database.firebase import db_client
from app.exceptions import NotFoundException

router = APIRouter(prefix="/market-prices", tags=["Market Intelligence"])


@router.get("")
async def get_market_prices(current_user: Dict[str, Any] = Depends(get_current_user)):
    # Returns complete active crop price indexes
    return market_service.get_prices()


@router.get("/forecast")
async def get_market_forecast(
    crop: str = Query(..., description="Crop type to forecast"),
    multiplier: Optional[float] = Query(1.0, description="Optional yield scaling multiplier"),
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
    farm_size = user_data.get("farm_size", 1.0)

    # Calculate estimated revenue, production costs, and expected profit margins
    forecast = market_service.calculate_forecast(crop, farm_size, multiplier)
    
    # Save search log to market_data collection
    db_client.collection("market_data").add({
        "farmer_uid": uid,
        "crop": crop,
        "estimated_yield": forecast["estimated_yield_quintals"],
        "estimated_profit": forecast["estimated_profit_inr"],
        "projected_profit": forecast["projected_profit_inr"]
    })

    return forecast
