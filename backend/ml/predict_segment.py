import pandas as pd

def predict_segments(
    df: pd.DataFrame,
    model_artifact: dict,
    model_version: str = "kmeans_segmentation_v1"
) -> pd.DataFrame:
    """
    Assign customer segments using a trained clustering pipeline.

    Parameters
    ----------
    df : pd.DataFrame
        Input customer data (raw CSV)
    model_artifact : dict
        Loaded segmentation_model.pkl artifact
    model_version : str
        Version identifier

    Returns
    -------
    pd.DataFrame
        customer_id, segment_label, model_version
    """

    # -------------------------
    # Defensive copy
    # -------------------------
    df = df.copy()

    # -------------------------
    # Preserve customer_id
    # -------------------------
    if "customer_id" not in df.columns:
        raise ValueError("customer_id column is required")

    customer_ids = df["customer_id"].values

    # -------------------------
    # Load pipeline
    # -------------------------
    pipeline = model_artifact["pipeline"]

    # -------------------------
    # Predict segments
    # -------------------------
    segment_labels = pipeline.predict(df)

    # -------------------------
    # Stable output schema
    # -------------------------
    return pd.DataFrame({
        "customer_id": customer_ids,
        "segment_label": segment_labels,
        "model_version": model_version
    })
