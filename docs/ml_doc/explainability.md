# Explainable AI – Churn Model

## Overview

This document describes how explainability is implemented for the churn
prediction model. Explainability enables understanding both:

- Global churn drivers across the customer base
- Local, per-customer reasons behind churn predictions

The implementation uses SHAP (SHapley Additive exPlanations), which provides
consistent and interpretable feature attributions for tree-based models.

---

## Explainability Technique

### Method Used
**SHAP (TreeExplainer)**

### Model Context
- Final model: Random Forest Classifier
- Data type: Tabular customer data
- Features: Numeric + categorical (one-hot encoded)
- Engineered features included via preprocessing pipeline

### Why SHAP
- Supports both global and local explanations
- Provides directionality (increases / decreases churn risk)
- Model-compatible and industry standard
- Additive and consistent explanations

---

## Global Explainability

### Objective
Identify which features most strongly influence churn predictions
across the entire dataset.

### How It Works
- SHAP values are computed for all customers
- Mean absolute SHAP values are calculated per feature
- Features are ranked by overall impact on churn predictions

### Outputs
- `global_feature_importance.csv`
- `global_shap_summary.png`

### Interpretation
- Higher mean absolute SHAP value → stronger global influence
- Positive SHAP values push predictions toward churn
- Negative SHAP values reduce churn likelihood

### Key Global Churn Drivers (Typical)
- Customer tenure
- Contract type (month-to-month)
- Support ticket frequency
- Pricing and usage intensity
- Billing and payment behavior

---

## Local (Customer-Level) Explainability

### Objective
Explain why a specific customer received a particular churn prediction.

### How It Works
- A single customer row is selected dynamically
- SHAP values are computed only for that customer
- Feature contributions are visualized relative to the model’s baseline

### Output
- SHAP waterfall plot for individual customer
- Feature-level contribution values

### Interpretation
- Red features increase churn risk
- Blue features reduce churn risk
- Contributions sum to the final churn probability

---

## Production Explainability Flow

Explainability is generated **on demand** in production.

1. User uploads CSV
2. Model generates churn predictions
3. User selects a specific customer in the UI
4. Backend requests a local explanation for that customer
5. SHAP explanation is computed dynamically and returned

Local explanations are not precomputed for all customers to ensure
scalability and performance.

---

## Notes & Limitations

- Explainability is computed using the same preprocessing and model
  as predictions, ensuring consistency
- SHAP computation may be slower for very large datasets
- Explanations reflect model behavior, not causal relationships
- Synthetic data may produce cleaner explanations than real-world data

---

## Conclusion

The explainability layer provides transparency, trust, and interpretability
for churn predictions at both global and individual customer levels, making
the model suitable for user-facing analysis and decision support.

## Explanation Representation

The explainability layer outputs numerical feature contribution values
(SHAP values). These values indicate how each feature increases or decreases
the churn prediction.

Human-readable explanations are generated downstream using rule-based or
LLM-based interpretation layers. Natural language generation is intentionally
kept outside the ML layer to ensure flexibility, localization, and UI control.
