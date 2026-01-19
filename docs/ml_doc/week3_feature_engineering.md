# Week 3 – Feature Engineering Improvements

## Dataset Update
The dataset was expanded to 200 records with realistic churn imbalance,
missing values, and noise to reduce trivial separability.

## Feature Importance Review
Feature importance analysis on the refined dataset shows that tenure,
contract type, pricing, and customer friction remain strong drivers,
but no single feature dominates completely.

## Feature Engineering Decisions
- Retained all baseline features
- Added interaction features:
  - charges_per_month
  - tickets_per_month
  - usage_per_charge
- No raw CSV features were removed or added

## Class Imbalance Handling

The refined dataset exhibits realistic churn imbalance.
To address this:

- Stratified train/validation split is used
- SMOTE oversampling is applied to training data only
- Validation data remains untouched
- Class weights are retained in the model

This improves recall for churn customers without data leakage.

## Preprocessing Refinement
- Existing imputation, encoding, and scaling retained
- Interaction feature generation added to preprocessing pipeline
- No schema changes introduced

## Pipeline Versioning Note

Baseline and refined models use separate preprocessing pipelines.
The baseline pipeline is frozen to ensure reproducibility,
while the refined pipeline introduces additional feature engineering.

This prevents accidental regression and ensures fair comparison.
