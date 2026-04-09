# Week 7 Update Report

## 1. Meta-Model for CHRI
CHRI aggregates disease risk probabilities using a data-driven meta-model to provide an overall cardiometabolic risk decision-support estimate. It does not provide medically validated diagnoses.
A Logistic Regression meta-layer was trained on synthetic distribution of probabilities to replace arbitrary static weights.
Learned Weights: 
- Heart: 18.7503
- Diabetes: 14.0446
- Stroke: 9.7276
- CKD: 5.1251
Intercept: -19.0243

## 2. Baseline Comparison
To evaluate the empirical effectiveness of our framework, we compare a Baseline (Single Logistic Regression without SMOTE) against our Final System (Ensemble Models with SMOTE data balancing):

**Recall Improvements:**
- **Stroke Recall**: 12% → 82%
- **Diabetes Recall**: 63% → 87%

**Summary**: The Ensemble + SMOTE system drastically improves Recall, successfully flagging true-positive high-risk patients that basic models miss due to heavy class imbalance. This establishes its utility as a reliable initial decision-support filter.

## 3. Error Analysis
On the Stroke test set (N=1022):
- **False Negatives:** 11 (These are critical as patients with stroke risk are missed). Needs optimization of recall threshold.
- **False Positives:** 220 (High false positives lead to alert fatigue but are generally safer in early screening).

## 4. Prediction Reliability
- **Brier Score:** 0.1335 (Measures probability calibration; lower is better, <0.1 is very good).
- The ROC curve plot is saved in `reports/figures/roc_curve_reliability.png`.

