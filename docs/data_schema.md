# Dataset Schema — Invisor.ai (Phase 1)

## 1. Dataset Overview

This CSV dataset is used as the single input source for:
- Churn prediction
- Customer segmentation
- Explainable AI
- Dashboard visualizations
- Insight-based chatbot

Each row represents one customer.

---

## 2. Required Columns (Mandatory)

These columns must be present in the uploaded CSV.

| Column Name | Data Type | Allowed Values | Description |
|------------|-----------|----------------|-------------|
| customer_id | String | Unique value | Unique identifier for each customer |
| tenure_months | Integer | >= 0 | Number of months the customer has stayed |
| monthly_charges | Float | >= 0 | Monthly billing amount |
| total_charges | Float | >= 0 | Total amount charged |
| contract_type | Categorical | Month-to-month, One year, Two year | Contract duration |
| payment_method | Categorical | Electronic check, Credit card, Bank transfer, Mailed check | Payment method |
| churn | Binary | 0/1, Yes/No, true/false | Target variable |

---

## 3. Optional Columns (Recommended)

Optional columns improve model quality and explainability.
Missing optional columns must NOT break the pipeline.

| Column Name | Data Type | Allowed Values | Usage |
|------------|-----------|----------------|-------|
| gender | Categorical | Male, Female, Other | Demographic segmentation |
| senior_citizen | Binary | 0/1, Yes/No | Churn risk modifier |
| partner | Binary | Yes/No | Household stability |
| dependents | Binary | Yes/No | Household stability |
| internet_service | Categorical | DSL, Fiber optic, None | Service usage |
| online_security | Binary | Yes/No | Engagement proxy |
| online_backup | Binary | Yes/No | Engagement proxy |
| tech_support | Binary | Yes/No | Service stickiness |
| streaming_tv | Binary | Yes/No | Usage behavior |
| streaming_movies | Binary | Yes/No | Usage behavior |
| paperless_billing | Binary | Yes/No | Billing behavior |

---

## 4. Data Type Definitions

### Numeric
- Integer: whole numbers
- Float: decimal numbers
- Missing values allowed and handled in preprocessing

### Binary
Accepted formats:
- Yes / No
- 0 / 1
- true / false

Internally normalized to:
- 1 = Yes / True
- 0 = No / False

### Categorical
- Stored as strings
- Encoded during preprocessing
- Unknown categories handled safely

---

## 5. Missing Values Policy

| Column Type | Missing Allowed | Handling |
|------------|-----------------|----------|
| Required | Yes (except customer_id) | Imputed |
| Optional | Yes | Ignored or imputed |
| customer_id | No | File rejected |

---

## 6. Backend Validation Rules

1. File must be CSV
2. All required columns must exist
3. churn must be binary
4. customer_id must not be null

---

## 7. Sample Dataset

Sample CSV file location:

docs/sample-data/sample_customer_churn.csv
