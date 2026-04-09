import random
from typing import List, Dict, Any

class RecommendationService:
    def __init__(self):
        # A static/dummy dataset of doctors for demonstration purposes
        self.doctors_db = [
            {"doctor_name": "Dr. Sarah Jenkins", "specialization": "Cardiologist", "location": "New York", "rating": 4.8, "availability": "Next week"},
            {"doctor_name": "Dr. Michael Chen", "specialization": "Cardiologist", "location": "San Francisco", "rating": 4.9, "availability": "Tomorrow"},
            {"doctor_name": "Dr. Emily Roberts", "specialization": "Endocrinologist", "location": "New York", "rating": 4.7, "availability": "Next Month"},
            {"doctor_name": "Dr. James Wilson", "specialization": "Endocrinologist", "location": "Chicago", "rating": 4.6, "availability": "This week"},
            {"doctor_name": "Dr. Olivia Davis", "specialization": "Neurologist", "location": "San Francisco", "rating": 5.0, "availability": "Immediate"},
            {"doctor_name": "Dr. William Taylor", "specialization": "Neurologist", "location": "Boston", "rating": 4.8, "availability": "Next week"},
            {"doctor_name": "Dr. Sophia Brown", "specialization": "Nephrologist", "location": "Los Angeles", "rating": 4.7, "availability": "Within 2 weeks"},
            {"doctor_name": "Dr. Liam Thomas", "specialization": "Nephrologist", "location": "New York", "rating": 4.5, "availability": "Next week"}
        ]

    def get_action_recommendation(self, risks: dict) -> dict:
        """
        Logic-based system to convert risk probabilities and CHRI into actionable steps.
        Args:
            risks: dictionary with 'heart_risk', 'diabetes_risk', 'stroke_risk', 'ckd_risk', 'chri_score'
        """
        urgency_level = "Routine"
        overall_risk_level = "Low"
        recommended_specialists = set()
        suggested_actions = []

        # 1. Evaluate CHRI (Primary Urgency Driver)
        chri = risks.get('chri_score', 0.0)
        if chri >= 0.6:
            urgency_level = "Urgent"
            overall_risk_level = "Critical"
            suggested_actions.append("Your Cardiometabolic Health Risk Index is critically high. Seek immediate medical consultation.")
        elif chri >= 0.4:
            urgency_level = "High Priority"
            overall_risk_level = "High"
            suggested_actions.append("Your overall risk is elevated. Schedule a comprehensive health checkup soon.")
        elif chri >= 0.2:
            urgency_level = "Moderate"
            overall_risk_level = "Moderate"
            suggested_actions.append("Consider moderate lifestyle improvements: diet, exercise, and regular monitoring.")
        else:
            overall_risk_level = "Low"
            suggested_actions.append("Maintain your current healthy lifestyle and continue annual checkups.")

        # 2. Disease-Specific Rules
        if risks.get('heart_risk', 0.0) >= 0.7:
            recommended_specialists.add("Cardiologist")
            suggested_actions.append("High Heart Disease risk detected. Advised to get an ECG and consult a Cardiologist.")
        elif risks.get('heart_risk', 0.0) >= 0.5:
            suggested_actions.append("Elevated Heart Disease risk. Monitor blood pressure and cholesterol.")

        if risks.get('diabetes_risk', 0.0) >= 0.7:
            recommended_specialists.add("Endocrinologist")
            suggested_actions.append("High Diabetes risk detected. Perform fasting blood sugar test and consult an Endocrinologist.")
        elif risks.get('diabetes_risk', 0.0) >= 0.5:
            suggested_actions.append("Elevated Diabetes risk. Limit sugar intake and increase physical activity.")

        if risks.get('stroke_risk', 0.0) >= 0.7:
            recommended_specialists.add("Neurologist")
            if urgency_level != "Urgent":
                urgency_level = "Urgent"
                overall_risk_level = "Critical"
            suggested_actions.append("High Stroke risk detected. Urgent: Consult a Neurologist and monitor blood pressure strictly.")

        if risks.get('ckd_risk', 0.0) >= 0.7:
            recommended_specialists.add("Nephrologist")
            suggested_actions.append("High Chronic Kidney Disease risk detected. Perform kidney function test and consult a Nephrologist.")

        # Default fallback if specialists are empty but risk is moderate/high
        if overall_risk_level in ["Moderate", "High"] and not recommended_specialists:
            recommended_specialists.add("General Practitioner")

        return {
            "risk_level": overall_risk_level,
            "urgency_level": urgency_level,
            "recommended_specialists": list(recommended_specialists) if recommended_specialists else ["General Practitioner"],
            "suggested_actions": suggested_actions
        }

    def get_doctors_recommendation(self, disease_focus: str, location: str = "") -> List[Dict[str, Any]]:
        """
        Basic logic to return doctors based on disease and location.
        """
        # Map disease generic names to specialties
        mapping = {
            "Heart Disease": "Cardiologist",
            "Diabetes": "Endocrinologist",
            "Stroke": "Neurologist",
            "Chronic Kidney Disease": "Nephrologist"
        }
        
        target_specialization = mapping.get(disease_focus, "General Practitioner")
        
        results = []
        for doc in self.doctors_db:
            if doc["specialization"] == target_specialization:
                # Give slight preference or filter by location if requested
                # Simple loose matching for simulation
                if not location or location.lower() in doc["location"].lower():
                    results.append(doc)
                    
        # If no doctors found in exact location, return specialists regardless of location
        if not results:
            results = [doc for doc in self.doctors_db if doc["specialization"] == target_specialization]

        # Sort by rating ascending just for fun, or descending
        results = sorted(results, key=lambda x: x["rating"], reverse=True)
        return results

    def fetch_nearby_facilities_mock(self, location: str) -> List[Dict[str, Any]]:
        """
        Uses OpenStreetMap Nominatim API to fetch real hospitals/clinics nearby in the specified location.
        Requires NO API keys and exclusively uses python standard libraries.
        """
        import json
        import urllib.request
        import urllib.parse
        import random
        
        try:
            # Add 'hospital' to the query to restrict results natively
            query = urllib.parse.quote(f"hospital in {location}")
            url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5&addressdetails=1"
            
            # Nominatim requires a valid user-agent
            req = urllib.request.Request(
                url, 
                headers={"User-Agent": "DiseasePredictionSystem/1.0"}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    results = []
                    for item in data:
                        name = item.get("name")
                        if not name:
                            continue
                            
                        # Format a nice address
                        addr = item.get("address", {})
                        road = addr.get("road", "")
                        city = addr.get("city", addr.get("town", addr.get("state", "")))
                        country = addr.get("country", "")
                        
                        address_parts = [p for p in [road, city, country] if p]
                        address_str = ", ".join(address_parts)
                        
                        if not address_str:
                            address_str = item.get("display_name", "Unknown Address")
                        
                        # Generate a random decent rating
                        rating = round(random.uniform(4.0, 5.0), 1)
                        
                        results.append({
                            "name": name,
                            "address": address_str,
                            "rating": rating
                        })
                    
                    if results:
                        return results

        except Exception as e:
            print("Error connecting to Nominatim API:", e)

        # Fallback to the original mock if API fails or empty
        cities = {
            "new york": [
                {"name": "NYU Langone Health", "address": "550 1st Ave, New York, NY", "rating": 4.8},
                {"name": "Mount Sinai Hospital", "address": "1 Gustave L. Levy Pl, New York, NY", "rating": 4.6}
            ],
            "san francisco": [
                {"name": "UCSF Medical Center", "address": "505 Parnassus Ave, San Francisco, CA", "rating": 4.7},
                {"name": "Zuckerberg San Francisco General", "address": "1001 Potrero Ave, San Francisco, CA", "rating": 4.2}
            ],
            "default": [
                {"name": "City General Clinic", "address": f"Main Medical Plaza, {location.title()} Area", "rating": 4.4},
                {"name": "Advanced Healthcare Center", "address": f"Downtown {location.title()}", "rating": 4.6}
            ]
        }
        
        loc_key = location.lower().strip()
        if loc_key in cities:
            return cities[loc_key]
        return cities["default"]

recommendation_service = RecommendationService()
