def interpret_query(query: str, customer_selected: bool = False) -> str:
    """
    Determine chatbot intent using keyword-based matching.
    Returns one of the supported intent codes.
    """

    q = query.lower()

    # Customer-level churn explanation
    if customer_selected and any(k in q for k in [
        "this customer",
        "why is this customer",
        "explain churn"
    ]):
        return "CHURN_CUSTOMER"

    # Segment-level churn
    if any(k in q for k in [
        "segment churn",
        "churn by segment",
        "highest churn"
    ]):
        return "SEGMENT_CHURN"

    # Churn drivers
    if any(k in q for k in [
        "features influence churn",
        "drivers of churn",
        "why churn",
        "influence churn"
    ]):
        return "CHURN_DRIVERS"

    # Overall churn
    if any(k in q for k in [
        "churn",
        "at risk",
        "likely to churn"
    ]):
        return "CHURN_OVERVIEW"

    # Explain specific segment
    if any(k in q for k in [
        "explain segment",
        "segment 1",
        "segment 2",
        "segment 3",
        "segment 4"
    ]):
        return "SEGMENT_EXPLAIN"

    # Segment distribution
    if any(k in q for k in [
        "segment distribution",
        "how many in each segment",
        "largest segment"
    ]):
        return "SEGMENT_DISTRIBUTION"

    # Segment overview
    if any(k in q for k in [
        "segments",
        "customer segments",
        "groups"
    ]):
        return "SEGMENT_OVERVIEW"

    # Dataset summary
    if any(k in q for k in [
        "dataset",
        "how many customers",
        "data size"
    ]):
        return "DATASET_SUMMARY"

    return "UNSUPPORTED"
