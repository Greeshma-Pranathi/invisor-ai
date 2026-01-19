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

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sample_customer_churn_v2.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "final_churn_model.pkl")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "models", "explainability")

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
# Load model artifact
# -------------------------
artifact = joblib.load(MODEL_PATH)
full_pipeline = artifact["preprocessor"]
model = artifact["model"]

# -------------------------
# Apply preprocessing step-by-step
# -------------------------
feature_engineering = full_pipeline.named_steps["feature_engineering"]
column_transformer = full_pipeline.named_steps["preprocessor"]

X_fe = feature_engineering.transform(X)
X_processed = column_transformer.transform(X_fe)

feature_names = column_transformer.get_feature_names_out()

# -------------------------
# SHAP explainer
# -------------------------
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_processed)

# Handle binary / multi-dim SHAP safely
if isinstance(shap_values, list):
    shap_values = shap_values[1]

if shap_values.ndim == 3:
    shap_values = shap_values[:, :, 1]

# -------------------------
# Local explanation plot
# -------------------------
plt.figure(figsize=(10, 6))

shap.waterfall_plot(
    shap.Explanation(
        values=shap_values[0],
        base_values=explainer.expected_value[1]
        if isinstance(explainer.expected_value, (list, np.ndarray))
        else explainer.expected_value,
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
