from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = [
    "senior_citizen",
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "avg_monthly_usage_gb",
    "support_tickets_last_6m",
    "late_payments_last_year"
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

def build_preprocessing_pipeline():
    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES)
        ]
    )
