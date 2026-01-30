def interpret_query(query: str, customer_selected: bool = False) -> str:
    q = query.lower()

    if customer_selected and any(k in q for k in [
        "this customer",
        "why is this customer",
        "explain churn"
    ]):
        return "CHURN_CUSTOMER"

    if any(k in q for k in [
        "segment churn",
        "churn by segment",
        "highest churn"
    ]):
        return "SEGMENT_CHURN"

    if any(k in q for k in [
        "drivers of churn",
        "why churn",
        "influence churn"
    ]):
        return "CHURN_DRIVERS"

    if any(k in q for k in [
        "explain segment"
    ]):
        return "SEGMENT_EXPLAIN"

    if any(k in q for k in [
        "segment distribution",
        "how many in each segment",
        "largest segment"
    ]):
        return "SEGMENT_DISTRIBUTION"

    if any(k in q for k in [
        "segments",
        "customer segments",
        "groups"
    ]):
        return "SEGMENT_OVERVIEW"

    if any(k in q for k in [
        "dataset",
        "how many customers",
        "data size"
    ]):
        return "DATASET_SUMMARY"

    if any(k in q for k in [
        "churn",
        "at risk",
        "likely to churn"
    ]):
        return "CHURN_OVERVIEW"

    return "UNSUPPORTED"
