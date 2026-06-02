from typing import Optional
from pydantic import BaseModel, Field


class SoilTelemetry(BaseModel):
    moisture: float = Field(..., description="Soil moisture percentage (0-100)")
    ph: float = Field(..., description="Soil pH value (0-14)")
    nitrogen: float = Field(..., description="Nitrogen value in mg/kg")
    phosphorus: float = Field(..., description="Phosphorus value in mg/kg")
    potassium: float = Field(..., description="Potassium value in mg/kg")


class CropTelemetry(BaseModel):
    canopy_index: float = Field(..., description="Normalized Difference Vegetation Index (NDVI) (0.0-1.0)")
    leaf_area_index: float = Field(..., description="LAI index value")
    chlorophyll: float = Field(..., description="Chlorophyll index (ug/cm2)")


class WeatherTelemetry(BaseModel):
    temperature: float = Field(..., description="Ambient temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity percentage (0-100)")
    rainfall_forecast: float = Field(..., description="Expected rainfall in mm")


class WaterTelemetry(BaseModel):
    water_flow_rate: float = Field(..., description="Irrigation flow rate in L/min")
    evapotranspiration: float = Field(..., description="ET rate in mm/day")


class DigitalTwinTelemetry(BaseModel):
    soil_data: SoilTelemetry
    crop_data: CropTelemetry
    weather_data: WeatherTelemetry
    water_data: WaterTelemetry


class TwinResponse(BaseModel):
    farm_id: str
    soil_data: SoilTelemetry
    crop_data: CropTelemetry
    weather_data: WeatherTelemetry
    water_data: WaterTelemetry
    health_score: float = Field(..., description="Calculated overall health score (0-100)")
    risk_score: float = Field(..., description="Calculated total agricultural threat index (0-100)")
