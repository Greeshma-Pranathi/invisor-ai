import requests
import os

BASE_URL = "http://localhost:8000"
FILE_PATH = r"c:\Users\prajy\OneDrive\Desktop\invisor-ai\backend\current_data.csv"

def upload_data():
    if not os.path.exists(FILE_PATH):
        print(f"❌ File not found: {FILE_PATH}")
        return False
        
    print(f"Uploading {FILE_PATH}...")
    try:
        with open(FILE_PATH, 'rb') as f:
            files = {'file': ('project_ready_customers.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload-csv", files=files)
            
        if response.status_code == 200:
            print("Upload successful!")
            print(response.json())
            return True
        else:
            print(f"Upload failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def trigger_processing():
    print("Triggering Churn Prediction...")
    try:
        print("Loading Models...")
        res = requests.post(f"{BASE_URL}/load-models", json={})
        if res.status_code == 200:
             print("Models loaded.")
        else:
             print(f"Load Models failed: {res.text}")

        print("Triggering Churn Prediction...")
        res = requests.post(f"{BASE_URL}/predict-churn")
        if res.status_code == 200:
            print("Churn Prediction generated.")
        else:
            print(f"Churn Prediction error: {res.text}")
            
        res = requests.post(f"{BASE_URL}/customer-segmentation")
        if res.status_code == 200:
            print("Segmentation generated.")
        else:
            print(f"Segmentation error: {res.text}")
            
        # Check Chatbot
        res = requests.post(f"{BASE_URL}/chatbot/query", json={"query": "features"})
        if res.status_code == 200:
            print(f"Chatbot check: {res.json()['response'][:100]}...")
        else:
            print(f"Chatbot check failed: {res.text}")

    except Exception as e:
        print(f"Processing Error: {e}")

if __name__ == "__main__":
    if upload_data():
        trigger_processing()
