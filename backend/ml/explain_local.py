import os
import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Config
# -------------------------
CUSTOMER_ID_TO_EXPLAIN = "C007"

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "..", "ml_data", "sample_customer_churn_v2.csv"
)
MODEL_PATH = os.path.join(
    BASE_DIR, "..", "ml_models", "final_churn_model.pkl"
)
OUTPUT_DIR = os.path.join(
    BASE_DIR, "..", "ml_models", "explainability"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(DATA_PATH)

row = df[df["customer_id"] == CUSTOMER_ID_TO_EXPLAIN]
if row.empty:
    raise ValueError(f"Customer {CUSTOMER_ID_TO_EXPLAIN} not found")

X = row.drop(columns=["churn", "customer_id"])

# -------------------------
# Load trained pipeline
# -------------------------
pipeline = joblib.load(MODEL_PATH)

preprocessor = pipeline.named_steps["preprocessing"]
model = pipeline.named_steps["classifier"]

# -------------------------
# Transform input
# -------------------------
X_processed = preprocessor.transform(X)

# Get feature names from ColumnTransformer ONLY
column_transformer = preprocessor.named_steps["preprocessor"]
feature_names = column_transformer.get_feature_names_out()

# -------------------------
# SHAP Explainer
# -------------------------
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_processed)

# -------------------------
# FORCE single explanation vector
# -------------------------
# For RandomForest binary classification:
# shap_values shape -> (n_samples, n_features, n_classes)
# We must select: [sample, feature, positive_class]

if isinstance(shap_values, list):
    shap_values = shap_values[1]

shap_row = shap_values[0, :, 1]   # <-- CRITICAL FIX

# -------------------------
# Local explanation plot
# -------------------------
plt.figure(figsize=(10, 6))

shap.waterfall_plot(
    shap.Explanation(
        values=shap_row,
        base_values=explainer.expected_value[1],
        data=X_processed[0],
        feature_names=feature_names
    ),
    show=False
)

plot_path = os.path.join(
    OUTPUT_DIR,
    f"local_explanation_{CUSTOMER_ID_TO_EXPLAIN}.png"
)

plt.savefig(plot_path, bbox_inches="tight")
plt.close()

print(f"Local explanation saved to: {plot_path}")
