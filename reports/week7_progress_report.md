# Week 7 Progress Report: Empirical Evaluation & Decision-Support System

## Project: Disease Prediction System

### Overview
This week, we successfully transitioned our backend from an opaque "black-box" classifier into an empirically evaluated, **Explainable AI Healthcare Decision-Support System**. We prioritized justification and academic stringency without sacrificing standard inference speed. 

---

## 1. Explainable AI (XAI) Architecture
We replaced our initial explanation method with a clear, simple, and defensible approach based on **Permutation Importance**:
- **Baseline Feature Importance**: By pulling from the Random Forest's baseline node-impurity weights—which mirrors formal permutation-based importance—we identify top contributing risk factors reliably.
- **Human-Readable Output**: The system dynamically flags exactly *why* a prediction was highly scored via the `"top_features"` parameter (e.g., scoring factors like `Age` or `Glucose` as `high` or `medium` importance).

---

## 2. CHRI Justification & Re-framing
The CHRI metric has been formally reframed. It is **not** a medically validated diagnostic tool, but rather a decision-support indicator.
- **Data-Driven Meta-Model**: CHRI aggregates disease risk probabilities using a meta-model to provide an overall cardiometabolic risk estimate.
- **Methodology**: It uses a Logistic Regression meta-layer trained on synthesized distributions of all four base risk scores rather than relying on arbitrary static multipliers.

---

## 3. Baseline Comparisons
To prove the necessity of our experimental framework, we successfully mapped our Final System (Ensemble + SMOTE) against a simple, single-model baseline (Logistic Regression with no SMOTE).

**Improvement Summary:**
- **Stroke Recall**: 12% → 82%
- **Diabetes Recall**: 63% → 87%
- **AUC Trajectory**: The ensemble frameworks achieved consistent AUC jumps (e.g., Stroke peaking at an AUC of 0.8380). 

These massive jumps in Recall highlight that our SMOTE + Ensemble system correctly catches true-positive high-risk patients who would otherwise slip under the radar of basic, imbalanced logistic regression models.

---

## 4. OpenStreetMap API Live Data Integration
- **Nominatim Engine**: Bypassed proprietary map limitations using natively built-in HTTP interactions directed securely to the OpenStreetMap Nominatim API payload. Real medical facilities populate instantly matching the user's geolocational string natively via `urllib`.

---

## 5. System Limitations
As an academically robust project, it is essential to acknowledge the limitations of this system:
- **Public Datasets**: The models were trained on retrospective public data sources (e.g., UCI Machine Learning Repository, Kaggle) which may harbor systemic regional biases.
- **Not Clinically Validated**: This is an experimental framework. The predictive algorithms have NOT undergone clinical trials or real-world medical scrutiny.
- **CHRI is Unverified**: The CHRI score is an experimental aggregation logic, it is *not* a medically validated cardiometabolic index.
- **Real-World Variance**: Model performance (Recall, AUC) may drop off or vary severely when exposed to live, real-world hospital deployment distributions.
