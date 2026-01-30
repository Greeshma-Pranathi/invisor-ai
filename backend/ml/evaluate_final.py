import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

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

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["churn", "customer_id"])
y = df["churn"]

# -------------------------
# Hold-out split
# -------------------------
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------
# Load trained pipeline
# -------------------------
model = joblib.load(MODEL_PATH)

# -------------------------
# Predictions
# -------------------------
y_pred = model.predict(X_val)
y_prob = model.predict_proba(X_val)[:, 1]

# -------------------------
# Metrics
# -------------------------
roc_auc = roc_auc_score(y_val, y_prob)
precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)

print("Refined Model Evaluation Metrics")
print("--------------------------------")
print(f"ROC-AUC  : {roc_auc:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"F1-score : {f1:.3f}")

print("\nClassification Report")
print(classification_report(y_val, y_pred))
