# Explainability package
from .shap_explainer import shap_explainer

# Import functions from ml_src if available
try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent / "ml_src"))
    
    # Create wrapper functions for the missing imports
    def generate_global_explanations(model, data, **kwargs):
        """Generate global SHAP explanations"""
        return shap_explainer.explain_predictions(data, model)
    
    def generate_local_explanations(model, data, customer_id=None, **kwargs):
        """Generate local SHAP explanations for specific customers"""
        if customer_id is not None:
            # Filter data for specific customer
            customer_data = data[data.get('customer_id', data.index) == customer_id]
            if customer_data.empty:
                customer_data = data.head(1)  # Fallback to first row
        else:
            customer_data = data.head(5)  # First 5 customers
        
        return shap_explainer.explain_predictions(customer_data, model)
    
    # Export the functions
    __all__ = ['shap_explainer', 'generate_global_explanations', 'generate_local_explanations']
    
except Exception as e:
    print(f"Warning: Could not set up explainability functions: {e}")
    __all__ = ['shap_explainer']