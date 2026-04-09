import joblib
import pandas as pd
import os
from pathlib import Path
from backend.app.schemas.prediction import (
    HeartPredictionInput, 
    DiabetesPredictionInput, 
    StrokePredictionInput, 
    CKDPredictionInput
)

class PredictionService:
    def __init__(self):
        # Base path relative to where the server runs (project root)
        self.model_dir = Path("models/exported")
        self.models = {}
        self.meta_model = None
        self.load_models()

    def load_models(self):
        # We will use the Voting (Soft) ensemble as our primary one for the backend
        model_files = {
            'heart': 'heart_voting_(soft).joblib',
            'diabetes': 'diabetes_voting_(soft).joblib',
            'stroke': 'stroke_voting_(soft).joblib',
            'ckd': 'ckd_voting_(soft).joblib'
        }
        
        for disease, filename in model_files.items():
            path = self.model_dir / filename
            if path.exists():
                print(f"Loading {disease} model from {path}...")
                self.models[disease] = joblib.load(path)
            else:
                print(f"Warning: Model not found at {path}")
                
        # Load Meta model for CHRI
        meta_path = self.model_dir / "chri_meta_model.joblib"
        if meta_path.exists():
            print(f"Loading CHRI Meta-Model from {meta_path}...")
            self.meta_model = joblib.load(meta_path)
        else:
            print(f"Warning: CHRI Meta-Model not found at {meta_path}")

    def _explain_prediction(self, disease, df):
        """
        Uses explicit model feature importances (acting as Permutation Importance baseline)
        to identify globally top contributing features for the prediction in a simple, defensible way.
        """
        try:
            model = self.models.get(disease)
            if not model:
                return []
                
            preprocessor = model.named_steps['preprocessor']
            classifier = model.named_steps['classifier']
            
            # Extract Random Forest from Voting Classifier to get feature importances
            rf = classifier.named_estimators_['rf']
            importances = rf.feature_importances_
            
            try:
                feature_names = preprocessor.get_feature_names_out()
            except:
                feature_names = [f'feature_{i}' for i in range(len(importances))]
                
            impacts = []
            for name, imp in zip(feature_names, importances):
                clean_name = name.split('__')[-1] if '__' in name else name
                impacts.append({'feature': clean_name, 'importance_val': imp})
                
            # Sort by highest importance
            impacts.sort(key=lambda x: x['importance_val'], reverse=True)
            
            top_features = []
            for i, item in enumerate(impacts[:3]):
                # Map top 1 to "high", top 2 to "high", top 3 to "medium"
                level = "high" if i < 2 else "medium"
                top_features.append({
                    "feature": item['feature'],
                    "importance": level
                })
            return top_features
        except Exception as e:
            print(f"Explainability error for {disease}:", e)
            return []

    def predict_heart(self, data: HeartPredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['heart'].predict_proba(df)[0][1]
        factors = self._explain_prediction('heart', df)
        return float(prob), factors

    def predict_diabetes(self, data: DiabetesPredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['diabetes'].predict_proba(df)[0][1]
        factors = self._explain_prediction('diabetes', df)
        return float(prob), factors

    def predict_stroke(self, data: StrokePredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['stroke'].predict_proba(df)[0][1]
        factors = self._explain_prediction('stroke', df)
        return float(prob), factors

    def predict_ckd(self, data: CKDPredictionInput):
        df = pd.DataFrame([data.model_dump()])
        prob = self.models['ckd'].predict_proba(df)[0][1]
        factors = self._explain_prediction('ckd', df)
        return float(prob), factors

    def get_risk_level(self, prob: float):
        if prob < 0.2:
            return "Low"
        elif prob < 0.4:
            return "Moderate"
        elif prob < 0.7:
            return "High"
        else:
            return "Critical"

    def calculate_chri(self, risks: dict):
        if self.meta_model:
            # Map frontend keys to what the meta-model expects internally
            formatted_risks = {
                'prob_heart': risks.get('heart', 0.0),
                'prob_diabetes': risks.get('diabetes', 0.0),
                'prob_stroke': risks.get('stroke', 0.0),
                'prob_ckd': risks.get('ckd', 0.0)
            }
            df = pd.DataFrame([formatted_risks])
            prob = self.meta_model.predict_proba(df)[0][1]
            return float(prob)
        else:
            # Fallback
            weights = {
                'heart': 0.35,
                'stroke': 0.30,
                'diabetes': 0.20,
                'ckd': 0.15
            }
            chri = sum(risks[d] * weights[d] for d in weights if risks[d] is not None)
            return chri

# Singleton instance
prediction_service = PredictionService()
