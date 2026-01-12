# Explainability Output Schema

## Overview
This document defines the structured output schema for explainable AI
used in the churn prediction system. The schema supports both global
and local explanations and is designed for backend and frontend
consumption.

---

## Global Explainability Schema

Global explanations describe feature influence across the entire dataset.

### Fields
- explanation_type: "global"
- model_version: string
- generated_at: timestamp
- features: list of feature contributions

Each feature entry contains:
- feature_name
- mean_contribution (mean absolute SHAP value)

---

## Local Explainability Schema

Local explanations describe why a specific customer received a churn
prediction.

### Fields
- explanation_type: "local"
- customer_id
- model_version
- base_value
- prediction_probability
- features: list of signed feature contributions

Each feature entry contains:
- feature_name
- contribution (positive or negative SHAP value)

---

## Global vs Local Distinction

Global explanations are aggregated and unsigned, intended for identifying
overall churn drivers. Local explanations are per-customer, signed, and
used for user-facing interpretability.

Natural language explanations are generated downstream and are not part
of the ML explainability schema.
