# Chatbot Response Format

## Overview
This document defines the standard response format for the Invisor.ai
chatbot. The chatbot provides text-only, insight-based summaries derived
from existing machine learning outputs.

---

## Response Principles
- Text-only responses
- Clear and non-technical language
- No ML or statistical jargon
- Deterministic structure per query type

---

## Supported Response Formats

### Plain Insight Summary
Used for general summaries and explanations.

Structure:
- One short headline sentence
- One or two explanatory sentences

---

### Structured Insight Summary
Used for ranked or comparative insights.

Structure:
- One-line summary
- Bullet list of key points

---

## Language Constraints
The chatbot avoids technical ML terminology and uses simple business
language focused on clarity and trust.

---

## Fallback Responses
For unsupported queries, the chatbot provides a polite message explaining
its scope and suggests supported topics.
