# Week 3 – Baseline Model Performance Review

## Summary of Baseline Results
The baseline Logistic Regression model achieved perfect evaluation metrics
on the validation set. These results validate pipeline correctness but do not
reflect real-world performance.

## Identified Weaknesses

### Overfitting
- Extremely small dataset
- Clean synthetic patterns
- High variance and memorization

### Class Imbalance Limitations
- Synthetic churn distribution does not reflect real-world imbalance
- Limited evaluation of recall–precision trade-offs

### Feature Simplicity and Noise
- Strong, obvious churn signals
- No overlapping or contradictory patterns
- No behavioral noise

### Model Capacity
- Logistic Regression cannot capture non-linear feature interactions
- Model expressiveness is limited for refined prediction

## Conclusion
Baseline results highlight the need for:
- More robust modeling
- Better evaluation strategies
- Increased model capacity
These improvements will be addressed in subsequent Week 3 subtasks.
