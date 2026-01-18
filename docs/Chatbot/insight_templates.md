# Chatbot Insight Templates

## Overview
This document defines fixed templates used by the Invisor.ai chatbot to
convert machine learning outputs into clear, non-technical insights.

The chatbot uses templates to ensure consistent, reliable, and
hallucination-free responses.

---

## Churn Risk Summary Templates
Used for summarizing overall churn risk and segment-level churn patterns.

Templates reference:
- Customer counts
- Risk labels
- Precomputed summaries

---

## Segment Behavior Summary Templates
Used to explain what each customer segment represents.

Templates reference:
- Segment labels
- Predefined segment interpretations

---

## Feature Importance Explanation Templates
Used to describe which factors influence churn risk most.

Templates reference:
- Ranked feature importance outputs
- Plain-language feature labels

---

## Design Constraints
- Templates must only use existing ML outputs
- No new analysis or reasoning
- No technical ML terminology
