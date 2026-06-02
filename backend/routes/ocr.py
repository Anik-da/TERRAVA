import uuid
import time
from fastapi import APIRouter, UploadFile, File, Depends, status
from typing import Dict, Any
from ai.ocr import ocr_engine
from database.firebase import db_client
from app.dependencies import get_current_user
from app.exceptions import TerravaException

router = APIRouter(prefix="/ocr", tags=["OCR Document Scanner"])


@router.post("/scan", status_code=status.HTTP_201_CREATED)
async def scan_document(
    file: UploadFile = File(..., description="Upload printed document, soil report, or receipt image"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Scan a printed document using TrOCR (microsoft/trocr-base-printed).
    Extracts text from soil test reports, agricultural receipts, and printed documents.
    """
    if not file.content_type.startswith("image/"):
        raise TerravaException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid document image (PNG, JPG).",
            error_code="INVALID_FILE_TYPE"
        )

    try:
        content = await file.read()

        # Run TrOCR OCR Pipeline
        result = await ocr_engine.scan(content)

        scan_id = str(uuid.uuid4())

        # Persist scan record in Firestore
        scan_data = {
            "scan_id": scan_id,
            "farmer_uid": current_user["uid"],
            "extracted_text": result["extracted_text"],
            "engine": result["engine"],
            "timestamp": time.time()
        }

        db_client.collection("ocr_scans").document(scan_id).set(scan_data)

        return scan_data
    except Exception as e:
        raise TerravaException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OCR scanning failure: {str(e)}",
            error_code="OCR_FAILURE"
        )
