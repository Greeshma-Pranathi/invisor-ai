#!/usr/bin/env python3
"""
Test script to verify model loading and basic functionality
"""
import sys
import os
from pathlib import Path

# Add ml_src to path
ml_src_path = str(Path(__file__).parent / "ml_src")
if ml_src_path not in sys.path:
    sys.path.insert(0, ml_src_path)

print("Testing model loading...")

try:
    from models.model_interface import model_interface
    print("✅ Model interface imported successfully")
    
    # Check model info
    info = model_interface.get_model_info()
    print(f"Model info: {info}")
    
    if info['churn_model_loaded']:
        print("✅ Churn model loaded successfully")
    else:
        print("❌ Churn model not loaded")
    
    if info['segmentation_model_loaded']:
        print("✅ Segmentation model loaded successfully")
    else:
        print("❌ Segmentation model not loaded")
    
    # Test with sample data
    import pandas as pd
    import numpy as np
    
    # Create sample data with correct column names
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
    
    print(f"\nTesting with sample data: {len(sample_data)} customers")
    
    # Test churn prediction
    if info['churn_model_loaded']:
        try:
            churn_results = model_interface.predict_churn(sample_data)
            print(f"✅ Churn prediction successful: {len(churn_results)} results")
            print(f"Sample result: {churn_results[0] if churn_results else 'None'}")
        except Exception as e:
            print(f"❌ Churn prediction failed: {e}")
    
    # Test segmentation
    if info['segmentation_model_loaded']:
        try:
            segment_results = model_interface.predict_segments(sample_data)
            print(f"✅ Segmentation successful: {len(segment_results)} results")
            print(f"Sample result: {segment_results[0] if segment_results else 'None'}")
        except Exception as e:
            print(f"❌ Segmentation failed: {e}")
    
    # Test explainability
    try:
        sys.path.append('explainability')
        from shap_explainer import shap_explainer
        print("✅ Explainability module imported successfully")
        
        if info['churn_model_loaded']:
            # Extract the actual model for explainability
            churn_model = model_interface.churn_model
            if isinstance(churn_model, dict):
                churn_model = churn_model['model']
            
            explanations = shap_explainer.explain_predictions(sample_data, churn_model)
            print(f"✅ Explanations generated: {explanations['explanation_type']}")
        
    except Exception as e:
        print(f"❌ Explainability test failed: {e}")

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")