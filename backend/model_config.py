"""
Model Configuration for Invisor.ai
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
ML_MODELS_DIR = BASE_DIR / "ml_models"
ML_SRC_DIR = BASE_DIR / "ml_src"

# Model file paths
MODEL_PATHS = {
    "churn_model": ML_MODELS_DIR / "final_churn_model.pkl",
    "baseline_churn_model": ML_MODELS_DIR / "baseline_churn_model.pkl", 
    "refined_churn_model": ML_MODELS_DIR / "refined_churn_model.pkl",
    "segmentation_model": ML_MODELS_DIR / "segmentation_model.pkl"
}

# Model metadata
MODEL_METADATA = {
    "churn_model": {
        "name": "Final Churn Prediction Model",
        "type": "classification",
        "features": ["age", "monthly_charges", "total_charges", "tenure", "contract_type"],
        "target": "churn",
        "performance": {"accuracy": 0.85, "precision": 0.82, "recall": 0.78}
    },
    "segmentation_model": {
        "name": "Customer Segmentation Model", 
        "type": "clustering",
        "features": ["monthly_charges", "total_charges", "tenure"],
        "n_clusters": 5,
        "segments": ["High Value", "At Risk", "New Customer", "Loyal", "Price Sensitive"]
    }
}

# Feature configurations
FEATURE_COLUMNS = [
    "customer_id", "age", "monthly_charges", "total_charges", 
    "tenure", "contract_type", "payment_method", "internet_service"
]

NUMERIC_FEATURES = ["age", "monthly_charges", "total_charges", "tenure"]
CATEGORICAL_FEATURES = ["contract_type", "payment_method", "internet_service"]

# Preprocessing settings
PREPROCESSING_CONFIG = {
    "handle_missing": True,
    "scale_features": True,
    "encode_categorical": True,
    "feature_selection": False
}
