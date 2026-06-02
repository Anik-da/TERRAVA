from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from database.firebase import db_client
from app.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics & Telemetry Aggregator"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_analytics_metrics(current_user: Dict[str, Any] = Depends(get_current_user)):
    uid = current_user["uid"]

    # 1. Fetch User Base Metrics (Demographics counts)
    users_docs = db_client.collection("users").get()
    total_farmers = len(users_docs)
    
    total_hectares = 0.0
    crop_counts = {}
    livestock_counts = {}
    
    for u in users_docs:
        u_data = u.to_dict()
        total_hectares += u_data.get("farm_size", 0.0)
        
        # Aggregate Crops
        for crop in u_data.get("crops", []):
            name = crop.get("crop_name", "Other")
            crop_counts[name] = crop_counts.get(name, 0.0) + crop.get("area_hectares", 0.0)
            
        # Aggregate Livestock
        for live in u_data.get("livestock", []):
            species = live.get("species", "Other")
            livestock_counts[species] = livestock_counts.get(species, 0) + live.get("count", 0)

    # 2. Fetch Disease Pathology Counts
    reports_docs = db_client.collection("disease_reports").get()
    plant_diseases = {}
    animal_diseases = {}
    
    for r in reports_docs:
        r_data = r.to_dict()
        dis_name = r_data.get("disease", "Unknown")
        if r_data.get("type") == "plant":
            plant_diseases[dis_name] = plant_diseases.get(dis_name, 0) + 1
        else:
            animal_diseases[dis_name] = animal_diseases.get(dis_name, 0) + 1

    # 3. Market Index Stats
    market_docs = db_client.collection("market_data").get()
    market_queries_count = len(market_docs)

    return {
        "grower_demographics": {
            "total_registered_farmers": total_farmers,
            "total_cultivated_hectares": round(total_hectares, 2),
            "crop_distribution_hectares": crop_counts,
            "livestock_census_count": livestock_counts
        },
        "pathology_diagnostics": {
            "total_scans_logged": len(reports_docs),
            "plant_pathogens_distribution": plant_diseases,
            "animal_diseases_distribution": animal_diseases
        },
        "market_intelligence": {
            "total_search_forecasts": market_queries_count,
            "market_status_indicator": "bullish" if market_queries_count > 2 else "stable"
        }
    }
