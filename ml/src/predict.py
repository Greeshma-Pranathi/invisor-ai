import pandas as pd
import joblib

def predict_churn(df, model_artifact, model_version="random_forest_v1"):
    """
    Generate churn predictions with a stable output schema.
    """

    # Extract customer_id (must be preserved)
    customer_ids = df["customer_id"].values

    # Prepare features
    X = df.drop(columns=["customer_id"])

    preprocessor = model_artifact["preprocessor"]
    model = model_artifact["model"]

    # Preprocess
    X_processed = preprocessor.transform(X)

    # Predictions
    churn_prob = model.predict_proba(X_processed)[:, 1]
    churn_label = (churn_prob >= 0.5).astype(int)

    # Output schema
    output = pd.DataFrame({
        "customer_id": customer_ids,
        "churn_probability": churn_prob,
        "churn_label": churn_label,
        "model_version": model_version
    })

    return output
