import pickle
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import os
import joblib
import sys
from pathlib import Path

# Add ml_src to path for importing preprocessing modules
sys.path.append(str(Path(__file__).parent.parent / "ml_src"))

try:
    from model_config import MODEL_PATHS, MODEL_METADATA, FEATURE_COLUMNS, NUMERIC_FEATURES, CATEGORICAL_FEATURES
    CONFIG_AVAILABLE = True
except ImportError:
    print("Warning: Could not import model_config")
    CONFIG_AVAILABLE = False
    MODEL_PATHS = {}
    MODEL_METADATA = {}

# Try to import preprocessing functions with correct names
try:
    from preprocessing_refined import build_preprocessing_pipeline as build_churn_pipeline
    from preprocessing_segmentation import build_segmentation_preprocessor
    PREPROCESSING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import preprocessing functions: {e}")
    PREPROCESSING_AVAILABLE = False

# Segment names mapping
SEGMENT_NAMES = {
    0: "High Value",
    1: "At Risk", 
    2: "New Customer",
    3: "Loyal",
    4: "Price Sensitive"
}

class ModelInterface:
    """Interface for loading and using ML models"""
    
    def __init__(self):
        self.churn_model = None
        self.segmentation_model = None
        self.feature_scaler = None
        self.churn_preprocessor = None
        self.segmentation_preprocessor = None
        self.model_metadata = MODEL_METADATA
        self.is_initialized = False
        
        # Auto-load models if they exist
        self._auto_load_models()
    
    def _auto_load_models(self):
        """Automatically load models if they exist"""
        try:
            if not CONFIG_AVAILABLE:
                print("⚠️ Config not available, skipping auto-load")
                return

            print("🔄 Auto-loading models from config...")

            # Load final churn model
            churn_model_path = MODEL_PATHS.get("churn_model")
            if churn_model_path and churn_model_path.exists():
                self.load_churn_model(str(churn_model_path))
            else:
                print(f"⚠️ Churn model not found at {churn_model_path}")
            
            # Load segmentation model
            seg_model_path = MODEL_PATHS.get("segmentation_model")
            if seg_model_path and seg_model_path.exists():
                self.load_segmentation_model(str(seg_model_path))
            else:
                print(f"⚠️ Segmentation model not found at {seg_model_path}")
            
            self.is_initialized = True
            
        except Exception as e:
            print(f"⚠️ Auto-load failed: {e}")
            self.is_initialized = False
    
    def load_churn_model(self, model_path: str) -> bool:
        """Load the churn prediction model"""
        try:
            if model_path.endswith('.pkl'):
                with open(model_path, 'rb') as f:
                    self.churn_model = pickle.load(f)
            elif model_path.endswith('.joblib'):
                self.churn_model = joblib.load(model_path)
            
            print(f"✅ Churn model loaded from {model_path}")
            
            # Try to build preprocessor
            if PREPROCESSING_AVAILABLE:
                try:
                    self.churn_preprocessor = build_churn_pipeline()
                    print("✅ Churn preprocessor initialized")
                except Exception as e:
                    print(f"⚠️ Could not build churn preprocessor: {e}")
            
            return True
        except Exception as e:
            print(f"❌ Error loading churn model: {e}")
            return False
    
    def load_segmentation_model(self, model_path: str) -> bool:
        """Load the customer segmentation model"""
        try:
            if model_path.endswith('.pkl'):
                with open(model_path, 'rb') as f:
                    self.segmentation_model = pickle.load(f)
            elif model_path.endswith('.joblib'):
                self.segmentation_model = joblib.load(model_path)
            
            print(f"✅ Segmentation model loaded from {model_path}")
            
            # Try to build preprocessor
            if PREPROCESSING_AVAILABLE:
                try:
                    # Import segmentation config
                    from segmentation_config import NUMERIC_FEATURES as seg_numeric, CATEGORICAL_FEATURES as seg_categorical
                    self.segmentation_preprocessor = build_segmentation_preprocessor(seg_numeric, seg_categorical)
                    print("✅ Segmentation preprocessor initialized")
                except Exception as e:
                    print(f"⚠️ Could not build segmentation preprocessor: {e}")
            
            return True
        except Exception as e:
            print(f"❌ Error loading segmentation model: {e}")
            return False
    
    def load_scaler(self, scaler_path: str) -> bool:
        """Load feature scaler"""
        try:
            if scaler_path.endswith('.pkl'):
                with open(scaler_path, 'rb') as f:
                    self.feature_scaler = pickle.load(f)
            elif scaler_path.endswith('.joblib'):
                self.feature_scaler = joblib.load(scaler_path)
            
            print(f"✅ Feature scaler loaded from {scaler_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading scaler: {e}")
            return False
    
    def preprocess_data_for_churn(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess data for churn prediction using ML pipeline"""
        try:
            if self.churn_preprocessor is not None:
                # Use the actual preprocessing pipeline
                processed_data = self.churn_preprocessor.fit_transform(data)
                return pd.DataFrame(processed_data)
            else:
                 # Fallback if preprocessor failed to build but model loaded? 
                 # This might happen if model expects processed data but pipeline file is missing.
                 # For now, let's try basic if pipeline is missing, but it might fail.
                print("⚠️ Churn preprocessor not available, using basic preprocessing")
                return self._basic_preprocessing(data)
        except Exception as e:
            print(f"⚠️ Churn preprocessing error: {e}")
            # Try basic as fallback
            return self._basic_preprocessing(data)
    
    def preprocess_data_for_segmentation(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess data for segmentation using ML pipeline"""
        try:
            if self.segmentation_preprocessor is not None:
                # Use the actual preprocessing pipeline
                processed_data = self.segmentation_preprocessor.fit_transform(data)
                return pd.DataFrame(processed_data)
            else:
                print("⚠️ Segmentation preprocessor not available, using basic preprocessing")
                return self._basic_preprocessing(data)
        except Exception as e:
            print(f"⚠️ Segmentation preprocessing error: {e}")
            return self._basic_preprocessing(data)
    
    def _basic_preprocessing(self, data: pd.DataFrame) -> pd.DataFrame:
        """Basic preprocessing fallback"""
        processed_data = data.copy()
        
        # simple numeric handling
        numeric_cols = processed_data.select_dtypes(include=[np.number]).columns
        processed_data[numeric_cols] = processed_data[numeric_cols].fillna(processed_data[numeric_cols].mean())
        
        # simple categorical handling
        categorical_cols = processed_data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            processed_data[col] = processed_data[col].fillna('Unknown')
            unique_vals = processed_data[col].unique()
            mapping = {val: idx for idx, val in enumerate(unique_vals)}
            processed_data[col] = processed_data[col].map(mapping)
            
        return processed_data
    
    def predict_churn(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate churn predictions using real ML model"""
        if self.churn_model is None:
            raise ValueError("Churn model is not loaded. Cannot generate predictions.")
        
        try:
            # Preprocess data using ML pipeline
            processed_data = self.preprocess_data_for_churn(data)
            
            # Get predictions and probabilities
            # Some models expect dataframe, others numpy array. Pipeline outputs array.
            predictions = self.churn_model.predict(processed_data)
            
            # Handle both binary and probability predictions
            if hasattr(self.churn_model, 'predict_proba'):
                probabilities = self.churn_model.predict_proba(processed_data)
                # Check shape to handle binary vs multi-class (though churn is binary)
                if len(probabilities.shape) > 1 and probabilities.shape[1] > 1:
                    probabilities = probabilities[:, 1]  # Probability of churn (class 1)
                elif len(probabilities.shape) > 1:
                    probabilities = probabilities[:, 0]
            else:
                # If no predict_proba, use predictions as probabilities (0 or 1)
                probabilities = predictions
            
            results = []
            for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
                # Ensure probability is between 0 and 1
                prob = float(prob)
                if prob > 1:
                    prob = prob / 100  # Convert percentage to probability if needed
                
                # Dynamic risk level based on probability
                risk_level = "High" if prob > 0.7 else "Medium" if prob > 0.4 else "Low"
                
                # Get Customer ID if available, else use index
                if "customer_id" in data.columns:
                    customer_id = data.iloc[idx]["customer_id"]
                else:
                    customer_id = idx

                results.append({
                    "customer_id": customer_id,
                    "churn_prediction": int(pred),
                    "churn_probability": round(prob, 3),
                    "risk_level": risk_level
                })
            
            print(f"✅ Generated {len(results)} churn predictions using real model")
            return results
        
        except Exception as e:
            print(f"❌ Error in churn prediction: {e}")
            import traceback
            traceback.print_exc()
            raise e
    
    def predict_segments(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate customer segments using real ML model"""
        if self.segmentation_model is None:
            raise ValueError("Segmentation model is not loaded. Cannot generate segments.")
        
        try:
            # Preprocess data using ML pipeline
            processed_data = self.preprocess_data_for_segmentation(data)
            
            # Get cluster assignments
            segments = self.segmentation_model.predict(processed_data)
            
            results = []
            for idx, segment_id in enumerate(segments):
                segment_id = int(segment_id)
                
                # Calculate confidence based on distance to cluster center (if available)
                confidence = 0.85  # Default confidence
                if hasattr(self.segmentation_model, 'transform'):
                    try:
                        # Some clusterers (like KMeans) support transform to get distances
                        distances = self.segmentation_model.transform(processed_data[idx:idx+1])
                        min_distance = np.min(distances)
                        confidence = max(0.6, 1.0 - (min_distance / 10))  # Normalize distance to confidence
                    except:
                        pass
                
                if "customer_id" in data.columns:
                    customer_id = data.iloc[idx]["customer_id"]
                else:
                    customer_id = idx

                results.append({
                    "customer_id": customer_id,
                    "segment_id": segment_id,
                    "segment_name": SEGMENT_NAMES.get(segment_id, f"Segment {segment_id}"),
                    "confidence": round(confidence, 3)
                })
            
            print(f"✅ Generated {len(results)} segments using real model")
            return results
        
        except Exception as e:
            print(f"❌ Error in segmentation: {e}")
            raise e
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            "churn_model_loaded": self.churn_model is not None,
            "segmentation_model_loaded": self.segmentation_model is not None,
            "scaler_loaded": self.feature_scaler is not None,
            "churn_preprocessor_loaded": self.churn_preprocessor is not None,
            "segmentation_preprocessor_loaded": self.segmentation_preprocessor is not None,
            "models_initialized": self.is_initialized,
            "model_metadata": self.model_metadata
        }
    


# Global model interface instance
model_interface = ModelInterface()
