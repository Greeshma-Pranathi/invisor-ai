# Explainability Logic – Churn Prediction Model

## Overview

This document explains how to interpret explainability outputs generated
for the churn prediction model, outlines known limitations of the
explainability approach, and describes how explanations align with the
underlying model behavior.

The explainability system is based on SHAP (SHapley Additive exPlanations)
applied to the final Random Forest churn model.

---

## Interpretation Guide

### 1. Explanation Types

The system provides two types of explanations:

- **Global explanations**
  - Describe which features generally drive churn across the dataset
  - Used for business insights and analytics

- **Local explanations**
  - Describe why a specific customer received a particular churn prediction
  - Used for user-facing interpretability

---

### 2. Interpreting Global Explanations

Global explanations are based on **mean absolute SHAP values**.

Key points:
- Higher values indicate stronger overall influence on churn predictions
- Values are always non-negative
- Global explanations do not show direction (increase vs decrease)

How to read:
- Features at the top of the global ranking are the most important churn drivers
- These features should align with domain expectations (e.g., tenure, contract type)

Global explanations answer:
> “What factors generally influence churn in this customer base?”

---

### 3. Interpreting Local (Customer-Level) Explanations

Local explanations provide **signed feature contributions** for a single customer.

Key points:
- Positive contribution → increases churn risk
- Negative contribution → decreases churn risk
- Larger magnitude → stronger impact

Each local explanation follows the SHAP additivity principle:
# Explainability Logic – Churn Prediction Model

## Overview

This document explains how to interpret explainability outputs generated
for the churn prediction model, outlines known limitations of the
explainability approach, and describes how explanations align with the
underlying model behavior.

The explainability system is based on SHAP (SHapley Additive exPlanations)
applied to the final Random Forest churn model.

---

## Interpretation Guide

### 1. Explanation Types

The system provides two types of explanations:

- **Global explanations**
  - Describe which features generally drive churn across the dataset
  - Used for business insights and analytics

- **Local explanations**
  - Describe why a specific customer received a particular churn prediction
  - Used for user-facing interpretability

---

### 2. Interpreting Global Explanations

Global explanations are based on **mean absolute SHAP values**.

Key points:
- Higher values indicate stronger overall influence on churn predictions
- Values are always non-negative
- Global explanations do not show direction (increase vs decrease)

How to read:
- Features at the top of the global ranking are the most important churn drivers
- These features should align with domain expectations (e.g., tenure, contract type)

Global explanations answer:
> “What factors generally influence churn in this customer base?”

---

### 3. Interpreting Local (Customer-Level) Explanations

Local explanations provide **signed feature contributions** for a single customer.

Key points:
- Positive contribution → increases churn risk
- Negative contribution → decreases churn risk
- Larger magnitude → stronger impact

Each local explanation follows the SHAP additivity principle:
        base_value + sum(feature_contributions) ≈ churn_probability


How to read:
- Identify top positive contributors (primary churn reasons)
- Identify top negative contributors (retention factors)
- Use relative magnitude to prioritize factors

Local explanations answer:
> “Why is this specific customer predicted to churn?”

---

### 4. From Values to User-Facing Explanations

The explainability layer outputs **numerical values only**.

Human-readable explanations (sentences) are generated downstream using:
- Rule-based templates, or
- LLM-powered summarization (optional, post-MVP)

This separation ensures:
- Flexibility in phrasing
- UI and localization control
- Stable ML outputs

---

## Known Limitations

### 1. Model-Based Explanations, Not Causality

SHAP explanations describe:
- How features influence the **model’s prediction**

They do **not** imply:
- Causal relationships
- Real-world guarantees

Example:
- “Support tickets increase churn risk” reflects model behavior, not causation.

---

### 2. Sensitivity to Data Quality

Explainability quality depends on:
- Input data correctness
- Feature engineering quality
- Consistency with training schema

Incorrect or out-of-distribution inputs may lead to misleading explanations.

---

### 3. Synthetic / Limited Dataset Effects

Since the current dataset is synthetic and limited in size:
- Explanations may appear overly clean or decisive
- Real-world data may produce noisier explanations

This does not invalidate the approach but limits real-world generalization.

---

### 4. Computational Cost

- Global explanations are computed offline
- Local explanations are computed on demand

SHAP computation can be expensive for very large datasets, which is why
local explanations are not precomputed for all customers.

---

## Model–Explanation Alignment

### 1. Shared Preprocessing Pipeline

Explanations are generated using:
- The same preprocessing pipeline
- The same feature engineering logic
- The same trained model

This ensures:
- No training–serving skew
- No explanation–prediction mismatch

---

### 2. Feature Space Consistency

- Explanations operate on the transformed feature space
- One-hot encoded features are explained individually
- Feature names are preserved for traceability

---

### 3. Prediction Consistency

Local explanations align numerically with predictions:
- Feature contributions sum to the final churn probability
- Directionality matches prediction behavior

This alignment validates that explanations accurately reflect model logic.

---

## Conclusion

The explainability system provides transparent, consistent, and reliable
insights into churn predictions at both global and customer levels.

By separating numerical explanations from language generation and ensuring
strict alignment with the trained model, the system is suitable for
production use in a user-facing MVP while remaining extensible for future
enhancements.
