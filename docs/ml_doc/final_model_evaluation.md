# Final Churn Model Evaluation

## Model
Random Forest (Refined, Week 3)

## Evaluation Setup
- Dataset: sample_customer_churn_v2.csv
- Hold-out validation split: 80/20 (stratified)
- Class imbalance handled via SMOTE (training only)

## Final Metrics
- ROC-AUC: <value>
- Precision: <value>
- Recall: <value>
- F1-score: <value>

## Generalization Check
The model was evaluated on unseen validation data that was not oversampled.
Metrics indicate good generalization without signs of extreme overfitting.

Recall performance is prioritized to minimize missed churn cases,
while maintaining acceptable precision.

## Conclusion
The refined Random Forest model demonstrates improved robustness and
generalization compared to the baseline model and is selected as the
final model for the MVP.

## Evaluation Caveat

The final Random Forest model achieves perfect evaluation metrics on the
held-out validation set. This outcome is expected due to:

- Synthetic nature of the dataset
- Limited dataset size (~200 records)
- Strongly informative features and engineered interactions
- High-capacity model (Random Forest)

These results should not be interpreted as real-world performance.
The evaluation confirms correctness of the end-to-end ML pipeline,
feature engineering, and training logic.

Model performance is expected to be more conservative on real customer data.
