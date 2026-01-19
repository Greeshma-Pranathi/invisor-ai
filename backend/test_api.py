#!/usr/bin/env python3
"""
Simple test script for Invisor.ai Backend API
"""

import requests
import pandas as pd
import io
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_csv_upload():
    """Test CSV upload with sample data"""
    print("📁 Testing CSV upload...")
    
    # Create sample customer data
    contract_types = ['Month-to-month', 'One year', 'Two year']
    sample_data = {
        'customer_id': range(1, 101),
        'age': [25 + i % 40 for i in range(100)],
        'monthly_charges': [50 + i % 100 for i in range(100)],
        'total_charges': [500 + i * 10 for i in range(100)],
        'tenure': [1 + i % 60 for i in range(100)],
        'contract_type': [contract_types[i % 3] for i in range(100)]
    }
    
    df = pd.DataFrame(sample_data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()
    
    # Upload CSV
    files = {'file': ('sample_data.csv', csv_content, 'text/csv')}
    response = requests.post(f"{BASE_URL}/upload-csv", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Uploaded {result['rows']} rows with {result['columns']} columns")
        print(f"Columns: {result['column_names']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_churn_prediction():
    """Test churn prediction endpoint"""
    print("🎯 Testing churn prediction...")
    response = requests.post(f"{BASE_URL}/predict-churn")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Generated predictions for {result['total_customers']} customers")
        print(f"High risk: {result['high_risk_count']}")
        print(f"Sample prediction: {result['predictions'][0]}")
    else:
        print(f"Error: {response.text}")
    print()

def test_segmentation():
    """Test customer segmentation endpoint"""
    print("👥 Testing customer segmentation...")
    response = requests.post(f"{BASE_URL}/customer-segmentation")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Generated segments for {result['total_customers']} customers")
        print("Segment summary:")
        for segment, info in result['segment_summary'].items():
            print(f"  {segment}: {info['count']} customers ({info['percentage']}%)")
    else:
        print(f"Error: {response.text}")
    print()

def test_explainability():
    """Test explainability endpoint"""
    print("🔍 Testing explainability...")
    response = requests.post(f"{BASE_URL}/explainability")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("Top 3 important features:")
        for i, feature in enumerate(result['global_feature_importance'][:3]):
            print(f"  {i+1}. {feature['feature']}: {feature['importance']}")
        print(f"Individual explanations for {len(result['individual_explanations'])} customers")
    else:
        print(f"Error: {response.text}")
    print()

def test_chatbot():
    """Test chatbot endpoints"""
    print("🤖 Testing chatbot...")
    
    # Test insights
    response = requests.get(f"{BASE_URL}/chatbot/insights")
    print(f"Insights status: {response.status_code}")
    if response.status_code == 200:
        insights = response.json()['insights']
        print(f"Got {len(insights)} insights")
    
    # Test query
    query_data = {"question": "What is churn prediction?"}
    response = requests.post(f"{BASE_URL}/chatbot/query", json=query_data)
    print(f"Query status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Chatbot response: {result['response']}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting Invisor.ai Backend API Tests")
    print("=" * 50)
    
    try:
        test_health_check()
        test_csv_upload()
        test_churn_prediction()
        test_segmentation()
        test_explainability()
        test_chatbot()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server.")
        print("   Make sure the server is running on http://localhost:8000")
        print("   Run: python start_server.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()