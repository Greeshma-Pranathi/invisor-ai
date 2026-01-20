def churn_overview_template(churn_df):
    total = len(churn_df)
    high_risk = (churn_df["churn_label"] == "High").sum()
    pct = round((high_risk / total) * 100, 1) if total > 0 else 0

    return (
        "A portion of customers show a higher risk of churn.\n\n"
        f"Out of {total} customers, {high_risk} ({pct}%) are currently "
        "classified as higher churn risk."
    )


def churn_drivers_template(global_explain_df, top_n=3):
    top_features = (
        global_explain_df
        .sort_values("mean_abs_shap", ascending=False)
        .head(top_n)["feature"]
        .tolist()
    )

    readable = ", ".join(top_features)

    return (
        "A small set of factors strongly influence churn risk.\n\n"
        f"The most influential factors include {readable}."
    )


def customer_churn_template(local_explain_df, customer_id):
    df = local_explain_df[local_explain_df["customer_id"] == customer_id]
    top = (
        df.sort_values("contribution_value", ascending=False)
        .head(2)["feature"]
        .tolist()
    )

    readable = " and ".join(top)

    return (
        "This customer shows a higher risk of churn.\n\n"
        f"Key contributing factors include {readable}, which are commonly "
        "associated with higher churn risk in the dataset."
    )


def segment_explain_template(segment_id, segment_descriptions):
    desc = segment_descriptions.get(
        segment_id,
        "a distinct group of customers with shared behavior patterns"
    )

    return (
        f"Segment {segment_id} represents a distinct group of customers.\n\n"
        f"These customers typically show patterns such as {desc}."
    )


def segment_distribution_template(segment_counts):
    return (
        "Customers are distributed across multiple segments.\n\n"
        "Each segment represents a different customer behavior pattern "
        "within the dataset."
    )
