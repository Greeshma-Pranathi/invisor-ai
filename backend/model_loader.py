import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Paths
CHURN_MODEL_PATH = BASE_DIR / "ml_models" / "final_churn_model.pkl"
SEGMENT_MODEL_PATH = BASE_DIR / "ml_models" / "segmentation_model.pkl"


def load_churn_model():
    if not CHURN_MODEL_PATH.exists():
        raise FileNotFoundError(f"Churn model not found: {CHURN_MODEL_PATH}")
    return joblib.load(CHURN_MODEL_PATH)


def load_segmentation_model():
    if not SEGMENT_MODEL_PATH.exists():
        raise FileNotFoundError(f"Segmentation model not found: {SEGMENT_MODEL_PATH}")
    return joblib.load(SEGMENT_MODEL_PATH)
