# Customer Segmentation – Model Training

## Objective
Train a clustering-based model to assign customers into behavioral segments.

## Algorithm
K-Means clustering was trained on preprocessed customer data.

## Preprocessing
- Missing values imputed
- Categorical features one-hot encoded
- Numerical features standardized

## Model Configuration
- Number of clusters: 4
- Initialization: k-means++
- Random state fixed for reproducibility

## Outputs
- Customer segment labels stored in customer_segments.csv
- Trained model and preprocessing pipeline saved as segmentation_model.pkl

## Evaluation
Silhouette score was used as a coarse measure of cluster quality to
ensure reasonable separation between segments.
