import os
import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from segmentation_config import NUMERIC_FEATURES, CATEGORICAL_FEATURES
from preprocessing_segmentation import build_segmentation_preprocessor

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sample_customer_churn_v2.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
OUTPUT_PATH = os.path.join(MODEL_DIR, "customer_segments.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "segmentation_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(DATA_PATH)

customer_ids = df["customer_id"]

# Select segmentation features explicitly
X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]

# -------------------------
# Preprocessing
# -------------------------
preprocessor = build_segmentation_preprocessor(
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES
)

X_processed = preprocessor.fit_transform(X)

# -------------------------
# Train K-Means
# -------------------------
N_CLUSTERS = 4  # initial choice, can be tuned later

kmeans = KMeans(
    n_clusters=N_CLUSTERS,
    random_state=42,
    n_init=10
)

cluster_labels = kmeans.fit_predict(X_processed)

# -------------------------
# Evaluate clustering quality
# -------------------------
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
artifact = {
    "preprocessor": preprocessor,
    "model": kmeans,
    "numeric_features": NUMERIC_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "n_clusters": N_CLUSTERS
}

joblib.dump(artifact, MODEL_PATH)

print(f"Segmentation model saved to: {MODEL_PATH}")
print(f"Customer segments saved to: {OUTPUT_PATH}")
