Target Variable (churn)
- Column name: churn
- Description: Indicates whether the customer has left the service
- Original values: Yes / No
- Encoding: Yes → 1, No → 0
- Notes: Synthetic churn column added for demo purposes

Dataset Expansion Notes
- Dataset is synthetic and expanded for demo purposes
- Columns added to improve churn signal and explainability
- No real customer data used

### Numeric Features
- senior_citizen
- tenure_months
- monthly_charges
- total_charges
- avg_monthly_usage_gb
- support_tickets_last_6m
- late_payments_last_year

All numeric features are valid behavioral or demographic indicators.

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

### Excluded Columns
- customer_id (identifier, not predictive)

### Missing Values Analysis
- No missing values detected in the current dataset
- Dataset is synthetically generated
- Missing value handling will still be implemented in preprocessing pipeline for robustness

## Missing Value Handling (Planned)

Although the current sample dataset contains no missing values,
the preprocessing pipeline will include missing value handling
to ensure robustness for real user-uploaded CSV files.

Planned strategy:
- Numeric features: median imputation
- Categorical features: most frequent value imputation
- Columns with excessive missing values (>30%): excluded from modeling


