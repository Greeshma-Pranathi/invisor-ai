# Customer Segmentation – Evaluation

## Objective
Evaluate clustering quality and determine an appropriate number of
customer segments.

## Metrics Used
- Silhouette score to measure cluster separation
- Cluster size distribution to assess balance

## Evaluation Results
Multiple values of K (2–8) were evaluated.

The final number of clusters was selected based on:
- Acceptable silhouette score (>0.25)
- Reasonable balance between cluster sizes
- Interpretability of resulting segments

## Final Selection
The chosen number of clusters provides a good trade-off between
separation quality and business usability.

## Notes
Clustering metrics are heuristic and should be interpreted alongside
domain knowledge and segment interpretability.

## Final Cluster Selection

Based on silhouette scores and cluster size distribution, K=4 was selected
as the final number of customer segments.

While K=2 and K=3 achieved slightly higher silhouette scores, they resulted
in overly dominant clusters with limited business interpretability.
Higher values of K (6–8) produced very small clusters (<5%), indicating
over-fragmentation.

K=4 provides a strong balance between cluster separation (silhouette ≈ 0.48),
size balance, and interpretability, making it suitable for an MVP customer
segmentation system.
