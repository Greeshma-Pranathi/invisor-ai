# Customer Segmentation – Model Selection

## Objective
Select a clustering algorithm suitable for segmenting customers based on
their characteristics and behavior.

## Selected Algorithm
K-Means Clustering

## Justification
K-Means was selected because it:
- Is simple and efficient
- Scales well to larger datasets
- Produces interpretable clusters
- Is widely used for customer segmentation in MVP systems

The algorithm aligns well with standardized numerical features and
one-hot encoded categorical features used in this project.

## Number of Clusters Strategy
The number of clusters will be determined empirically using:
- Elbow method (inertia)
- Silhouette score

Candidate cluster counts will be evaluated in the range of 2 to 8, with
preference given to a small, interpretable number of clusters.

## Alternatives Considered
- Hierarchical clustering: rejected due to scalability concerns
- Gaussian Mixture Models: deferred due to added complexity and lower interpretability

These alternatives may be explored in future iterations.
