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

OPTIONAL_COLUMNS = {"churn"}


def predict_churn(
    df: pd.DataFrame,
    model_pipeline,
    model_version: str = "random_forest_v1"
) -> pd.DataFrame:
    """
    Generate churn predictions using a trained sklearn Pipeline.
    """

    # -------------------------
    # Validate input
    # -------------------------
    if "customer_id" not in df.columns:
        raise ValueError("customer_id column is required")

    customer_ids = df["customer_id"].astype(str).values

    # -------------------------
    # Prepare features
    # -------------------------
    X = df.drop(columns=["customer_id", "churn"], errors="ignore")

    # -------------------------
    # Predict via pipeline
    # -------------------------
    churn_prob = model_pipeline.predict_proba(X)[:, 1]
    churn_label = (churn_prob >= 0.5).astype(int)

    # -------------------------
    # Output schema
    # -------------------------
    return pd.DataFrame({
        "customer_id": customer_ids,
        "churn_probability": churn_prob,
        "churn_label": churn_label,
        "model_version": model_version
    })
