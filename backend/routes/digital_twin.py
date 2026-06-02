from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from models.digital_twin import DigitalTwinTelemetry, TwinResponse
from database.firebase import db_client
from app.dependencies import get_current_user
from app.exceptions import NotFoundException

router = APIRouter(prefix="/digital-twin", tags=["Digital Farm Twin Engine"])


@router.post("", response_model=TwinResponse)
async def update_digital_twin(
    payload: DigitalTwinTelemetry,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    
    # Check user existence & auto-seed if needed
    user_ref = db_client.collection("users").document(uid)
    user_snap = user_ref.get()
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
        user_ref.set(user_data)

    # Business Logic: Agricultural Health & Risk Calculations
    soil = payload.soil_data
    crop = payload.crop_data
    weather = payload.weather_data
    water = payload.water_data

    # 1. Health Score Calculation (0-100)
    # Ideal moisture is between 40% and 75%
    moisture_score = 100 - abs(soil.moisture - 57.5) * 2.2
    moisture_score = max(0.0, min(100.0, moisture_score))
    
    # Ideal pH is between 6.0 and 7.0
    ph_score = 100 - abs(soil.ph - 6.5) * 40.0
    ph_score = max(0.0, min(100.0, ph_score))
    
    # NDVI (canopy index) maps linearly (0.0 to 1.0 -> 0 to 100)
    ndvi_score = crop.canopy_index * 100.0
    
    # Chlorophyll index ideal is > 40
    chloro_score = min(100.0, (crop.chlorophyll / 50.0) * 100.0)
    
    health_score = round((moisture_score * 0.25) + (ph_score * 0.2) + (ndvi_score * 0.35) + (chloro_score * 0.2), 1)

    # 2. Threat Risk Score Calculation (0-100)
    risk_factors = []
    
    # Drought risk (moisture < 30) or Flood risk (moisture > 80)
    if soil.moisture < 30.0:
        risk_factors.append((30.0 - soil.moisture) * 2.0)  # Up to 60 risk points
    elif soil.moisture > 80.0:
        risk_factors.append((soil.moisture - 80.0) * 3.0)  # Up to 60 risk points
        
    # Soil nutrient deficiency
    nutrient_avg = (soil.nitrogen + soil.phosphorus + soil.potassium) / 3.0
    if nutrient_avg < 40.0:
        risk_factors.append((40.0 - nutrient_avg) * 1.5)
        
    # Canopy stress (low NDVI)
    if crop.canopy_index < 0.5:
        risk_factors.append((0.5 - crop.canopy_index) * 80.0)
        
    # Extreme weather factors (temp > 38 or temp < 5)
    if weather.temperature > 38.0:
        risk_factors.append((weather.temperature - 38.0) * 5.0)
    elif weather.temperature < 5.0:
        risk_factors.append((5.0 - weather.temperature) * 6.0)

    # Evapotranspiration vs Water Flow deficits (ET > flow rate)
    if water.evapotranspiration > (water.water_flow_rate / 5.0):
        risk_factors.append((water.evapotranspiration - (water.water_flow_rate / 5.0)) * 10.0)

    # Compile Risk Score
    risk_score = round(min(100.0, sum(risk_factors) if risk_factors else 5.0), 1)

    # Format telemetry dict
    twin_data = {
        "farm_id": uid,
        "soil_data": soil.model_dump(),
        "crop_data": crop.model_dump(),
        "weather_data": weather.model_dump(),
        "water_data": water.model_dump(),
        "health_score": health_score,
        "risk_score": risk_score
    }

    # Persist twin telemetry in farms collection
    db_client.collection("farms").document(uid).set(twin_data)
    
    return TwinResponse(
        farm_id=uid,
        soil_data=soil,
        crop_data=crop,
        weather_data=weather,
        water_data=water,
        health_score=health_score,
        risk_score=risk_score
    )


@router.get("", response_model=TwinResponse)
async def get_digital_twin(current_user: Dict[str, Any] = Depends(get_current_user)):
    uid = current_user["uid"]
    
    # Auto-seed user profile if missing
    user_ref = db_client.collection("users").document(uid)
    if not user_ref.get().exists:
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
        user_ref.set(user_data)

    twin_snap = db_client.collection("farms").document(uid).get()
    if not twin_snap.exists:
        # Default high-fidelity telemetry for hackathon-ready demo
        default_twin = {
            "farm_id": uid,
            "soil_data": {
                "moisture": 52.4,
                "ph": 6.7,
                "nitrogen": 48.0,
                "phosphorus": 35.0,
                "potassium": 115.0
            },
            "crop_data": {
                "canopy_index": 0.72,
                "leaf_area_index": 3.1,
                "chlorophyll": 42.5
            },
            "weather_data": {
                "temperature": 28.5,
                "humidity": 62.0,
                "rainfall_forecast": 1.2
            },
            "water_data": {
                "water_flow_rate": 22.5,
                "evapotranspiration": 4.1
            },
            "health_score": 82.5,
            "risk_score": 12.0
        }
        db_client.collection("farms").document(uid).set(default_twin)
        return TwinResponse(**default_twin)
        
    data = twin_snap.to_dict()
    return TwinResponse(**data)
