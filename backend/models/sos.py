from pydantic import BaseModel, Field
from datetime import datetime
from models.profile import GPSCoordinates


class SOSRequest(BaseModel):
    location: GPSCoordinates
    emergency_type: str = Field(..., description="E.g., extreme_weather, medical, wild_animal_intrusion, equipment_failure")


class SOSResponse(BaseModel):
    sos_id: str
    farmer_uid: str
    farmer_name: str
    farmer_phone: str
    location: GPSCoordinates
    emergency_type: str
    status: str  # E.g., pending, dispatched, resolved
    created_at: datetime
