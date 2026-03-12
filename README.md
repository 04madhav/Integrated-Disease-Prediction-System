# AI-Based Integrated Cardiometabolic & Renal Risk Assessment System

This project is a multi-disease prediction system that calculates individual risks for Heart Disease, Diabetes, Stroke, and CKD, along with an integrated Global Risk Score (CHRI).

## 🚀 How to Run the Backend (FastAPI)

Your teammates can run the backend and see the interactive docs by following these steps:

### 1. Prerequisite: Install dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Start the Server
Run the bootstrapper script from the project root:
```bash
python run_backend.py
```
The server will start at `http://127.0.0.1:8000`.

### 3. View the Interactive API Docs (Swagger)
Once the server is running, open your browser and go to:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

From here, anyone can:
*   Click on an endpoint (e.g., `/predict/heart`).
*   Click **"Try it out"**.
*   Enter patient data in the JSON box.
*   Click **"Execute"** to see the real-time AI risk assessment.

---

## 📂 Project Structure for Teammates
*   `backend/`: Contains the FastAPI application logic.
*   `models/exported/`: Contains the trained `.joblib` model files.
*   `reports/`: Contains all weekly progress reports and terminology guides.
*   `scripts/`: Python scripts for model training and visualization.
*   `test_api.py`: A script to verify everything is working correctly.

## 📊 Key Documentation
For presentation preparation, please review:
*   `reports/terminology_guide.md`: Explains ML terms.
*   `reports/dataset_parameters_guide.md`: Explains clinical features and why we monitor them.
*   `reports/midterm_presentation_outline.md`: The structure for our final presentation.
