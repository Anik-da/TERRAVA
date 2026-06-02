import uuid
import time
from fastapi import APIRouter, UploadFile, File, Depends, status
from typing import Dict, Any
from ai.plant_disease import plant_detector
from ai.animal_disease import animal_detector
from database.firebase import db_client, storage_bucket
from app.dependencies import get_current_user
from app.exceptions import TerravaException

router = APIRouter(prefix="/disease", tags=["Pathology & Disease Diagnostics"])


@router.post("/plant", status_code=status.HTTP_201_CREATED)
async def detect_plant_disease(
    file: UploadFile = File(..., description="Upload leaf or crop lesion image"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise TerravaException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid crop leaf image",
            error_code="INVALID_FILE_TYPE"
        )

    try:
        content = await file.read()
        
        # Run AI Diagnostic Pipeline
        diagnosis = await plant_detector.detect(content)
        
        # Optional: Save image to Firebase Storage if key is set
        report_id = str(uuid.uuid4())
        image_url = ""
        try:
            blob_path = f"disease_reports/plant_{report_id}.jpg"
            blob = storage_bucket.blob(blob_path)
            blob.upload_from_string(content, content_type="image/jpeg")
            image_url = blob.generate_signed_url(expiration=3600)
        except Exception:
            # Fallback to local reference
            image_url = f"https://terrava-farm.web.app/assets/reports/{report_id}.jpg"

        # Construct database report record
        report_data = {
            "report_id": report_id,
            "farmer_uid": current_user["uid"],
            "type": "plant",
            "disease": diagnosis["disease"],
            "severity": diagnosis["severity"],
            "confidence": diagnosis["confidence"],
            "treatment": diagnosis["treatment"],
            "image_url": image_url,
            "timestamp": time.time()
        }

        # Persist report in disease_reports collection
        db_client.collection("disease_reports").document(report_id).set(report_data)
        
        return report_data
    except Exception as e:
        raise TerravaException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during plant diagnostics: {str(e)}",
            error_code="DIAGNOSTIC_FAILURE"
        )


@router.post("/animal", status_code=status.HTTP_201_CREATED)
async def detect_animal_disease(
    file: UploadFile = File(..., description="Upload livestock skin or lesion image"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise TerravaException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid livestock diagnostic image",
            error_code="INVALID_FILE_TYPE"
        )

    try:
        content = await file.read()
        
        # Run Livestock Diagnostic Pipeline
        diagnosis = await animal_detector.detect(content)
        
        report_id = str(uuid.uuid4())
        image_url = ""
        try:
            blob_path = f"disease_reports/animal_{report_id}.jpg"
            blob = storage_bucket.blob(blob_path)
            blob.upload_from_string(content, content_type="image/jpeg")
            image_url = blob.generate_signed_url(expiration=3600)
        except Exception:
            image_url = f"https://terrava-farm.web.app/assets/reports/{report_id}.jpg"

        report_data = {
            "report_id": report_id,
            "farmer_uid": current_user["uid"],
            "type": "animal",
            "disease": diagnosis["disease"],
            "severity": diagnosis["severity"],
            "confidence": diagnosis["confidence"],
            "recommendation": diagnosis["recommendation"],
            "image_url": image_url,
            "timestamp": time.time()
        }

        db_client.collection("disease_reports").document(report_id).set(report_data)
        
        return report_data
    except Exception as e:
        raise TerravaException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during livestock diagnostics: {str(e)}",
            error_code="DIAGNOSTIC_FAILURE"
        )
