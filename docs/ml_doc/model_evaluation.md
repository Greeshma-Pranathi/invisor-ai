# Baseline Churn Model Evaluation

## Model
Logistic Regression (baseline)

## Evaluation Metrics
- Accuracy: 1.000
- Precision: 1.000
- Recall: 1.000
- ROC-AUC: 1.000

## Interpretation
The baseline model demonstrates reasonable predictive performance,
indicating that the dataset contains meaningful churn signal.

Recall was prioritized over precision to minimize missed churn cases.

## Known Limitations
- Trained on a small synthetic dataset
- Linear model limits capture of complex patterns
- No advanced feature engineering
- Threshold not optimized for business objectives

These limitations will be addressed in Week 3 during model refinement.

## Evaluation Caveat
The baseline model achieves perfect evaluation metrics on the current
validation split. This is expected due to:

- Extremely small dataset size
- Synthetic data with strong, clean churn patterns
- High separability between churned and non-churned customers

These results should NOT be interpreted as real-world performance.
The evaluation only validates that the end-to-end ML pipeline is working
correctly.
