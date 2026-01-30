import os
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from ml.segmentation_config import NUMERIC_FEATURES, CATEGORICAL_FEATURES
from ml.preprocessing_segmentation import build_segmentation_preprocessor

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "..", "ml_data", "sample_customer_churn_v2.csv"
)

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(DATA_PATH)

X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]

# -------------------------
# Preprocessing (evaluation only)
# -------------------------
preprocessor = build_segmentation_preprocessor(
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES
)

X_processed = preprocessor.fit_transform(X)

# -------------------------
# Evaluate different K values
# -------------------------
results = []

for k in range(2, 9):
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X_processed)
    sil = silhouette_score(X_processed, labels)

    cluster_sizes = pd.Series(labels).value_counts(normalize=True)

    results.append({
        "k": k,
        "silhouette_score": sil,
        "min_cluster_pct": cluster_sizes.min(),
        "max_cluster_pct": cluster_sizes.max()
    })

results_df = pd.DataFrame(results)

print("\nSegmentation Evaluation Summary")
print("--------------------------------")
print(results_df)
