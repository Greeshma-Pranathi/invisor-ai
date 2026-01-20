# Invisor.ai – Backend Validation Rules (Phase 1)

This document defines the backend validation rules for Phase 1 of Invisor.ai.
The goal is to ensure clean data ingestion, safe ML inference, predictable API
behavior, and demo-ready reliability—without introducing enterprise-level
complexity.

---

## 1. General API-Level Validation (All Endpoints)

### Request Validation
- Accept only JSON payloads (`applicationjson`)  
  - Exception CSV upload endpoint (`multipartform-data`)
- Reject empty request bodies
- Enforce strict request schema validation using Pydantic
- Reject unexpected or extra fields
- Validate `Content-Type` header explicitly

### Response Validation
All API responses must follow this standard structure

```json
{
  status success  error,
  message human readable summary,
  data {}
}


2. CSV Upload Endpoint (`/upload-csv`)

This endpoint handles CSV file uploads for model training and data ingestion.
It enforces strict file- and content-level validation while allowing flexibility
for exploratory data analysis.

---

2.1 File-Level Validation

- Accept **only `.csv` files**
- Reject **empty files**
- Reject **corrupted or non-CSV files**
- Enforce a **maximum file size of 10 MB**

---

2.2 CSV Content Validation

- CSV **must contain a header row**
- CSV **must contain at least one data row**
- Reject **duplicate column names**
- Trim **leading and trailing whitespace** from column names

---

2.3 Required Columns

The following columns are mandatory:

- `customer_id`
- **Churn target column** *(required for training mode only)*

Notes
- Extra columns are **allowed**
- Extra columns are **logged for visibility** but **not rejected**

---

2.4 Data Quality Checks *(Warnings Only)*

The following checks generate **warnings** but **do not block processing**:

- Completely empty columns
- Columns with **more than 90% missing values**

---

2.5 Storage Validation & Success Response

After a successful upload, the system returns metadata about the stored file:

```json
{
  "file_id": "uuid",
  "row_count": n,
  "column_count": m
}

3. Churn Prediction Endpoint (`/predict-churn`)

This endpoint performs churn inference on previously uploaded and processed
customer data using the trained churn prediction model.

---

3.1 Validation Rules

- Validate that `file_id` **exists**
- Reject **missing, invalid, or unprocessed** files
- Apply the **same preprocessing pipeline** used during training
- Ensure the **churn model artifact exists** before inference

---

3.2 Output Validation

- `churn_probability` must be in the range **[0, 1]**
- `churn_label` must be one of **{0, 1}**
- Generate **exactly one prediction per customer**

---

4. Explainability Endpoint (`/explain-churn`)

This endpoint provides model explainability outputs for churn predictions,
supporting both customer-level and global insights.

---

4.1 Validation Rules

- Validate both `file_id` and `customer_id`
- Reject requests if **churn predictions have not yet been generated**
- Limit **top N features** for global explanations
- Ensure explanation output **aligns with the prediction schema**

---

5. Customer Segmentation Endpoint (`/segment-customers`)

This endpoint segments customers using an unsupervised clustering model
to support behavioral and risk-based analysis.

---

5.1 Validation Rules

- Reject input if the **churn target column is included**
- Validate that the **clustering model artifact exists**
- Ensure **exactly one segment per customer**
- Segment labels must be **deterministic** for the same input data

---

6. Chatbot Endpoint (`/chatbot/query`)

This endpoint enables natural language interaction over generated insights
while enforcing strict safety and reliability constraints.

---

6.1 Validation Rules

- Question must be **non-empty**
- Maximum question length: **500 characters**
- Responses must be **text-only**
- Reject **hallucinated or unsupported insights**
- Gracefully handle **unsupported or ambiguous queries**

---

7. Security & Safety (Phase 1)

Security measures are intentionally minimal for Phase 1 while ensuring
basic system safety.

- **No authentication or authorization** *(explicit Phase 1 decision)*
- Sanitize **uploaded filenames**
- Prevent **path traversal attacks**
- Sanitize all **user-provided text input**
- Do **not execute or evaluate** user-provided content

---

8. Performance & Stability

To maintain demo-ready reliability, the following safeguards are applied:

- Apply request timeouts for:
  - Model inference
  - Explainability computation
- Cache outputs per `file_id` **where feasible**
- Apply **basic throttling** if needed to protect system stability

---

9. Logging & Observability

The system maintains lightweight logging for debugging and demo support.

Logged Fields
- Endpoint name
- `file_id`
- Timestamp

Logging Rules
- **Never log raw customer data**
- Logs are used **only for debugging and demo support**
