import uvicorn
import os
import sys

# Redirect stdout/stderr to file for capture
sys.stdout = open('output.txt', 'w', buffering=1, encoding='utf-8')
sys.stderr = sys.stdout

# Ensure current dir is in path
sys.path.append(os.getcwd())
# Ensure ml_src is in path
sys.path.append(os.path.join(os.getcwd(), 'ml_src'))

if __name__ == "__main__":
    print("🚀 Starting Backend Programmatically...")
    
    try:
        from models.model_interface import model_interface
        print("✅ Model Interface imported")
        model_interface._auto_load_models()
        print(f"DEBUG: Churn Model after auto-load: {model_interface.churn_model is not None}")
    except Exception as e:
        print(f"❌ Error during manual load check: {e}")
        import traceback
        traceback.print_exc()

    # Start Uvicorn
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
    except Exception as e:
        print(f"CRITICAL SERVER ERROR: {e}")
        import traceback
        traceback.print_exc()
