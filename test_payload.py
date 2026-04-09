import sys
import json
from backend.app.schemas.prediction import CHRIPredictionInput
from backend.app.services.prediction_service import prediction_service
from backend.app.services.recommendation_service import recommendation_service

payload = {
    "heart": {
        "age": 65, "sex": 1, "cp": 3, "trestbps": 150, "chol": 240, "fbs": 1, 
        "restecg": 1, "thalach": 140, "exang": 1, "oldpeak": 1.5, "slope": 1, "ca": 1, "thal": 2
    },
    "diabetes": {
        "Pregnancies": 0, "Glucose": 160, "BloodPressure": 150, "SkinThickness": 20,
        "Insulin": 80, "BMI": 33.6, "DiabetesPedigreeFunction": 0.5, "Age": 65
    },
    "stroke": {
        "gender": "Male", "age": 65, "hypertension": 1, "heart_disease": 1, 
        "ever_married": "Yes", "work_type": "Private", "Residence_type": "Urban", 
        "avg_glucose_level": 160, "bmi": 33.6, "smoking_status": "smokes"
    },
    "ckd": {
        "age": 65, "bp": 150, "sg": 1.015, "al": 2, "su": 0, "rbc": "normal", "pc": "abnormal", 
        "pcc": "present", "ba": "notpresent", "bgr": 160, "bu": 40, "sc": 1.5, "sod": 135, 
        "pot": 4.0, "hemo": 11.0, "pcv": 32, "wc": 6000, "rc": 4.0, "htn": "yes", "dm": "yes", 
        "cad": "no", "appet": "poor", "pe": "yes", "ane": "yes"
    }
}

try:
    print("Parsing Pydantic...")
    data = CHRIPredictionInput(**payload)
    print("Heart...")
    heart_prob, heart_factors = prediction_service.predict_heart(data.heart)
    print("Diabetes...")
    diabetes_prob, diag_factors = prediction_service.predict_diabetes(data.diabetes)
    print("Stroke...")
    stroke_prob, stroke_factors = prediction_service.predict_stroke(data.stroke)
    print("CKD...")
    ckd_prob, ckd_factors = prediction_service.predict_ckd(data.ckd)
    
    print("Calculating CHRI...")
    risks = {'heart': heart_prob, 'diabetes': diabetes_prob, 'stroke': stroke_prob, 'ckd': ckd_prob}
    chri = prediction_service.calculate_chri(risks)
    print("Done! CHRI:", chri)

except Exception as e:
    import traceback
    traceback.print_exc()

