import os
import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline

from ml.segmentation_config import NUMERIC_FEATURES, CATEGORICAL_FEATURES
from ml.preprocessing_segmentation import build_segmentation_preprocessor

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "..", "ml_data", "sample_customer_churn_v2.csv"
)
MODEL_DIR = os.path.join(
    BASE_DIR, "..", "ml_models"
)

OUTPUT_PATH = os.path.join(
    MODEL_DIR, "customer_segments.csv"
)
MODEL_PATH = os.path.join(
    MODEL_DIR, "segmentation_model.pkl"
)

os.makedirs(MODEL_DIR, exist_ok=True)

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(DATA_PATH)

customer_ids = df["customer_id"]

X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]

# -------------------------
# Build segmentation pipeline
# -------------------------
N_CLUSTERS = 4  # can be tuned later

pipeline = Pipeline(steps=[
    (
        "preprocessing",
        build_segmentation_preprocessor(
            NUMERIC_FEATURES,
            CATEGORICAL_FEATURES
        )
    ),
    (
        "clustering",
        KMeans(
            n_clusters=N_CLUSTERS,
            random_state=42,
            n_init=10
        )
    )
])

# -------------------------
# Train segmentation model
# -------------------------
cluster_labels = pipeline.fit_predict(X)

# -------------------------
# Evaluate clustering quality
# -------------------------
X_processed = pipeline.named_steps["preprocessing"].transform(X)
sil_score = silhouette_score(X_processed, cluster_labels)

print(f"Silhouette Score (K={N_CLUSTERS}): {sil_score:.3f}")

# -------------------------
# Save segmentation output
# -------------------------
segmented_df = pd.DataFrame({
    "customer_id": customer_ids,
    "segment_label": cluster_labels
})

segmented_df.to_csv(OUTPUT_PATH, index=False)

# -------------------------
# Save model artifact
# -------------------------
joblib.dump(
    {
        "pipeline": pipeline,
        "n_clusters": N_CLUSTERS,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES
    },
    MODEL_PATH
)

print(f"Segmentation model saved to: {MODEL_PATH}")
print(f"Customer segments saved to: {OUTPUT_PATH}")
