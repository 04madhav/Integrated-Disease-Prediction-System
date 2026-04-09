# Week 6 Progress Report: Clinical Recommendation System

## Project: Disease Prediction System

### Overview
This week, we expanded the system from a pure predictive risk calculator into a fully actionable **Healthcare Navigation Tool**. By translating raw algorithmic probabilities into actionable, clinical recommendations, the system now provides the vital "What's Next?" to the user rather than simply providing a score.

---

## 1. Risk-to-Action Mapping 
We added a sophisticated logic engine (`recommendation_service.py`) that interprets the probabilities bounds of our existing risk models and the CHRI score.
- **Urgency Handlers**: Routes logic through urgency indicators ("Routine", "Moderate", "High Priority", "Urgent").
- **Dynamic Advice**: Maps specific disease high-risk probabilities (e.g. Heart Disease >= 70%) to tailored medical suggestions (e.g. "Advised to get an ECG and monitor blood pressure").

---

## 2. Doctor Recommendation System
We developed mechanisms to directly map clinical risks into specific specialists. 
- Integrated a mock local medical directory system tracking Specialists (Cardiologists, Neurologists, Endocrinologists, Nephrologists).
- Generates locally relevant doctor profiles, complete with wait time indicators, locations, and system patient ratings.

---

## 3. Basic Healthcare Navigation Endpoint
To further assist users acting on urgent recommendations:
- Setup geographic API routes designed to locate and list active nearby hospitals and testing clinics given a patient's city string.

---

## 4. API Endpoints Upgraded
We updated our FastAPI backend routers, formally launching three new post-prediction interactive routes:
- `/recommend/action`: Generates risk matrix workflows.
- `/recommend/doctors`: Fetches specialized MDs corresponding to the highest clinical risks.
- `/recommend/facilities`: Pulls proximal diagnostic and emergency facilities.

---

## Next Steps (Week 7)
- **Model Validation**: Scientifically test the boundaries, baseline discrepancies, and reliability correlations of our risk engines.
- **Explainability**: Integrate real-time feature importance markers (e.g., "Age heavily factored into this score") so users understand exactly why they flagged high risk.
- **Meta-Modeling**: Replace static multiplier metrics in CHRI with data-driven predictive logic.
