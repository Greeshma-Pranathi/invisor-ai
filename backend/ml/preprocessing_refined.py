import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# -------------------------
# Feature Lists
# -------------------------
NUMERIC_FEATURES = [
    "senior_citizen",
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "avg_monthly_usage_gb",
    "support_tickets_last_6m",
    "late_payments_last_year",
    # engineered features
    "charges_per_month",
    "tickets_per_month",
    "usage_per_charge"
]

CATEGORICAL_FEATURES = [
    "gender",
    "partner",
    "dependents",
    "contract_type",
    "payment_method",
    "internet_service",
    "online_security",
    "tech_support",
    "paperless_billing",
    "streaming_tv",
    "streaming_movies",
    "multiple_lines",
    "autopay_enabled",
    "billing_cycle",
    "region"
]

# -------------------------
# Feature Engineering Step
# -------------------------
class InteractionFeatureGenerator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        required = [
        "total_charges",
        "tenure_months",
        "support_tickets_last_6m",
        "avg_monthly_usage_gb",
        "monthly_charges"
        ]

        for col in required:
            if col not in X.columns:
                X[col] = np.nan

        X["charges_per_month"] = X["total_charges"] / X["tenure_months"].replace(0, np.nan)
        X["tickets_per_month"] = X["support_tickets_last_6m"] / X["tenure_months"].replace(0, np.nan)
        X["usage_per_charge"] = X["avg_monthly_usage_gb"] / X["monthly_charges"].replace(0, np.nan)

        return X

# -------------------------
# Build Preprocessing Pipeline
# -------------------------
def build_preprocessing_pipeline():

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    column_transformer = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES)
        ]
    )

    return Pipeline(steps=[
        ("feature_engineering", InteractionFeatureGenerator()),
        ("preprocessor", column_transformer)
    ])
