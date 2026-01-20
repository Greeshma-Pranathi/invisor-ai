import os
from supabase import create_client, Client
from typing import Optional, Dict, Any
import pandas as pd
import json
from datetime import datetime

class SupabaseStorage:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        self.client: Optional[Client] = None
        
        if self.url and self.key:
            self.client = create_client(self.url, self.key)
    
    def is_connected(self) -> bool:
        """Check if Supabase client is properly initialized"""
        return self.client is not None
    
    def upload_csv_data(self, filename: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Store CSV data and metadata in Supabase"""
        if not self.is_connected():
            return {"error": "Supabase not configured"}
        
        try:
            # Convert DataFrame to JSON for storage
            data_json = data.to_json(orient='records')
            
            # Create record in uploads table
            upload_record = {
                "filename": filename,
                "upload_time": datetime.now().isoformat(),
                "row_count": len(data),
                "column_count": len(data.columns),
                "columns": data.columns.tolist(),
                "data": data_json
            }
            
            result = self.client.table("uploads").insert(upload_record).execute()
            return {"success": True, "upload_id": result.data[0]["id"]}
            
        except Exception as e:
            return {"error": f"Upload failed: {str(e)}"}
    
    def store_predictions(self, upload_id: int, predictions: list) -> Dict[str, Any]:
        """Store churn predictions"""
        if not self.is_connected():
            return {"error": "Supabase not configured"}
        
        try:
            prediction_record = {
                "upload_id": upload_id,
                "predictions": json.dumps(predictions),
                "created_at": datetime.now().isoformat()
            }
            
            result = self.client.table("predictions").insert(prediction_record).execute()
            return {"success": True, "prediction_id": result.data[0]["id"]}
            
        except Exception as e:
            return {"error": f"Prediction storage failed: {str(e)}"}
    
    def store_segments(self, upload_id: int, segments: list) -> Dict[str, Any]:
        """Store customer segments"""
        if not self.is_connected():
            return {"error": "Supabase not configured"}
        
        try:
            segment_record = {
                "upload_id": upload_id,
                "segments": json.dumps(segments),
                "created_at": datetime.now().isoformat()
            }
            
            result = self.client.table("segments").insert(segment_record).execute()
            return {"success": True, "segment_id": result.data[0]["id"]}
            
        except Exception as e:
            return {"error": f"Segment storage failed: {str(e)}"}
    
    def get_upload_history(self) -> Dict[str, Any]:
        """Get list of previous uploads"""
        if not self.is_connected():
            return {"error": "Supabase not configured"}
        
        try:
            result = self.client.table("uploads").select("*").order("upload_time", desc=True).execute()
            return {"success": True, "uploads": result.data}
            
        except Exception as e:
            return {"error": f"Failed to fetch history: {str(e)}"}

# Global instance
supabase_storage = SupabaseStorage()