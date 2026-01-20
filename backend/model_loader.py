#!/usr/bin/env python3
"""
Custom model loader to handle pickle import issues
"""
import pickle
import joblib
import sys
from pathlib import Path

# Add ml_src to path
ml_src_path = str(Path(__file__).parent / "ml_src")
if ml_src_path not in sys.path:
    sys.path.insert(0, ml_src_path)

class CustomUnpickler(pickle.Unpickler):
    """Custom unpickler to handle missing module imports"""
    
    def find_class(self, module, name):
        # Handle sklearn imports that might be missing
        if name == 'Pipeline':
            from sklearn.pipeline import Pipeline
            return Pipeline
        elif name == 'ColumnTransformer':
            from sklearn.compose import ColumnTransformer
            return ColumnTransformer
        elif module == 'sklearn.pipeline' and name == 'Pipeline':
            from sklearn.pipeline import Pipeline
            return Pipeline
        elif module == 'sklearn.compose' and name == 'ColumnTransformer':
            from sklearn.compose import ColumnTransformer
            return ColumnTransformer
        
        # Handle preprocessing modules
        if module in ['preprocessing_refined', 'preprocessing_segmentation']:
            try:
                # Import the module
                __import__(module)
                mod = sys.modules[module]
                return getattr(mod, name)
            except (ImportError, AttributeError):
                pass
        
        # Default behavior
        return super().find_class(module, name)

def load_model_safe(model_path: str):
    """Safely load a pickled model with custom unpickler"""
    try:
        # First try joblib (recommended for sklearn models)
        if model_path.endswith('.pkl'):
            try:
                return joblib.load(model_path)
            except Exception as e:
                print(f"Joblib failed: {e}, trying custom pickle...")
        
        # Try custom unpickler
        with open(model_path, 'rb') as f:
            unpickler = CustomUnpickler(f)
            return unpickler.load()
            
    except Exception as e:
        print(f"Custom unpickler failed: {e}")
        raise e

if __name__ == "__main__":
    # Test the loader
    model_path = "ml_models/final_churn_model.pkl"
    try:
        model = load_model_safe(model_path)
        print(f"✅ Successfully loaded model: {type(model)}")
        if isinstance(model, dict):
            print(f"Model keys: {list(model.keys())}")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")