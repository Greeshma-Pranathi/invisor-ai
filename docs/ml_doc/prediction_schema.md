# Prediction Output Schema

## Overview
The churn prediction model outputs both a probability score and a binary
churn label for each customer. Customer identifiers are preserved to ensure
row-level traceability.

## Output Fields

| Field | Type | Description |
|----|----|----|
| customer_id | string | Identifier from input CSV |
| churn_probability | float | Probability of churn (0–1) |
| churn_label | integer | Binary churn prediction (0 or 1) |
| model_version | string | Identifier of the model used |

## Decision Logic
The churn label is derived using a default threshold of 0.5:


Threshold tuning may be performed in future iterations without changing
the output schema.

## Notes
- One output row corresponds to one input customer
- Output schema is model-agnostic and stable across versions

