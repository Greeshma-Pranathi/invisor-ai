# Chatbot Query → Data Source Mapping

## Overview
This document defines how chatbot queries are mapped to existing machine
learning outputs. The chatbot only summarizes and aggregates precomputed
results and does not perform new analysis.

---

## Churn-Related Queries

| Query Type | Data Source | Fields Used |
|----------|------------|------------|
Which customers are likely to churn? | Churn prediction output | customer_id, churn_label |
How many customers are high risk? | Churn prediction output | churn_label |
What features influence churn most? | Global explainability | feature_name, contribution |
Why is this customer at risk? | Local explainability | feature_name, contribution |

---

## Segmentation Queries

| Query Type | Data Source | Fields Used |
|----------|------------|------------|
What customer segments exist? | Segment metadata | segment_label |
Explain segment N | Segment interpretation notes | static text |
Customers per segment | customer_segments.csv | segment_label |

---

## Combined Insights

| Query Type | Data Sources | Logic |
|----------|-------------|------|
Segment with highest churn risk | Churn + segmentation outputs | Precomputed churn rate |
Churn across segments | Churn + segmentation outputs | Precomputed summary |

---

## Constraints
- No new model inference
- No recomputation of features
- No causal reasoning
- No what-if analysis

All chatbot responses must be derived from existing outputs.
