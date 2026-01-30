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

# -------------------------
# Load models once at startup
# -------------------------
CHURN_MODEL = load_churn_model()
SEGMENT_MODEL = load_segmentation_model()

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

# Load global explainability output (precomputed)
GLOBAL_EXPLAIN_PATH = "ml_models/explainability/global_feature_importance.csv"

try:
    GLOBAL_EXPLAIN_DF = pd.read_csv(GLOBAL_EXPLAIN_PATH)
except FileNotFoundError:
    GLOBAL_EXPLAIN_DF = None

@app.get("/explain/global")
def global_explain_api():
    if GLOBAL_EXPLAIN_DF is None:
        raise HTTPException(
            status_code=500,
            detail="Global explainability not available"
        )

    return {
        "status": "success",
        "message": "Global churn drivers retrieved",
        "data": GLOBAL_EXPLAIN_DF.to_dict(orient="records")
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

        cached_outputs = {
            "churn": churn_df,
            "global_explain": GLOBAL_EXPLAIN_DF,
            "local_explain": None,  # computed only when needed
            "segment_counts": segment_counts,
            "segment_churn": segment_churn,
            "segment_descriptions": {},  # optional later
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
