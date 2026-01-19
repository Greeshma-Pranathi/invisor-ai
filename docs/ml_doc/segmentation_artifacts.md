# Customer Segmentation – Saved Artifacts

## Overview
This document describes the persisted artifacts generated during customer
segmentation model training.

## Segmentation Model Artifact
File: segmentation_model.pkl

Contents:
- Preprocessing pipeline
- Trained K-Means clustering model
- Feature lists used for segmentation
- Number of clusters

This artifact is used to assign segment labels to new customers and ensure
consistent segmentation across runs.

## Customer Segment Mapping
File: customer_segments.csv

Contents:
- customer_id
- segment_label

This file maps each customer to a segment and is used by downstream systems
for analytics, visualization, and business decision-making.

## Notes
Segment labels are numeric identifiers. Business-friendly segment names are
maintained separately in documentation and UI layers.

## Production Inference Interface

File: predict_segment.py

This file provides a stable interface for assigning customer segments
using the trained clustering model. It applies the same preprocessing
pipeline used during training and returns a consistent output schema
for backend and frontend consumption.
