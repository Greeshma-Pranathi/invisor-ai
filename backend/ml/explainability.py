import pandas as pd
import shap
import numpy as np


def explain_customer(customer_id, df, model_pipeline, top_n: int = 5):
    """
    Generate local SHAP explanation for a single customer.

    Parameters
    ----------
    customer_id : str
    df : pd.DataFrame
        Raw input dataframe
    model_pipeline : sklearn.pipeline.Pipeline
        Trained churn model pipeline
    top_n : int
        Number of top contributing features to return

    Returns
    -------
    pd.DataFrame
        Columns: customer_id, feature, contributions
    """

    # -------------------------
    # Locate customer
    # -------------------------
    row = df[df["customer_id"] == customer_id]
    if row.empty:
        raise ValueError(f"Customer {customer_id} not found")

    # -------------------------
    # Prepare features
    # -------------------------
    X = row.drop(columns=["customer_id", "churn"], errors="ignore")

    # -------------------------
    # Extract pipeline components
    # -------------------------
    preprocessing_pipeline = model_pipeline.named_steps["preprocessing"]
    classifier = model_pipeline.named_steps["classifier"]

    # -------------------------
    # Transform input
    # -------------------------
    X_processed = preprocessing_pipeline.transform(X)

    # -------------------------
    # Feature names (from ColumnTransformer only)
    # -------------------------
    column_transformer = preprocessing_pipeline.named_steps["preprocessor"]
    feature_names = column_transformer.get_feature_names_out()

    # -------------------------
    # SHAP explanation
    # -------------------------
    explainer = shap.TreeExplainer(classifier)
    shap_values = explainer.shap_values(X_processed)

    # Binary classification safety
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    if shap_values.ndim == 3:
        shap_row = shap_values[0, :, 1]
    else:
        shap_row = shap_values[0]

    # -------------------------
    # Build DataFrame
    # -------------------------
    local_df = pd.DataFrame({
        "customer_id": customer_id,
        "feature": feature_names,
        "contributions": shap_row
    })

    # -------------------------
    # Sort by importance & keep top N
    # -------------------------
    local_df["abs_contribution"] = local_df["contributions"].abs()
    local_df = (
        local_df
        .sort_values("abs_contribution", ascending=False)
        .head(top_n)
        .drop(columns="abs_contribution")
        .reset_index(drop=True)
    )

    return local_df
