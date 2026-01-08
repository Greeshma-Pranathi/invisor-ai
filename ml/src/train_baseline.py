import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from preprocessing import build_preprocessing_pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sample_customer_churn.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "baseline_churn_model.pkl")

df = pd.read_csv(DATA_PATH)


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
# Build preprocessing pipeline
# -------------------------
preprocessor = build_preprocessing_pipeline()

# -------------------------
# Build full model pipeline
# -------------------------
model = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ))
])

# -------------------------
# Train model
# -------------------------
model.fit(X_train, y_train)

# -------------------------
# Save trained model
# -------------------------
joblib.dump(model, MODEL_PATH)

print(f"Baseline churn model saved to: {MODEL_PATH}")
