import joblib
import os
import sys
import sklearn
import pandas as pd
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), "ml_src"))

print(f"Python: {sys.version}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Numpy: {np.__version__}")

model_dir = r"c:\Users\prajy\OneDrive\Desktop\invisor-ai\backend\ml_models"
churn_path = os.path.join(model_dir, "final_churn_model.pkl")

print(f"\nAttempting to load: {churn_path}")
if not os.path.exists(churn_path):
    print("ERROR: File not found!")
else:
    try:
        model = joblib.load(churn_path)
        print("SUCCESS: Model loaded.")
        print(f"Type: {type(model)}")
    except Exception as e:
        print(f"ERROR: Failed to load model: {e}")
        import traceback
        traceback.print_exc()
