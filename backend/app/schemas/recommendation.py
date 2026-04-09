from pydantic import BaseModel, Field
from typing import List, Optional

class RiskInput(BaseModel):
    heart_risk: float = Field(0.0, ge=0.0, le=1.0)
    diabetes_risk: float = Field(0.0, ge=0.0, le=1.0)
    stroke_risk: float = Field(0.0, ge=0.0, le=1.0)
    ckd_risk: float = Field(0.0, ge=0.0, le=1.0)
    chri_score: float = Field(0.0, ge=0.0, le=1.0)

    class Config:
        json_schema_extra = {
            "example": {
                "heart_risk": 0.75,
                "diabetes_risk": 0.20,
                "stroke_risk": 0.10,
                "ckd_risk": 0.40,
                "chri_score": 0.45
            }
        }

class ActionRecommendationOutput(BaseModel):
    risk_level: str
    urgency_level: str
    recommended_specialists: List[str]
    suggested_actions: List[str]

class DoctorInput(BaseModel):
    disease_focus: str
    location: str

    class Config:
        json_schema_extra = {
            "example": {
                "disease_focus": "Heart Disease",
                "location": "New York"
            }
        }

class DoctorOutput(BaseModel):
    doctor_name: str
    specialization: str
    location: str
    rating: float
    availability: str

class LocationFacilitiesInput(BaseModel):
    location: str

    class Config:
        json_schema_extra = {
            "example": {
                "location": "San Francisco"
            }
        }

class FacilityOutput(BaseModel):
    name: str
    address: str
    rating: float
