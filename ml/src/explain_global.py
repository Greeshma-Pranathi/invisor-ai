import os
import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt

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
X = df.drop(columns=["churn", "customer_id"])

# -------------------------
# Load model artifact
# -------------------------
artifact = joblib.load(MODEL_PATH)

full_pipeline = artifact["preprocessor"]
model = artifact["model"]

# -------------------------
# STEP 1: Apply feature engineering ONLY
# -------------------------
feature_engineering = full_pipeline.named_steps["feature_engineering"]
column_transformer = full_pipeline.named_steps["preprocessor"]

X_fe = feature_engineering.transform(X)

# -------------------------
# STEP 2: Apply ColumnTransformer
# -------------------------
X_processed = column_transformer.transform(X_fe)

# -------------------------
# STEP 3: Get correct feature names
# -------------------------
feature_names = column_transformer.get_feature_names_out()

# -------------------------
# SHAP Explainer
# -------------------------
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_processed)

# Handle binary classification safely
if isinstance(shap_values, list):
    shap_values_churn = shap_values[1]
else:
    shap_values_churn = shap_values

# -------------------------
# Sanity checks
# -------------------------
assert X_processed.shape[1] == len(feature_names), (
    f"Feature count mismatch: X={X_processed.shape[1]}, names={len(feature_names)}"
)

assert X_processed.shape[1] == shap_values_churn.shape[1], (
    f"SHAP mismatch: X={X_processed.shape[1]}, SHAP={shap_values_churn.shape[1]}"
)

# -------------------------
# Global Feature Importance (SAFE SHAP HANDLING)
# -------------------------

# Ensure SHAP is 2D: (n_samples, n_features)
if shap_values_churn.ndim == 3:
    # shape: (n_samples, n_features, n_classes)
    shap_values_churn = shap_values_churn[:, :, 1]

elif shap_values_churn.ndim == 2:
    # shape already correct
    pass

else:
    raise ValueError(
        f"Unexpected SHAP shape: {shap_values_churn.shape}"
    )

# Now safely compute mean absolute SHAP per feature
mean_abs_shap = np.abs(shap_values_churn).mean(axis=0)

# Final sanity check
assert mean_abs_shap.ndim == 1
assert len(mean_abs_shap) == len(feature_names)

global_importance = pd.DataFrame({
    "feature": feature_names,
    "mean_abs_shap": mean_abs_shap
}).sort_values("mean_abs_shap", ascending=False)

# Save table
csv_path = os.path.join(OUTPUT_DIR, "global_feature_importance.csv")
global_importance.to_csv(csv_path, index=False)

print("\nTop 10 Global Churn Drivers")
print("---------------------------")
print(global_importance.head(10))

# -------------------------
# SHAP Summary Plot
# -------------------------
plt.figure(figsize=(10, 6))
shap.summary_plot(
    shap_values_churn,
    X_processed,
    feature_names=feature_names,
    show=False
)

plot_path = os.path.join(OUTPUT_DIR, "global_shap_summary.png")
plt.savefig(plot_path, bbox_inches="tight")
plt.close()

print(f"\nSaved global importance table to: {csv_path}")
print(f"Saved SHAP summary plot to: {plot_path}")
