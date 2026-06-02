from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class GPSCoordinates(BaseModel):
    latitude: float
    longitude: float


class CropDetail(BaseModel):
    crop_name: str
    area_hectares: float
    planted_date: str


class LivestockDetail(BaseModel):
    species: str
    count: int


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    farm_size: Optional[float] = None
    crops: Optional[List[CropDetail]] = None
    location: Optional[GPSCoordinates] = None
    livestock: Optional[List[LivestockDetail]] = None


class ProfileResponse(BaseModel):
    uid: str
    name: str
    phone: str
    email: str
    state: str
    district: str
    farm_size: float
    crops: List[CropDetail] = []
    location: Optional[GPSCoordinates] = None
    livestock: List[LivestockDetail] = []
