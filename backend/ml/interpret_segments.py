import os
import pandas as pd
import joblib

from ml.segmentation_config import NUMERIC_FEATURES, CATEGORICAL_FEATURES

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "..", "ml_data", "sample_customer_churn_v2.csv"
)
MODEL_PATH = os.path.join(
    BASE_DIR, "..", "ml_models", "segmentation_model.pkl"
)

# -------------------------
# Load data and model
# -------------------------
df = pd.read_csv(DATA_PATH)
artifact = joblib.load(MODEL_PATH)

pipeline = artifact["pipeline"]

# -------------------------
# Predict segments
# -------------------------
df["segment_label"] = pipeline.predict(df)

# -------------------------
# Numerical feature summary
# -------------------------
numeric_summary = (
    df.groupby("segment_label")[NUMERIC_FEATURES]
      .mean()
      .round(2)
)

print("\n=== Numeric Feature Averages by Segment ===")
print(numeric_summary)

# -------------------------
# Categorical feature summary
# -------------------------
print("\n=== Dominant Categorical Traits by Segment ===")

for seg in sorted(df["segment_label"].unique()):
    print(f"\nSegment {seg}")
    seg_df = df[df["segment_label"] == seg]

    for col in CATEGORICAL_FEATURES:
        top_val = seg_df[col].value_counts(normalize=True).idxmax()
        pct = seg_df[col].value_counts(normalize=True).max()
        print(f"  {col}: {top_val} ({pct:.0%})")
