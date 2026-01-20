from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import io
import os
from dotenv import load_dotenv

# Import custom modules
from models.model_interface import model_interface
try:
    from explainability.shap_explainer import shap_explainer
except ImportError:
    # Fallback import
    import sys
    sys.path.append('explainability')
    from shap_explainer import shap_explainer
from supabase_client import supabase_storage

# Load environment variables
load_dotenv()

app = FastAPI(title="Invisor.ai Backend", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store current data and upload info
current_data = None
current_upload_id = None
DATA_FILE = "current_data.csv"

def _ensure_data_loaded():
    """Ensure data is loaded from file if global variable is None"""
    global current_data
    if current_data is None and os.path.exists(DATA_FILE):
        try:
            print("🔄 Loading data from persistence file...")
            current_data = pd.read_csv(DATA_FILE)
            print(f"✅ Loaded {len(current_data)} rows from {DATA_FILE}")
            return True
        except Exception as e:
            print(f"❌ Failed to load persistence file: {e}")
            return False
    return current_data is not None

@app.get("/")
async def root():
    return {"message": "Invisor.ai Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "models_loaded": model_interface.churn_model is not None,
        "supabase_connected": supabase_storage.is_connected()
    }

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and validate CSV file"""
    global current_data, current_upload_id
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV content
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        # Basic validation
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Store data globally for processing
        current_data = df
        
        # Persist to local file
        try:
            df.to_csv(DATA_FILE, index=False)
            print(f"✅ Saved data to {DATA_FILE}")
        except Exception as e:
            print(f"⚠️ Failed to persist data: {e}")
        
        # Store in Supabase if connected
        if supabase_storage.is_connected():
            upload_result = supabase_storage.upload_csv_data(file.filename, df)
            if upload_result.get("success"):
                current_upload_id = upload_result.get("upload_id")
        
        # Return basic info about the dataset
        return {
            "message": "CSV uploaded successfully",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "sample_data": df.head().to_dict('records'),
            "upload_id": current_upload_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

@app.post("/predict-churn")
async def predict_churn():
    """Generate churn predictions for uploaded data"""
    global current_data, current_upload_id
    
    if current_data is None:
        raise HTTPException(status_code=400, detail="No data uploaded. Please upload a CSV first.")
    
    try:
        # Use model interface for predictions
        predictions = model_interface.predict_churn(current_data)
        
        # Store predictions in Supabase if connected
        if supabase_storage.is_connected() and current_upload_id:
            supabase_storage.store_predictions(current_upload_id, predictions)
        
        # Calculate summary statistics
        high_risk_count = sum(1 for p in predictions if p["risk_level"] == "High")
        medium_risk_count = sum(1 for p in predictions if p["risk_level"] == "Medium")
        low_risk_count = sum(1 for p in predictions if p["risk_level"] == "Low")
        
        return {
            "message": "Churn predictions generated",
            "total_customers": len(predictions),
            "high_risk_count": high_risk_count,
            "medium_risk_count": medium_risk_count,
            "low_risk_count": low_risk_count,
            "predictions": predictions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating predictions: {str(e)}")
@app.post("/customer-segmentation")
async def customer_segmentation():
    """Generate customer segments for uploaded data"""
    global current_data, current_upload_id
    
    if current_data is None:
        raise HTTPException(status_code=400, detail="No data uploaded. Please upload a CSV first.")
    
    try:
        # Use model interface for segmentation
        segments = model_interface.predict_segments(current_data)
        
        # Store segments in Supabase if connected
        if supabase_storage.is_connected() and current_upload_id:
            supabase_storage.store_segments(current_upload_id, segments)
        
        # Generate segment summaries
        segment_summary = {}
        for segment in segments:
            segment_name = segment["segment_name"]
            if segment_name not in segment_summary:
                segment_summary[segment_name] = {"count": 0, "percentage": 0}
            segment_summary[segment_name]["count"] += 1
        
        # Calculate percentages
        total_customers = len(segments)
        for segment_name in segment_summary:
            count = segment_summary[segment_name]["count"]
            segment_summary[segment_name]["percentage"] = round((count / total_customers) * 100, 1)
        
        return {
            "message": "Customer segmentation completed",
            "total_customers": total_customers,
            "segments": segments,
            "segment_summary": segment_summary
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating segments: {str(e)}")

@app.post("/explainability")
async def get_explainability():
    """Generate explainability results for churn predictions"""
    global current_data
    
    _ensure_data_loaded()
    
    if current_data is None:
        raise HTTPException(status_code=400, detail="No data uploaded. Please upload a CSV first.")
    
    try:
        # Use SHAP explainer with real model if available
        model = model_interface.churn_model if model_interface.churn_model else None
        explanations = shap_explainer.explain_predictions(current_data, model=model)
        
        return {
            "message": "Explainability results generated",
            **explanations
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explainability: {str(e)}")
@app.get("/chatbot/insights")
async def get_chatbot_insights():
    """Get predefined insights for the chatbot"""
    global current_data
    
    _ensure_data_loaded()
    
    if current_data is None:
        return {"insights": ["Please upload a CSV file first to generate insights."]}
    
    try:
        insights = [
            f"Dataset contains {len(current_data)} customers with {len(current_data.columns)} features.",
            "High-risk customers show patterns in usage frequency and support tickets.",
            "Customer segments reveal distinct behavioral patterns for targeted marketing.",
            "Feature importance analysis shows top factors influencing churn decisions.",
            "Explainable AI provides transparency in model predictions for business users."
        ]
        
        return {"insights": insights}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

@app.post("/chatbot/query")
async def chatbot_query(query: Dict[str, str]):
    """Handle basic chatbot queries about the data and models"""
    user_query = query.get("query", "").lower()
    
    _ensure_data_loaded()
    
    if current_data is None:
        return {"response": "Please upload a CSV file first to analyze your customer data."}
    
    try:
        # Generate predictions once for efficiency
        predictions = model_interface.predict_churn(current_data)
        segments = model_interface.predict_segments(current_data)
        
        # Count risk levels
        high_risk = sum(1 for p in predictions if p['risk_level'] == 'High')
        medium_risk = sum(1 for p in predictions if p['risk_level'] == 'Medium')
        low_risk = sum(1 for p in predictions if p['risk_level'] == 'Low')
        
        # Count segments
        seg_counts = pd.Series([s['segment_name'] for s in segments]).value_counts().to_dict()
        
        # Enhanced query handling
        if "high risk" in user_query or ("how many" in user_query and "risk" in user_query):
            return {"response": f"I found {high_risk} customers at High Risk of churn ({high_risk/len(predictions)*100:.1f}% of your customer base). Additionally, {medium_risk} are at Medium Risk and {low_risk} are at Low Risk."}
        
        elif "segment" in user_query and ("highest" in user_query or "most" in user_query) and "churn" in user_query:
            # Analyze churn risk by segment
            segment_risk = {}
            for pred, seg in zip(predictions, segments):
                seg_name = seg['segment_name']
                if seg_name not in segment_risk:
                    segment_risk[seg_name] = {'total': 0, 'high_risk': 0}
                segment_risk[seg_name]['total'] += 1
                if pred['risk_level'] == 'High':
                    segment_risk[seg_name]['high_risk'] += 1
            
            # Calculate risk percentages
            for seg_name in segment_risk:
                segment_risk[seg_name]['risk_pct'] = (segment_risk[seg_name]['high_risk'] / segment_risk[seg_name]['total']) * 100
            
            # Find highest risk segment
            highest_risk_segment = max(segment_risk.keys(), key=lambda x: segment_risk[x]['risk_pct'])
            risk_pct = segment_risk[highest_risk_segment]['risk_pct']
            
            return {"response": f"The '{highest_risk_segment}' segment has the highest churn risk at {risk_pct:.1f}% ({segment_risk[highest_risk_segment]['high_risk']} out of {segment_risk[highest_risk_segment]['total']} customers). Consider targeted retention strategies for this segment."}
        
        elif "segment" in user_query:
            top_segment = max(seg_counts, key=seg_counts.get)
            segment_list = ", ".join([f"{name}: {count}" for name, count in seg_counts.items()])
            return {"response": f"Customer segments: {segment_list}. The largest segment is '{top_segment}' with {seg_counts[top_segment]} customers."}
        
        elif "feature" in user_query or "important" in user_query or "influence" in user_query:
            try:
                # Try to get feature importance from precomputed data
                explainability_dir = Path("ml_models/explainability")
                global_importance_file = explainability_dir / "global_feature_importance.csv"
                
                if global_importance_file.exists():
                    importance_df = pd.read_csv(global_importance_file)
                    top_features = importance_df.head(3)
                    feature_text = ", ".join([f"{row['feature']} ({row['importance']:.1%})" for _, row in top_features.iterrows()])
                    return {"response": f"The most important features influencing churn are: {feature_text}. These factors have the strongest impact on customer retention decisions."}
                else:
                    return {"response": "Feature importance analysis is not available. The key factors typically include contract type, tenure, monthly charges, and customer service interactions."}
            except Exception as e:
                return {"response": "I couldn't analyze feature importance at the moment. Generally, contract type, tenure, and monthly charges are key churn indicators."}
        
        elif "summary" in user_query or "insight" in user_query:
            avg_churn_prob = sum(p['churn_probability'] for p in predictions) / len(predictions)
            return {"response": f"Customer Analysis Summary: {len(current_data)} customers analyzed. Risk Distribution: {high_risk} High Risk ({high_risk/len(predictions)*100:.1f}%), {medium_risk} Medium Risk, {low_risk} Low Risk. Average churn probability: {avg_churn_prob:.1%}. Top segment: {max(seg_counts, key=seg_counts.get)} ({seg_counts[max(seg_counts, key=seg_counts.get)]} customers)."}
        
        elif "data" in user_query and "count" in user_query:
            return {"response": f"I have analyzed {len(current_data)} customers with {len(current_data.columns)} features. The churn model is active and generating real-time predictions."}
        
        else:
            # Default response with helpful suggestions
            return {"response": f"I can help analyze your {len(current_data)} customers. Try asking: 'How many customers are at high risk?', 'Which segment has highest churn risk?', 'What features influence churn most?', or 'Summarize the customer insights'."}
    
    except Exception as e:
        return {"response": f"I encountered an error analyzing your data: {str(e)}. Please try uploading your data again or ask a different question."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
@app.get("/upload-history")
async def get_upload_history():
    """Get history of previous uploads"""
    if supabase_storage.is_connected():
        result = supabase_storage.get_upload_history()
        return result
    else:
        return {"message": "Upload history not available - Supabase not configured"}

@app.post("/load-models")
async def load_models(model_paths: Dict[str, str]):
    """Load ML models from specified paths"""
    results = {}
    
    if "churn_model" in model_paths:
        success = model_interface.load_churn_model(model_paths["churn_model"])
        results["churn_model"] = "loaded" if success else "failed"
    
    if "segmentation_model" in model_paths:
        success = model_interface.load_segmentation_model(model_paths["segmentation_model"])
        results["segmentation_model"] = "loaded" if success else "failed"
    
    if "scaler" in model_paths:
        success = model_interface.load_scaler(model_paths["scaler"])
        results["scaler"] = "loaded" if success else "failed"
    
    return {"message": "Model loading completed", "results": results}

@app.get("/model-status")
async def get_model_status():
    """Get current status of loaded models"""
    model_info = model_interface.get_model_info()
    return {
        **model_info,
        "supabase_connected": supabase_storage.is_connected()
    }