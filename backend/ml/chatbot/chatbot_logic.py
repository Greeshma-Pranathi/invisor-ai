from ml.chatbot.intent_detection import interpret_query
from ml.chatbot.insight_templates import (
    churn_overview_template,
    churn_drivers_template,
    customer_churn_template,
    segment_explain_template,
    segment_distribution_template,
    segment_churn_template,
    dataset_summary_template
)
from ml.chatbot.fallback import fallback_response


def chatbot_response(
    query: str,
    cached_outputs: dict | None,
    customer_selected: bool = False,
    selected_customer_id: str | None = None
) -> str:

    if not cached_outputs:
        return "Please upload data to begin analysis."

    if not query or not isinstance(query, str):
        return "Please ask a question about the data."

    query = query.strip()
    query_lower = query.lower()

    intent = interpret_query(query, customer_selected)

    # -------------------------
    # Churn
    # -------------------------
    if intent == "CHURN_OVERVIEW":
        return churn_overview_template(cached_outputs["churn"])

    if intent == "CHURN_DRIVERS":
        if cached_outputs.get("global_explain") is None:
            return "Churn drivers are not available yet."
        return churn_drivers_template(cached_outputs["global_explain"])

    if intent == "CHURN_CUSTOMER":
        if not customer_selected or not selected_customer_id:
            return "Please select a customer to get a customer-specific explanation."
        if cached_outputs.get("local_explain") is None:
            return "Customer-level explanation could not be generated for this customer."
        return customer_churn_template(
            cached_outputs["local_explain"],
            selected_customer_id
        )

    # -------------------------
    # Segmentation
    # -------------------------
    if intent == "SEGMENT_EXPLAIN":
        segment_id = extract_segment_id(query)
        if segment_id is None:
            return "Please specify which segment you want explained (e.g., segment 1)."
        segment_desc = cached_outputs.get("segment_descriptions", {})
        return segment_explain_template(segment_id, segment_desc)

    if intent in ("SEGMENT_DISTRIBUTION", "SEGMENT_OVERVIEW"):
        return segment_distribution_template(
            cached_outputs["segment_counts"]
        )

    if intent == "SEGMENT_CHURN":
        return segment_churn_template(
            cached_outputs["segment_churn"]
        )

    # -------------------------
    # Dataset
    # -------------------------
    if intent == "DATASET_SUMMARY":
        return dataset_summary_template(
            cached_outputs["dataset_summary"]
        )

    # -------------------------
    # True fallback
    # -------------------------
    return fallback_response()


def extract_segment_id(query: str):
    for token in query.split():
        if token.isdigit():
            return int(token)
    return None
