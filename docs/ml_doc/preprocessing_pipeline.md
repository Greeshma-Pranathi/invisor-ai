# Data Preprocessing Pipeline

## Overview
A unified preprocessing pipeline is used for both training and inference
to ensure consistency and prevent data leakage.

## Missing Value Handling
- Numeric features: median imputation
- Categorical features: most frequent value imputation

## Categorical Encoding
- One-hot encoding
- Unknown categories handled safely using handle_unknown="ignore"

## Feature Scaling
- Numeric features scaled using StandardScaler
- Required for baseline Logistic Regression model

## Implementation Notes
- Implemented using sklearn ColumnTransformer and Pipeline
- Same pipeline will be reused during model inference via backend APIs

## Model Compatibility Note

The preprocessing pipeline is model-agnostic and designed to work with
both linear (Logistic Regression) and tree-based models (Random Forest, XGBoost).

Although scaling is not required for tree-based models, it is retained
to ensure compatibility with linear models and to keep a single,
consistent preprocessing pipeline across experiments.
