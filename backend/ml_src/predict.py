import pandas as pd

# -------------------------
# Expected schema (RAW CSV)
# -------------------------
REQUIRED_COLUMNS = {
    "customer_id",
    "gender",
    "senior_citizen",
    "partner",
    "dependents",
    "tenure_months",
    "contract_type",
    "payment_method",
    "monthly_charges",
    "total_charges",
    "internet_service",
    "online_security",
    "tech_support",
    "paperless_billing",
    "streaming_tv",
    "streaming_movies",
    "multiple_lines",
    "avg_monthly_usage_gb",
    "support_tickets_last_6m",
    "late_payments_last_year",
    "autopay_enabled",
    "billing_cycle",
    "region"
}

# churn is OPTIONAL at inference time
OPTIONAL_COLUMNS = {"churn"}

# -------------------------
# Prediction Interface
# -------------------------
def predict_churn(df: pd.DataFrame, model_artifact: dict, model_version="random_forest_v1"):
    """
    Generate churn predictions with a stable output schema.

    Parameters
    ----------
    df : pd.DataFrame
        Input customer data (uploaded CSV as DataFrame)
    model_artifact : dict
        Loaded model artifact containing preprocessor and model
    model_version : str
        Version identifier for the model

    Returns
    -------
    pd.DataFrame
        Predictions with schema:
        customer_id, churn_probability, churn_label, model_version
    """

    # -------------------------
    # Basic validation
    # -------------------------
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns in input CSV: {missing_cols}")

    if "customer_id" not in df.columns:
        raise ValueError("customer_id column is required for prediction output")

    # -------------------------
    # Preserve customer_id
    # -------------------------
    customer_ids = df["customer_id"].astype(str).values

    # -------------------------
    # Prepare features
    # -------------------------
    # Drop identifier and target if present
    drop_cols = ["customer_id"]
    if "churn" in df.columns:
        drop_cols.append("churn")

    X = df.drop(columns=drop_cols)

    # -------------------------
    # Load preprocessing + model
    # -------------------------
    preprocessor = model_artifact["preprocessor"]
    model = model_artifact["model"]

    # -------------------------
    # Preprocess
    # -------------------------
    X_processed = preprocessor.transform(X)

    # -------------------------
    # Predictions
    # -------------------------
    churn_prob = model.predict_proba(X_processed)[:, 1]
    churn_label = (churn_prob >= 0.5).astype(int)

    # -------------------------
    # Output schema
    # -------------------------
    output = pd.DataFrame({
        "customer_id": customer_ids,
        "churn_probability": churn_prob,
        "churn_label": churn_label,
        "model_version": model_version
    })

    return output
