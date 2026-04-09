from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.schemas.recommendation import (
    RiskInput,
    ActionRecommendationOutput,
    DoctorInput,
    DoctorOutput,
    LocationFacilitiesInput,
    FacilityOutput
)
from backend.app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.post("/action", response_model=ActionRecommendationOutput)
async def recommend_action(data: RiskInput):
    """
    Generate actionable recommendations based on disease risk predictions and CHRI score.
    """
    try:
        recommendations = recommendation_service.get_action_recommendation(data.model_dump())
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/doctors", response_model=List[DoctorOutput])
async def recommend_doctors(data: DoctorInput):
    """
    Recommend specialists based on predicted disease and optionally by location.
    """
    try:
        doctors = recommendation_service.get_doctors_recommendation(
            disease_focus=data.disease_focus,
            location=data.location
        )
        return doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facilities", response_model=List[FacilityOutput])
async def recommend_facilities(data: LocationFacilitiesInput):
    """
    Recommend nearby healthcare facilities based on a location (Simulated Google Maps API).
    """
    try:
        facilities = recommendation_service.fetch_nearby_facilities_mock(location=data.location)
        return facilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
