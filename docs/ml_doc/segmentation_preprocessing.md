# Customer Segmentation – Data Preprocessing

## Objective
Prepare customer data for clustering by handling missing values,
encoding categorical features, and scaling numerical features.

## Missing Value Handling
- Numerical features: median imputation
- Categorical features: most frequent value imputation
- No rows are dropped during preprocessing

## Categorical Encoding
- One-hot encoding applied to all categorical features
- Unknown categories handled safely

## Feature Scaling
- StandardScaler applied to numerical features
- Ensures equal contribution of all features to distance calculations

## Output
The preprocessing pipeline produces a fully numerical, normalized
feature matrix suitable for clustering algorithms.
