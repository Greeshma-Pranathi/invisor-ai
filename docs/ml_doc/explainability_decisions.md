# Explainability Technique Selection

## Selected Method
SHAP (SHapley Additive exPlanations)

## Model Context
The final churn prediction model is a Random Forest classifier trained
on tabular customer data with engineered and categorical features.

## Justification
SHAP was selected because it provides:

- Global explanations to identify overall churn drivers
- Local explanations to interpret individual customer predictions
- Model-specific support via TreeExplainer for Random Forest
- Additive, consistent, and directionally meaningful explanations

Built-in Random Forest feature importance was not sufficient, as it
only provides global importance and lacks per-customer interpretability.

## Explanation Scope
- Global explanations: feature impact across the dataset
- Local explanations: feature contribution per customer

This approach enables transparent, customer-level churn interpretation
required for the explainable AI phase.
