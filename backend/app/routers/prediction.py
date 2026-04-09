from fastapi import APIRouter, HTTPException
from backend.app.schemas.prediction import (
    HeartPredictionInput,
    DiabetesPredictionInput,
    StrokePredictionInput,
    CKDPredictionInput,
    CHRIPredictionInput
)
from backend.app.services.prediction_service import prediction_service
from backend.app.services.recommendation_service import recommendation_service

router = APIRouter()

@router.post("/predict/heart")
async def predict_heart(data: HeartPredictionInput):
    try:
        prob, factors = prediction_service.predict_heart(data)
        return {
            "disease": "Heart Disease",
            "risk_probability": round(prob, 4),
            "risk_level": prediction_service.get_risk_level(prob),
            "top_features": factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/diabetes")
async def predict_diabetes(data: DiabetesPredictionInput):
    try:
        prob, factors = prediction_service.predict_diabetes(data)
        return {
            "disease": "Diabetes",
            "risk_probability": round(prob, 4),
            "risk_level": prediction_service.get_risk_level(prob),
            "top_features": factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/stroke")
async def predict_stroke(data: StrokePredictionInput):
    try:
        prob, factors = prediction_service.predict_stroke(data)
        return {
            "disease": "Stroke",
            "risk_probability": round(prob, 4),
            "risk_level": prediction_service.get_risk_level(prob),
            "top_features": factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/ckd")
async def predict_ckd(data: CKDPredictionInput):
    try:
        prob, factors = prediction_service.predict_ckd(data)
        return {
            "disease": "Chronic Kidney Disease",
            "risk_probability": round(prob, 4),
            "risk_level": prediction_service.get_risk_level(prob),
            "top_features": factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/chri")
async def predict_chri(data: CHRIPredictionInput):
    try:
        heart_prob, heart_factors = prediction_service.predict_heart(data.heart)
        diabetes_prob, diag_factors = prediction_service.predict_diabetes(data.diabetes)
        stroke_prob, stroke_factors = prediction_service.predict_stroke(data.stroke)
        ckd_prob, ckd_factors = prediction_service.predict_ckd(data.ckd)
        
        risks = {
            'heart': heart_prob,
            'diabetes': diabetes_prob,
            'stroke': stroke_prob,
            'ckd': ckd_prob
        }
        
        chri_score = prediction_service.calculate_chri(risks)
        
        # Get Action Recommendations
        action_recs = recommendation_service.get_action_recommendation({
            'heart_risk': heart_prob,
            'diabetes_risk': diabetes_prob,
            'stroke_risk': stroke_prob,
            'ckd_risk': ckd_prob,
            'chri_score': chri_score
        })
        
        # Get one doctor per recommended specialist
        doctors = []
        for spec in action_recs.get("recommended_specialists", []):
            disease = "Heart Disease" if spec == "Cardiologist" else \
                      "Diabetes" if spec == "Endocrinologist" else \
                      "Stroke" if spec == "Neurologist" else \
                      "Chronic Kidney Disease" if spec == "Nephrologist" else \
                      "General Practitioner"
            docs = recommendation_service.get_doctors_recommendation(disease_focus=disease)
            if docs:
                doctors.append(docs[0])

        return {
            # Core probabilities
            "heart": round(float(heart_prob), 4),
            "diabetes": round(float(diabetes_prob), 4),
            "stroke": round(float(stroke_prob), 4),
            "ckd": round(float(ckd_prob), 4),
            "chri_score": round(float(chri_score), 4),
            "risk_level": action_recs["risk_level"],
            
            # Week 7 Explainability & Actions
            "top_features": {
                "heart": heart_factors,
                "diabetes": diag_factors,
                "stroke": stroke_factors,
                "ckd": ckd_factors
            },
            "recommendations": {
                "urgency_level": action_recs["urgency_level"],
                "suggested_actions": action_recs["suggested_actions"],
                "recommended_doctors": doctors
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
