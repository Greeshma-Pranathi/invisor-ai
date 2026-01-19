# Final Churn Model – ML Decisions

## 1. Final Model Choice

**Selected Model:** Random Forest Classifier

### Justification
The Random Forest model was selected as the final churn prediction model because:

- It captures non-linear relationships and feature interactions
- It is robust to noise and missing values
- It performs well on small-to-medium tabular datasets
- It requires minimal hyperparameter tuning compared to more complex models
- It avoids additional external dependencies (e.g., XGBoost) for the MVP

XGBoost was considered as a future enhancement but deferred to prioritize
simplicity, stability, and delivery timelines.

---

## 2. Feature List

### Raw Input Features (from CSV)

**Numeric Features**
- senior_citizen
- tenure_months
- monthly_charges
- total_charges
- avg_monthly_usage_gb
- support_tickets_last_6m
- late_payments_last_year

**Categorical Features**
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

**Excluded Features**
- customer_id (identifier only)
- churn (target variable)

---

## 3. Engineered Features (Preprocessing Only)

The following interaction features are generated inside the preprocessing
pipeline and are not part of the raw CSV:

- charges_per_month = total_charges / tenure_months
- tickets_per_month = support_tickets_last_6m / tenure_months
- usage_per_charge = avg_monthly_usage_gb / monthly_charges

These features capture rate-based customer behavior and improve model robustness.

---

## 4. Preprocessing Summary

- Numeric features:
  - Median imputation
  - Standard scaling
- Categorical features:
  - Most-frequent imputation
  - One-hot encoding
  - Unknown categories handled safely
- Feature engineering applied before column transformation
- Separate preprocessing pipelines maintained for baseline and refined models

---

## 5. Class Imbalance Handling

- Dataset refined to reflect realistic churn imbalance (~25%)
- Stratified train/validation split used
- SMOTE oversampling applied to training data only
- Validation data left untouched
- Class weighting retained in the model

---

## 6. Performance Summary

### Evaluation Setup
- Dataset: sample_customer_churn_v2.csv
- Validation strategy: 80/20 hold-out split (stratified)
- Evaluation performed on unseen data

### Final Metrics
- ROC-AUC: 1.00
- Precision: 1.00
- Recall: 1.00
- F1-score: 1.00

### Interpretation
Perfect metrics were observed due to the synthetic nature of the dataset,
limited sample size, and strong feature separability. These results confirm
pipeline correctness rather than real-world performance expectations.

---

## 7. Known Limitations

- Dataset is synthetic and limited in size
- Evaluation metrics are not representative of production performance
- Model may overfit structured synthetic patterns
- No temporal or longitudinal customer behavior included
- No external validation dataset available

These limitations will be addressed in future iterations using
larger, real-world datasets and more rigorous evaluation strategies.

---

## 8. Future Improvements

- Train and compare XGBoost as an alternative model
- Introduce cross-validation
- Add threshold optimization based on business costs
- Incorporate temporal churn signals
- Perform explainability analysis (SHAP) for customer-level insights
