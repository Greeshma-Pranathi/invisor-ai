from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd

from storage import CACHE
from model_loader import load_churn_model, load_segmentation_model

from ml.predict import predict_churn
from ml.predict_segment import predict_segments

import joblib
import pandas as pd

from ml.explainability import explain_customer

from pydantic import BaseModel
from ml.chatbot.chatbot_logic import chatbot_response

from fastapi.middleware.cors import CORSMiddleware

from fastapi import HTTPException
import shap
import numpy as np
import pandas as pd

# -------------------------
# Load models once at startup
# -------------------------
CHURN_MODEL = load_churn_model()
SEGMENT_MODEL = load_segmentation_model()

def compute_global_explainability(df, model_pipeline):
    import shap
    import numpy as np
    import pandas as pd

    X = df.drop(columns=["customer_id", "churn"], errors="ignore")

    preprocessing = model_pipeline.named_steps["preprocessing"]
    classifier = model_pipeline.named_steps["classifier"]

    X_processed = preprocessing.transform(X)
    column_transformer = preprocessing.named_steps["preprocessor"]
    feature_names = column_transformer.get_feature_names_out()

    explainer = shap.TreeExplainer(classifier)
    shap_values = explainer.shap_values(X_processed)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, 1]

    mean_abs_shap = np.abs(shap_values).mean(axis=0)

    return (
        pd.DataFrame({
            "feature": feature_names,
            "mean_abs_shap": mean_abs_shap
        })
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
    )

# -------------------------
# App
# -------------------------
app = FastAPI(
    title="Invisor.ai Backend",
    description="Minimal backend for ML APIs",
    version="1.0"
)

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "data_loaded": CACHE["dataframe"] is not None
    }

# -------------------------
# Upload CSV
# -------------------------
@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read CSV file")

    if df.empty:
        raise HTTPException(status_code=400, detail="CSV file is empty")

    CACHE["dataframe"] = df
    CACHE["filename"] = file.filename

    return {
        "status": "success",
        "message": "CSV uploaded successfully",
        "data": {
            "filename": file.filename,
            "row_count": df.shape[0],
            "column_count": df.shape[1]
        }
    }

# -------------------------
# Predict churn
# -------------------------
@app.post("/predict-churn")
def predict_churn_api():
    if CACHE["dataframe"] is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded")

    try:
        predictions_df = predict_churn(
            df=CACHE["dataframe"],
            model_pipeline=CHURN_MODEL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "message": "Churn prediction completed",
        "data": predictions_df.to_dict(orient="records")
    }

# -------------------------
# Predict segments
# -------------------------
@app.post("/predict-segments")
def predict_segments_api():
    if CACHE["dataframe"] is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded")

    try:
        segments_df = predict_segments(
            df=CACHE["dataframe"],
            model_artifact=SEGMENT_MODEL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "message": "Segmentation completed",
        "data": segments_df.to_dict(orient="records")
    }

@app.get("/explain/global")
def global_explain_api():
    # 1. Ensure CSV is uploaded
    if CACHE["dataframe"] is None:
        raise HTTPException(
            status_code=400,
            detail="Upload CSV before requesting explainability"
        )

    df = CACHE["dataframe"]

    # 2. Prepare features
    X = df.drop(columns=["customer_id", "churn"], errors="ignore")

    # 3. Extract pipeline components
    preprocessing = CHURN_MODEL.named_steps["preprocessing"]
    classifier = CHURN_MODEL.named_steps["classifier"]

    # 4. Transform data
    X_processed = preprocessing.transform(X)

    column_transformer = preprocessing.named_steps["preprocessor"]
    feature_names = column_transformer.get_feature_names_out()

    # 5. SHAP
    explainer = shap.TreeExplainer(classifier)
    shap_values = explainer.shap_values(X_processed)

    # Binary classifier safety
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, 1]

    # 6. Aggregate global importance
    mean_abs_shap = np.abs(shap_values).mean(axis=0)

    global_df = (
        pd.DataFrame({
            "feature": feature_names,
            "mean_abs_shap": mean_abs_shap
        })
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
    )

    return {
        "status": "success",
        "message": "Global churn drivers retrieved",
        "data": global_df.to_dict(orient="records")
    }

@app.get("/explain/customer/{customer_id}")
def customer_explain_api(customer_id: str):
    if CACHE["dataframe"] is None:
        raise HTTPException(
            status_code=400,
            detail="No CSV uploaded"
        )

    try:
        explanation = explain_customer(
            customer_id=customer_id,
            df=CACHE["dataframe"],
            model_pipeline=CHURN_MODEL
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "status": "success",
        "message": f"Explainability generated for customer {customer_id}",
        "data": explanation
    }

class ChatRequest(BaseModel):
    query: str
    customer_selected: bool = False
    selected_customer_id: str | None = None

GLOBAL_EXPLAIN_PATH = "ml_models/explainability/global_feature_importance.csv"

try:
    GLOBAL_EXPLAIN_DF = pd.read_csv(GLOBAL_EXPLAIN_PATH)
except FileNotFoundError:
    GLOBAL_EXPLAIN_DF = None

@app.post("/chat")
def chat_api(request: ChatRequest):
    if CACHE["dataframe"] is None:
        raise HTTPException(
            status_code=400,
            detail="No CSV uploaded"
        )

    # -------------------------
    # Build cached outputs
    # -------------------------
    try:
        churn_df = predict_churn(
            df=CACHE["dataframe"],
            model_pipeline=CHURN_MODEL
        )

        segments_df = predict_segments(
            df=CACHE["dataframe"],
            model_artifact=SEGMENT_MODEL
        )

        # Segment counts
        segment_counts = (
            segments_df["segment_label"]
            .value_counts()
            .to_dict()
        )

        # Segment churn rates
        merged = churn_df.merge(
            segments_df,
            on="customer_id"
        )

        segment_churn = (
            merged.groupby("segment_label")["churn_label"]
            .mean()
            .round(2)
            .to_dict()
        )
        global_explain_df = compute_global_explainability(
        df=CACHE["dataframe"],
        model_pipeline=CHURN_MODEL
        )
        cached_outputs = {
            "churn": churn_df,
            "global_explain": global_explain_df,  # ✅ FIXED
            "local_explain": None,
            "segment_counts": segment_counts,
            "segment_churn": segment_churn,
            "segment_descriptions": {},
            "dataset_summary": f"{len(churn_df)} customers analyzed"
        }

        # Local explainability (only if requested)
        if request.customer_selected and request.selected_customer_id:
            cached_outputs["local_explain"] = explain_customer(
                customer_id=request.selected_customer_id,
                df=CACHE["dataframe"],
                model_pipeline=CHURN_MODEL
            )

        response_text = chatbot_response(
            query=request.query,
            cached_outputs=cached_outputs,
            customer_selected=request.customer_selected,
            selected_customer_id=request.selected_customer_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "status": "success",
        "response": response_text
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
