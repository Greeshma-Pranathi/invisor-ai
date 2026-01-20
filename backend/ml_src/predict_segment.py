import pandas as pd

def predict_segments(df, model_artifact, model_version="kmeans_segmentation_v1"):
    """
    Assign customer segments using a trained clustering model.

    Parameters
    ----------
    df : pd.DataFrame
        Input customer data (must follow training schema)
    model_artifact : dict
        Loaded segmentation_model.pkl artifact
    model_version : str
        Version identifier for the segmentation model

    Returns
    -------
    pd.DataFrame
        Customer-to-segment mapping
    """

    # -------------------------
    # Preserve customer_id
    # -------------------------
    customer_ids = df["customer_id"].values

    # -------------------------
    # Load artifact components
    # -------------------------
    preprocessor = model_artifact["preprocessor"]
    model = model_artifact["model"]
    numeric_features = model_artifact["numeric_features"]
    categorical_features = model_artifact["categorical_features"]

    # -------------------------
    # Select segmentation features
    # -------------------------
    X = df[numeric_features + categorical_features]

    # -------------------------
    # Preprocess & predict
    # -------------------------
    X_processed = preprocessor.transform(X)
    segment_labels = model.predict(X_processed)

    # -------------------------
    # Stable output schema
    # -------------------------
    output = pd.DataFrame({
        "customer_id": customer_ids,
        "segment_label": segment_labels,
        "model_version": model_version
    })

    return output
