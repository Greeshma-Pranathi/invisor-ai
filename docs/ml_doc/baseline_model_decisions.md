# Baseline Churn Model — ML Decisions (Phase 1)

## 1. Model Choice Justification

The baseline churn prediction model uses Logistic Regression.

Justification:
- Simple and fast to train
- Well-suited for binary classification
- Highly interpretable and explainable
- Works effectively with one-hot encoded categorical features
- Provides a strong feasibility baseline before introducing more complex models

More advanced models (e.g., Random Forest, XGBoost) are intentionally deferred
to the next phase to avoid premature complexity.

---

## 2. Feature List

### Numeric Features
- senior_citizen
- tenure_months
- monthly_charges
- total_charges
- avg_monthly_usage_gb
- support_tickets_last_6m
- late_payments_last_year

### Categorical Features
- gender
- partner
- dependents
- contract_type
- payment_method
- internet_service
- online_security
- tech_support
- paperless_billing
- streaming_tv
- streaming_movies
- multiple_lines
- autopay_enabled
- billing_cycle
- region

### Excluded Features
- customer_id (identifier, not predictive)
- churn (target variable)

---

## 3. Preprocessing Summary

A unified preprocessing pipeline is applied to both training and inference data.

- Numeric features:
  - Median imputation for missing values
  - Standard scaling

- Categorical features:
  - Most frequent value imputation
  - One-hot encoding
  - Unknown categories handled safely using `handle_unknown="ignore"`

The preprocessing pipeline is implemented using
`sklearn`'s `Pipeline` and `ColumnTransformer` to ensure consistency
and prevent data leakage.

---

## 4. Model Evaluation Summary

The baseline model was evaluated using:
- Accuracy
- Precision
- Recall
- ROC-AUC

Perfect evaluation scores were observed due to:
- Very small dataset size
- Synthetic data with strong churn signal
- High separability between classes

These metrics validate pipeline correctness, not real-world performance.

---

## 5. Known Limitations of Baseline Model

- Trained on a small, synthetic dataset
- Evaluation metrics are not generalizable
- Logistic Regression cannot capture complex non-linear relationships
- No advanced feature engineering or interaction terms
- Default classification threshold (0.5) used
- No cross-validation performed

These limitations will be addressed in Week 3 through
model refinement and evaluation improvements.
