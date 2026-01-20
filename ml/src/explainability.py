def explain_customer(customer_id, df, artifact):
    """
    Generate local SHAP explanation for a single customer.
    """

    row = df[df["customer_id"] == customer_id]

    if row.empty:
        raise ValueError(f"Customer {customer_id} not found")

    X = row.drop(columns=["customer_id"])

    full_pipeline = artifact["preprocessor"]
    model = artifact["model"]

    feature_engineering = full_pipeline.named_steps["feature_engineering"]
    column_transformer = full_pipeline.named_steps["preprocessor"]

    X_fe = feature_engineering.transform(X)
    X_processed = column_transformer.transform(X_fe)

    feature_names = column_transformer.get_feature_names_out()

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_processed)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, 1]

    return {
        "customer_id": customer_id,
        "features": feature_names.tolist(),
        "contributions": shap_values[0].tolist()
    }
