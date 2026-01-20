#!/usr/bin/env python3
"""
Data mapping utility to handle different column names between uploaded data and model expectations
"""
import pandas as pd
import numpy as np

# Column mapping from uploaded data to model expected columns
COLUMN_MAPPING = {
    # Direct mappings
    'tenure': 'tenure_months',
    'age': 'age',
    'gender': 'gender', 
    'monthly_charges': 'monthly_charges',
    'total_charges': 'total_charges',
    'contract_type': 'contract_type',
    'customer_id': 'customer_id',
    'location': 'region',
    'balance': 'balance',
    'num_products': 'num_products',
    'engagement_score': 'engagement_score',
    
    # Additional possible mappings
    'contract': 'contract_type',
    'region': 'region',
    'area': 'region',
    'city': 'region',
}

# Required columns for the churn model (based on sample data structure)
REQUIRED_CHURN_COLUMNS = [
    'customer_id', 'gender', 'senior_citizen', 'partner', 'dependents', 
    'tenure_months', 'contract_type', 'payment_method', 'monthly_charges', 
    'total_charges', 'internet_service', 'online_security', 'tech_support', 
    'paperless_billing', 'streaming_tv', 'streaming_movies', 'multiple_lines',
    'avg_monthly_usage_gb', 'support_tickets_last_6m', 'late_payments_last_year',
    'autopay_enabled', 'billing_cycle', 'region'
]

# Default values for missing columns
DEFAULT_VALUES = {
    'senior_citizen': 0,
    'partner': 'No',
    'dependents': 'No',
    'payment_method': 'Electronic check',
    'internet_service': 'DSL',
    'online_security': 'No',
    'tech_support': 'No',
    'paperless_billing': 'Yes',
    'streaming_tv': 'No',
    'streaming_movies': 'No',
    'multiple_lines': 'No',
    'avg_monthly_usage_gb': 100.0,
    'support_tickets_last_6m': 0,
    'late_payments_last_year': 0,
    'autopay_enabled': 'No',
    'billing_cycle': 'Monthly',
    'region': 'Urban'
}

def map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Map uploaded data columns to model expected columns"""
    df_mapped = df.copy()
    
    # Apply column mapping
    for old_col, new_col in COLUMN_MAPPING.items():
        if old_col in df_mapped.columns and old_col != new_col:
            df_mapped[new_col] = df_mapped[old_col]
            # Keep original column for now, we'll clean up later
    
    return df_mapped

def add_missing_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add missing columns with default values"""
    df_complete = df.copy()
    
    for col in REQUIRED_CHURN_COLUMNS:
        if col not in df_complete.columns:
            if col in DEFAULT_VALUES:
                df_complete[col] = DEFAULT_VALUES[col]
                print(f"Added missing column '{col}' with default value: {DEFAULT_VALUES[col]}")
            else:
                # Try to derive from existing data
                if col == 'senior_citizen' and 'age' in df_complete.columns:
                    df_complete[col] = (df_complete['age'] >= 65).astype(int)
                    print(f"Derived '{col}' from age column")
                elif col == 'partner' and 'gender' in df_complete.columns:
                    # Simple heuristic: assume some customers have partners
                    df_complete[col] = np.random.choice(['Yes', 'No'], size=len(df_complete), p=[0.4, 0.6])
                    print(f"Generated '{col}' with random distribution")
                elif col == 'dependents' and 'age' in df_complete.columns:
                    # Younger customers more likely to have dependents
                    prob_dependents = np.where(df_complete['age'] < 40, 0.3, 0.1)
                    df_complete[col] = np.random.choice(['Yes', 'No'], size=len(df_complete), p=[prob_dependents, 1-prob_dependents])
                    print(f"Generated '{col}' based on age distribution")
                elif col == 'avg_monthly_usage_gb' and 'monthly_charges' in df_complete.columns:
                    # Higher charges might correlate with higher usage
                    base_usage = 50 + (df_complete['monthly_charges'] - df_complete['monthly_charges'].min()) * 2
                    df_complete[col] = np.clip(base_usage, 10, 500)
                    print(f"Derived '{col}' from monthly charges")
                elif col == 'support_tickets_last_6m' and 'engagement_score' in df_complete.columns:
                    # Lower engagement might mean more support tickets
                    tickets = np.random.poisson(lam=np.clip(2 * (1 - df_complete['engagement_score']), 0.1, 3))
                    df_complete[col] = np.clip(tickets, 0, 10)
                    print(f"Derived '{col}' from engagement score")
                else:
                    df_complete[col] = 'Unknown'
                    print(f"Added missing column '{col}' with default value: Unknown")
    
    return df_complete

def prepare_data_for_model(df: pd.DataFrame, model_type: str = 'churn') -> pd.DataFrame:
    """Prepare uploaded data for ML model consumption"""
    
    print(f"Original data shape: {df.shape}")
    print(f"Original columns: {list(df.columns)}")
    
    # Step 1: Map columns
    df_mapped = map_columns(df)
    print(f"After mapping: {list(df_mapped.columns)}")
    
    # Step 2: Add missing columns for both churn and segmentation
    df_complete = add_missing_columns(df_mapped)
    print(f"After adding missing columns: {df_complete.shape}")
    
    # Step 3: Select required columns based on model type
    if model_type == 'churn':
        df_final = df_complete[REQUIRED_CHURN_COLUMNS].copy()
    elif model_type == 'segmentation':
        # Segmentation uses the same columns as churn model
        df_final = df_complete[REQUIRED_CHURN_COLUMNS].copy()
    else:
        # Fallback: use all available columns
        df_final = df_complete.copy()
    
    print(f"Final data shape: {df_final.shape}")
    print(f"Final columns: {list(df_final.columns)}")
    
    return df_final

if __name__ == "__main__":
    # Test with current data
    try:
        df = pd.read_csv("current_data.csv")
        print("Testing data mapping...")
        df_prepared = prepare_data_for_model(df, 'churn')
        print("✅ Data mapping successful!")
        print(f"Sample prepared data:\n{df_prepared.head()}")
    except Exception as e:
        print(f"❌ Data mapping failed: {e}")