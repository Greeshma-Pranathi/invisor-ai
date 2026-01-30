import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    classification_report
)

# -------------------------
# Paths (robust)
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "ml_data", "sample_customer_churn.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "ml_models", "baseline_churn_model.pkl")

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["churn", "customer_id"])
y = df["churn"]

# Same split strategy as training
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------
# Load trained model
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
accuracy = accuracy_score(y_val, y_pred)
precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)
roc_auc = roc_auc_score(y_val, y_prob)

print("Baseline Model Evaluation Metrics")
print("---------------------------------")
print(f"Accuracy : {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"ROC-AUC  : {roc_auc:.3f}")

print("\nClassification Report")
print(classification_report(y_val, y_pred))
