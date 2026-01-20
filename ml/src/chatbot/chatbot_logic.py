from intent_detection import interpret_query
from insight_templates import (
    churn_overview_template,
    churn_drivers_template,
    customer_churn_template,
    segment_explain_template,
    segment_distribution_template
)
from fallback import fallback_response


def chatbot_response(
    query: str,
    cached_outputs: dict,
    customer_selected: bool = False,
    selected_customer_id: str = None
) -> str:
    """
    Main chatbot entry point.
    """

    intent = interpret_query(query, customer_selected)

    if intent == "CHURN_OVERVIEW":
        return churn_overview_template(cached_outputs["churn"])

    if intent == "CHURN_DRIVERS":
        return churn_drivers_template(cached_outputs["global_explain"])

    if intent == "CHURN_CUSTOMER" and selected_customer_id:
        return customer_churn_template(
            cached_outputs["local_explain"],
            selected_customer_id
        )

    if intent == "SEGMENT_EXPLAIN":
        segment_id = extract_segment_id(query)
        return segment_explain_template(
            segment_id,
            cached_outputs["segment_descriptions"]
        )

    if intent == "SEGMENT_DISTRIBUTION":
        return segment_distribution_template(
            cached_outputs["segment_counts"]
        )

    return fallback_response()


def extract_segment_id(query: str):
    for token in query.split():
        if token.isdigit():
            return int(token)
    return None
