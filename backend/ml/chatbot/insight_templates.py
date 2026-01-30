def churn_overview_template(churn_df):
    total = len(churn_df)
    high_risk = (churn_df["churn_label"] == 1).sum()
    pct = round((high_risk / total) * 100, 1) if total else 0

    return (
        "Here is an overview of churn risk in the dataset.\n\n"
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

    return (
        "Several factors strongly influence churn risk.\n\n"
        f"The most influential factors include {', '.join(top_features)}."
    )


def customer_churn_template(local_explain_df, customer_id):
    df = local_explain_df[local_explain_df["customer_id"] == customer_id]

    top = (
        df.sort_values("contributions", ascending=False)
        .head(2)["feature"]
        .tolist()
    )

    return (
        "This customer shows elevated churn risk.\n\n"
        f"The most important contributing factors are {' and '.join(top)}."
    )


def segment_explain_template(segment_id, segment_descriptions):
    desc = segment_descriptions.get(
        segment_id,
        "a distinct group of customers with shared behavioral patterns"
    )

    return (
        f"Segment {segment_id} represents a specific customer group.\n\n"
        f"These customers typically show patterns such as {desc}."
    )


def segment_distribution_template(segment_counts):
    return (
        "Customers are distributed across multiple segments.\n\n"
        f"Segment sizes: {segment_counts}."
    )


def segment_churn_template(segment_churn):
    return (
        "Churn varies across customer segments.\n\n"
        f"Segment-level churn rates: {segment_churn}."
    )


def dataset_summary_template(summary):
    return (
        "Here is a summary of the uploaded dataset.\n\n"
        f"{summary}"
    )
