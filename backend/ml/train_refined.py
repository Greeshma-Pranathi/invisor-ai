import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

from ml.preprocessing_refined import build_preprocessing_pipeline

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
# Load dataset
# -------------------------
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["churn", "customer_id"])
y = df["churn"]

# -------------------------
# Train / validation split
# -------------------------
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------
# Build full pipeline
# -------------------------
model = Pipeline(steps=[
    ("preprocessing", build_preprocessing_pipeline()),
    ("classifier", RandomForestClassifier(
        n_estimators=400,
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])

# -------------------------
# Train model
# -------------------------
model.fit(X_train, y_train)

# -------------------------
# Evaluation (sanity check)
# -------------------------
y_pred = model.predict(X_val)
y_prob = model.predict_proba(X_val)[:, 1]

print("Refined Random Forest Evaluation")
print("--------------------------------")
print(classification_report(y_val, y_pred))
print("ROC-AUC:", roc_auc_score(y_val, y_prob))

# -------------------------
# Save final model artifact
# -------------------------
joblib.dump(model, MODEL_PATH)

print(f"Final churn model saved to: {MODEL_PATH}")
