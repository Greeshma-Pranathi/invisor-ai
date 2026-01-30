import os
import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "ml_data", "sample_customer_churn_v2.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "ml_models", "final_churn_model.pkl")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "ml_models", "explainability")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
X = df.drop(columns=["churn", "customer_id"])

# Load pipeline
pipeline = joblib.load(MODEL_PATH)
preprocessor = pipeline.named_steps["preprocessing"]
model = pipeline.named_steps["classifier"]

# Transform data
X_processed = preprocessor.transform(X)
column_transformer = preprocessor.named_steps["preprocessor"]
feature_names = column_transformer.get_feature_names_out()

# SHAP
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_processed)

# Binary classifier → take positive class
if isinstance(shap_values, list):
    shap_values = shap_values[1]

# Handle 3D safely
if shap_values.ndim == 3:
    shap_values = shap_values[:, :, 1]

# Aggregate
mean_abs_shap = np.abs(shap_values).mean(axis=0)

global_importance = pd.DataFrame({
    "feature": feature_names,
    "mean_abs_shap": mean_abs_shap
}).sort_values("mean_abs_shap", ascending=False)

csv_path = os.path.join(OUTPUT_DIR, "global_feature_importance.csv")
global_importance.to_csv(csv_path, index=False)

print("\nTop 10 Global Churn Drivers")
print(global_importance.head(10))

# Plot
plt.figure(figsize=(10, 6))
shap.summary_plot(
    shap_values,
    X_processed,
    feature_names=feature_names,
    show=False
)

plot_path = os.path.join(OUTPUT_DIR, "global_shap_summary.png")
plt.savefig(plot_path, bbox_inches="tight")
plt.close()

print(f"\nSaved global importance table to: {csv_path}")
print(f"Saved SHAP summary plot to: {plot_path}")
