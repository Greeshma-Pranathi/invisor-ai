import shap
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import io
import base64
import sys
from pathlib import Path

# Add ml_src to path for importing explainability modules
sys.path.append(str(Path(__file__).parent.parent / "ml_src"))

try:
    from explainability import generate_global_explanations, generate_local_explanations
    from model_config import MODEL_PATHS
except ImportError as e:
    print(f"Warning: Could not import explainability modules: {e}")

class ShapExplainer:
    """SHAP-based explainability for ML models"""
    
    def __init__(self):
        self.explainer = None
        self.shap_values = None
        self.feature_names = None
        self.global_importance_cache = None
        self._load_precomputed_explanations()
    
    def _load_precomputed_explanations(self):
        """Load precomputed global feature importance if available"""
        try:
            explainability_dir = Path(__file__).parent.parent / "ml_models" / "explainability"
            global_importance_file = explainability_dir / "global_feature_importance.csv"
            
            if global_importance_file.exists():
                self.global_importance_cache = pd.read_csv(global_importance_file)
                print("✅ Loaded precomputed global feature importance")
            else:
                print("⚠️ No precomputed explanations found")
                
        except Exception as e:
            print(f"⚠️ Could not load precomputed explanations: {e}")
    
    def initialize_explainer(self, model, background_data: pd.DataFrame):
        """Initialize SHAP explainer with model and background data"""
        try:
            # Determine the best explainer type based on model
            model_type = str(type(model)).lower()
            
            if 'xgb' in model_type or 'lightgbm' in model_type or 'catboost' in model_type:
                # Tree-based models
                self.explainer = shap.TreeExplainer(model)
                print("✅ Using TreeExplainer for tree-based model")
            elif hasattr(model, 'predict_proba'):
                # General ML models with probability prediction
                self.explainer = shap.Explainer(model, background_data.sample(min(100, len(background_data))))
                print("✅ Using general Explainer")
            else:
                # Linear models or others
                self.explainer = shap.LinearExplainer(model, background_data)
                print("✅ Using LinearExplainer")
            
            self.feature_names = background_data.columns.tolist()
            return True
            
        except Exception as e:
            print(f"❌ Error initializing SHAP explainer: {e}")
            # Fallback to basic explainer
            try:
                self.explainer = shap.Explainer(model.predict, background_data.sample(min(50, len(background_data))))
                self.feature_names = background_data.columns.tolist()
                print("✅ Using fallback Explainer")
                return True
            except Exception as e2:
                print(f"❌ Fallback explainer also failed: {e2}")
                return False
    
    def explain_predictions(self, data: pd.DataFrame, model=None) -> Dict[str, Any]:
        """Generate SHAP explanations for predictions"""
        
        # Try to use real explainability first
        if model is not None:
            try:
                return self._generate_real_explanations(data, model)
            except Exception as e:
                print(f"⚠️ Real explanations failed: {e}")
        
        # Try using precomputed explanations
        if self.global_importance_cache is not None:
            try:
                return self._use_precomputed_explanations(data)
            except Exception as e:
                print(f"⚠️ Precomputed explanations failed: {e}")
        
        
        # If all else fails, return error
        raise ValueError("Could not generate explanations using real model or precomputed data.")
    
    def _generate_real_explanations(self, data: pd.DataFrame, model) -> Dict[str, Any]:
        """Generate real SHAP explanations using the ML model"""
        
        # Initialize explainer if not done
        if self.explainer is None:
            if not self.initialize_explainer(model, data.sample(min(50, len(data)))):
                raise Exception("Could not initialize SHAP explainer")
        
        # Calculate SHAP values for a sample of data (to avoid memory issues)
        sample_size = min(20, len(data))
        sample_data = data.head(sample_size)
        
        shap_values = self.explainer(sample_data)
        self.shap_values = shap_values
        
        # Global feature importance
        global_importance = self._calculate_global_importance(shap_values)
        
        # Individual explanations
        individual_explanations = self._generate_individual_explanations(shap_values, sample_data)
        
        # Summary plot
        summary_plot = self._generate_summary_plot(shap_values)
        
        return {
            "global_feature_importance": global_importance,
            "individual_explanations": individual_explanations,
            "summary_plot": summary_plot,
            "explanation_type": "real_shap"
        }
    
    def _use_precomputed_explanations(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Use precomputed explainability results"""
        
        # Use cached global importance
        global_importance = []
        for _, row in self.global_importance_cache.iterrows():
            global_importance.append({
                "feature": row['feature'],
                "importance": round(float(row['importance']), 3),
                "rank": int(row.get('rank', 0))
            })
        
        # Generate individual explanations based on feature importance patterns
        individual_explanations = []
        top_features = [item['feature'] for item in global_importance[:5]]
        
        for i in range(min(5, len(data))):
            explanations = []
            for feature in top_features:
                if feature in data.columns:
                    # Simulate SHAP value based on feature importance and value
                    feature_value = data.iloc[i][feature]
                    base_importance = next((item['importance'] for item in global_importance if item['feature'] == feature), 0.1)
                    
                    # Simulate SHAP value (positive/negative based on feature value)
                    if pd.isna(feature_value):
                        shap_val = 0
                    else:
                        # Normalize feature value and apply importance
                        normalized_val = (feature_value - data[feature].mean()) / (data[feature].std() + 1e-8)
                        shap_val = normalized_val * base_importance * 0.1
                    
                    # Convert numpy types to Python types
                    if hasattr(feature_value, 'item'):
                        feature_value = feature_value.item()
                    elif isinstance(feature_value, (np.integer, np.floating)):
                        feature_value = float(feature_value)
                    
                    explanations.append({
                        "feature": feature,
                        "shap_value": round(float(shap_val), 3),
                        "feature_value": feature_value,
                        "impact": "Positive" if shap_val > 0 else "Negative"
                    })
            
            individual_explanations.append({
                "customer_id": i,
                "explanations": explanations
            })
        
        return {
            "global_feature_importance": global_importance,
            "individual_explanations": individual_explanations,
            "summary_plot": None,
            "explanation_type": "precomputed"
        }
    
    def _calculate_global_importance(self, shap_values) -> List[Dict[str, Any]]:
        """Calculate global feature importance from SHAP values"""
        # Calculate mean absolute SHAP values for each feature
        if hasattr(shap_values, 'values'):
            importance_scores = np.abs(shap_values.values).mean(axis=0)
        else:
            importance_scores = np.abs(shap_values).mean(axis=0)
        
        # Create feature importance list
        feature_importance = []
        for i, (feature, score) in enumerate(zip(self.feature_names, importance_scores)):
            feature_importance.append({
                "feature": feature,
                "importance": round(float(score), 3),
                "rank": i + 1
            })
        
        # Sort by importance
        feature_importance.sort(key=lambda x: x["importance"], reverse=True)
        
        # Update ranks
        for i, item in enumerate(feature_importance):
            item["rank"] = i + 1
        
        return feature_importance
    
    def _generate_individual_explanations(self, shap_values, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate individual SHAP explanations"""
        explanations = []
        
        # Limit to available data
        n_customers = min(len(data), 10)
        
        for i in range(n_customers):
            if hasattr(shap_values, 'values'):
                customer_shap = shap_values.values[i]
            else:
                customer_shap = shap_values[i]
            
            customer_explanations = []
            for j, (feature, shap_val) in enumerate(zip(self.feature_names, customer_shap)):
                feature_value = data.iloc[i, j] if j < len(data.columns) else "N/A"
                
                # Convert numpy types to Python types
                if hasattr(feature_value, 'item'):
                    feature_value = feature_value.item()
                elif isinstance(feature_value, (np.integer, np.floating)):
                    feature_value = float(feature_value)
                
                customer_explanations.append({
                    "feature": feature,
                    "shap_value": round(float(shap_val), 3),
                    "feature_value": feature_value,
                    "impact": "Positive" if shap_val > 0 else "Negative"
                })
            
            # Sort by absolute SHAP value
            customer_explanations.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
            
            explanations.append({
                "customer_id": i,
                "explanations": customer_explanations[:5]  # Top 5 features
            })
        
        return explanations
    
    def _generate_summary_plot(self, shap_values) -> Optional[str]:
        """Generate SHAP summary plot as base64 encoded image"""
        try:
            plt.figure(figsize=(10, 6))
            
            # Create summary plot
            if hasattr(shap_values, 'values'):
                shap.summary_plot(shap_values.values, feature_names=self.feature_names, show=False)
            else:
                shap.summary_plot(shap_values, feature_names=self.feature_names, show=False)
            
            # Convert plot to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
            buffer.seek(0)
            plot_data = buffer.getvalue()
            buffer.close()
            plt.close()
            
            # Encode as base64
            plot_base64 = base64.b64encode(plot_data).decode('utf-8')
            return f"data:image/png;base64,{plot_base64}"
        
        except Exception as e:
            print(f"❌ Error generating summary plot: {e}")
            plt.close()  # Ensure plot is closed
            return None
    


# Global explainer instance
shap_explainer = ShapExplainer()