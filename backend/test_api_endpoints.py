#!/usr/bin/env python3
"""
Test API endpoints to verify functionality
"""
import requests
import json
import pandas as pd
import io

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_upload():
    """Test CSV upload"""
    try:
        # Create sample CSV data
        sample_data = pd.DataFrame({
            'customer_id': ['C001', 'C002'],
            'gender': ['Female', 'Male'],
            'senior_citizen': [0, 0],
            'partner': ['Yes', 'No'],
            'dependents': ['No', 'No'],
            'tenure_months': [12, 36],
            'contract_type': ['Month-to-month', 'Two year'],
            'payment_method': ['Electronic check', 'Credit card'],
            'monthly_charges': [50.0, 80.0],
            'total_charges': [600.0, 2880.0],
            'internet_service': ['DSL', 'Fiber optic'],
            'online_security': ['No', 'Yes'],
            'tech_support': ['No', 'Yes'],
            'paperless_billing': ['Yes', 'No'],
            'streaming_tv': ['No', 'Yes'],
            'streaming_movies': ['No', 'Yes'],
            'multiple_lines': ['No', 'Yes'],
            'avg_monthly_usage_gb': [100.0, 200.0],
            'support_tickets_last_6m': [1, 0],
            'late_payments_last_year': [0, 0],
            'autopay_enabled': ['No', 'Yes'],
            'billing_cycle': ['Monthly', 'Monthly'],
            'region': ['South', 'North']
        })
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        sample_data.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        
        # Upload
        files = {'file': ('test_data.csv', csv_content, 'text/csv')}
        response = requests.post(f"{BASE_URL}/upload-csv", files=files)
        
        print(f"Upload test: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Upload test failed: {e}")
        return False

def test_churn_prediction():
    """Test churn prediction endpoint"""
    try:
        response = requests.post(f"{BASE_URL}/predict-churn")
        print(f"Churn prediction: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if response.status_code == 200 and 'predictions' in result:
            print(f"✅ Got {len(result['predictions'])} churn predictions")
            return True
        return False
        
    except Exception as e:
        print(f"Churn prediction test failed: {e}")
        return False

def test_segmentation():
    """Test segmentation endpoint"""
    try:
        response = requests.post(f"{BASE_URL}/customer-segmentation")
        print(f"Segmentation: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if response.status_code == 200 and 'segments' in result:
            print(f"✅ Got {len(result['segments'])} segments")
            return True
        return False
        
    except Exception as e:
        print(f"Segmentation test failed: {e}")
        return False

def test_explainability():
    """Test explainability endpoint"""
    try:
        response = requests.post(f"{BASE_URL}/explainability")
        print(f"Global explainability: {response.status_code}")
        result = response.json()
        print(f"Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if response.status_code == 200:
            print("✅ Global explanations working")
            return True
        return False
        
    except Exception as e:
        print(f"Explainability test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    tests = [
        ("Health Check", test_health),
        ("CSV Upload", test_upload),
        ("Churn Prediction", test_churn_prediction),
        ("Segmentation", test_segmentation),
        ("Explainability", test_explainability)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'✅ PASS' if success else '❌ FAIL'}")
    
    print(f"\n--- SUMMARY ---")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")