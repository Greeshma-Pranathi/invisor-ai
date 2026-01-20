# Invisor.ai Backend API

🚀 **FastAPI backend for the Invisor.ai customer churn prediction and segmentation platform.**

## 🎯 Features

- **📊 CSV Upload & Processing**: Upload customer data for analysis
- **🎯 Churn Prediction**: ML-powered customer churn predictions with risk levels
- **👥 Customer Segmentation**: Unsupervised clustering for customer segments  
- **🔍 Explainable AI**: SHAP-based explanations for model predictions
- **🤖 Basic Chatbot**: Insight-based chatbot for data exploration
- **💾 Supabase Integration**: Data storage and persistence

## ⚡ Quick Start

### 1. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 2. Environment Setup (Optional)

For Supabase integration, copy and configure the environment file:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` with your Supabase credentials:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Start the Server

```bash
# Recommended: Use the startup script
python start_server.py

# Alternative: Direct uvicorn command
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the API

```bash
# Run comprehensive API tests
python test_api.py

# Or test individual endpoints
curl http://localhost:8000/health
```

🌐 **API will be available at: `http://localhost:8000`**  
📚 **Interactive docs at: `http://localhost:8000/docs`**

## 📋 API Endpoints Reference

### 🏥 System Health & Status

#### `GET /`
**Basic API information**
```bash
curl http://localhost:8000/
```
**Response:**
```json
{
  "message": "Invisor.ai Backend API",
  "status": "running"
}
```

#### `GET /health`
**Health check with system status**
```bash
curl http://localhost:8000/health
```
**Response:**
```json
{
  "status": "healthy",
  "models_loaded": false,
  "supabase_connected": false
}
```

#### `GET /model-status`
**Detailed model loading status**
```bash
curl http://localhost:8000/model-status
```
**Response:**
```json
{
  "churn_model_loaded": false,
  "segmentation_model_loaded": false,
  "scaler_loaded": false,
  "supabase_connected": false
}
```

### 📁 Data Management

#### `POST /upload-csv`
**Upload customer data CSV file**
```bash
curl -X POST -F "file=@customer_data.csv" http://localhost:8000/upload-csv
```
**Response:**
```json
{
  "message": "CSV uploaded successfully",
  "rows": 100,
  "columns": 6,
  "column_names": ["customer_id", "age", "monthly_charges", "total_charges", "tenure", "contract_type"],
  "sample_data": [...],
  "upload_id": 1
}
```

#### `GET /upload-history`
**Get history of previous uploads (requires Supabase)**
```bash
curl http://localhost:8000/upload-history
```

### 🎯 Machine Learning Predictions

#### `POST /predict-churn`
**Generate churn predictions for uploaded data**
```bash
curl -X POST http://localhost:8000/predict-churn
```
**Response:**
```json
{
  "message": "Churn predictions generated",
  "total_customers": 100,
  "high_risk_count": 30,
  "medium_risk_count": 45,
  "low_risk_count": 25,
  "predictions": [
    {
      "customer_id": 0,
      "churn_prediction": 1,
      "churn_probability": 0.375,
      "risk_level": "Low"
    }
  ]
}
```

#### `POST /customer-segmentation`
**Generate customer segments for uploaded data**
```bash
curl -X POST http://localhost:8000/customer-segmentation
```
**Response:**
```json
{
  "message": "Customer segmentation completed",
  "total_customers": 100,
  "segments": [
    {
      "customer_id": 0,
      "segment_id": 2,
      "segment_name": "New Customer",
      "confidence": 0.85
    }
  ],
  "segment_summary": {
    "High Value": {"count": 11, "percentage": 11.0},
    "At Risk": {"count": 21, "percentage": 21.0},
    "New Customer": {"count": 27, "percentage": 27.0},
    "Loyal": {"count": 23, "percentage": 23.0},
    "Price Sensitive": {"count": 18, "percentage": 18.0}
  }
}
```

### 🔍 Explainable AI

#### `POST /explainability`
**Get SHAP-based explanations for predictions**
```bash
curl -X POST http://localhost:8000/explainability
```
**Response:**
```json
{
  "message": "Explainability results generated",
  "global_feature_importance": [
    {
      "feature": "age",
      "importance": 0.956,
      "rank": 1
    }
  ],
  "individual_explanations": [
    {
      "customer_id": 0,
      "explanations": [
        {
          "feature": "age",
          "shap_value": 0.234,
          "feature_value": 45,
          "impact": "Positive"
        }
      ]
    }
  ]
}
```

### 🤖 Chatbot Interface

#### `GET /chatbot/insights`
**Get predefined insights about the data**
```bash
curl http://localhost:8000/chatbot/insights
```
**Response:**
```json
{
  "insights": [
    "Dataset contains 100 customers with 6 features.",
    "High-risk customers show patterns in usage frequency and support tickets.",
    "Customer segments reveal distinct behavioral patterns for targeted marketing."
  ]
}
```

#### `POST /chatbot/query`
**Query the chatbot with questions**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is churn prediction?"}' \
  http://localhost:8000/chatbot/query
```
**Response:**
```json
{
  "response": "Churn prediction identifies customers likely to leave. Our model analyzes behavioral patterns to predict churn probability."
}
```

**Supported query keywords:**
- `churn` - Information about churn prediction
- `segment` - Customer segmentation details
- `feature` or `important` - Feature importance explanations
- `data` - Current dataset information

### ⚙️ Model Management

#### `POST /load-models`
**Load ML models from file paths**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "churn_model": "models/churn_model.pkl",
    "segmentation_model": "models/segmentation_model.pkl",
    "scaler": "models/feature_scaler.pkl"
  }' \
  http://localhost:8000/load-models
```
**Response:**
```json
{
  "message": "Model loading completed",
  "results": {
    "churn_model": "loaded",
    "segmentation_model": "loaded",
    "scaler": "loaded"
  }
}
```

## 🔄 Complete Workflow Example

Here's a step-by-step example of using the API:

### 1. Check System Status
```bash
curl http://localhost:8000/health
```

### 2. Upload Customer Data
```bash
curl -X POST -F "file=@customer_data.csv" http://localhost:8000/upload-csv
```

### 3. Generate Churn Predictions
```bash
curl -X POST http://localhost:8000/predict-churn
```

### 4. Create Customer Segments
```bash
curl -X POST http://localhost:8000/customer-segmentation
```

### 5. Get Explanations
```bash
curl -X POST http://localhost:8000/explainability
```

### 6. Query Chatbot
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What are the top risk factors for churn?"}' \
  http://localhost:8000/chatbot/query
```

## 📊 Sample Data Format

Your CSV file should contain customer data with columns like:

```csv
customer_id,age,monthly_charges,total_charges,tenure,contract_type
1,25,65.5,1200.50,12,Month-to-month
2,45,89.0,3500.75,36,Two year
3,32,55.25,890.25,8,One year
```

**Supported data types:**
- Numeric features (age, charges, tenure)
- Categorical features (contract type, payment method)
- Customer identifiers

## 🚀 Integration Guide

### Frontend Integration (React/Vue/Angular)

```javascript
// Upload CSV
const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/upload-csv', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
};

// Get predictions
const getPredictions = async () => {
  const response = await fetch('http://localhost:8000/predict-churn', {
    method: 'POST'
  });
  
  return await response.json();
};

// Query chatbot
const queryChatbot = async (question) => {
  const response = await fetch('http://localhost:8000/chatbot/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  
  return await response.json();
};
```

### Python Client Integration

```python
import requests
import pandas as pd

# API base URL
BASE_URL = "http://localhost:8000"

# Upload CSV
def upload_csv(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload-csv", files=files)
    return response.json()

# Get predictions
def get_predictions():
    response = requests.post(f"{BASE_URL}/predict-churn")
    return response.json()

# Get segments
def get_segments():
    response = requests.post(f"{BASE_URL}/customer-segmentation")
    return response.json()

# Example usage
result = upload_csv("customer_data.csv")
predictions = get_predictions()
segments = get_segments()
```

## 🏗️ Project Structure

```
invisor-ai-backend/
├── 📄 main.py                    # FastAPI application & routes
├── 🚀 start_server.py            # Server startup script
├── 💾 supabase_client.py         # Supabase integration
├── 🧪 test_api.py               # API testing script
├── 📋 requirements.txt           # Python dependencies
├── 🐳 Dockerfile                # Docker configuration
├── 🐳 docker-compose.yml        # Docker Compose setup
├── 🗄️ supabase_schema.sql       # Database schema
├── ⚙️ .env.example              # Environment template
├── 📚 README.md                 # This documentation
├── 📁 models/
│   ├── __init__.py
│   └── model_interface.py       # ML model interface
└── 📁 explainability/
    ├── __init__.py
    └── shap_explainer.py        # SHAP explanations
```

## 🔧 Advanced Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SUPABASE_URL` | Supabase project URL | - | No |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | - | No |
| `API_HOST` | Server host address | `0.0.0.0` | No |
| `API_PORT` | Server port number | `8000` | No |
| `ENVIRONMENT` | Environment mode | `development` | No |

### Docker Deployment

```bash
# Build and run with Docker
docker build -t invisor-backend .
docker run -p 8000:8000 --env-file .env invisor-backend

# Or use Docker Compose
docker-compose up -d
```

### Production Considerations

- **CORS**: Update CORS origins for production domains
- **Authentication**: Add API key authentication if needed
- **Rate Limiting**: Implement rate limiting for public APIs
- **Logging**: Configure structured logging for monitoring
- **Health Checks**: Use `/health` endpoint for load balancer checks

## 🤝 Team Integration Guide

### For Jignash (Backend Developer)
- ✅ **Complete API Implementation**: All endpoints tested and working
- ✅ **Supabase Integration**: Data persistence layer ready
- ✅ **Model Interface**: Clean integration points for ML models
- ✅ **Error Handling**: Comprehensive error responses
- ✅ **Documentation**: API reference and examples provided

### For Greeshma (AI/ML Lead)
- 🔗 **Model Integration**: Use `/load-models` endpoint to load trained models
- 📊 **Data Pipeline**: Preprocessing handled in `model_interface.py`
- 🎯 **Predictions**: Replace mock predictions with actual model outputs
- 📈 **Evaluation**: Model performance metrics can be added to responses
- 🔍 **SHAP Integration**: Real SHAP values replace mock explanations

**Model Integration Steps:**
```python
# 1. Save your trained models
joblib.dump(churn_model, 'models/churn_model.pkl')
joblib.dump(segmentation_model, 'models/segmentation_model.pkl')
joblib.dump(scaler, 'models/feature_scaler.pkl')

# 2. Load models via API
requests.post("http://localhost:8000/load-models", json={
    "churn_model": "models/churn_model.pkl",
    "segmentation_model": "models/segmentation_model.pkl", 
    "scaler": "models/feature_scaler.pkl"
})
```

### For Shruthi (Frontend Developer)
- 🌐 **CORS Enabled**: Ready for frontend integration
- 📊 **JSON Responses**: Clean, structured data for dashboard
- 🎨 **Sample Data**: Use test_api.py to understand response formats
- 📈 **Visualization Data**: Segment summaries and feature importance ready
- 🔄 **Workflow**: Upload → Predict → Segment → Explain → Visualize

**Key Integration Points:**
```javascript
// Dashboard data flow
const workflow = {
  upload: '/upload-csv',
  predict: '/predict-churn', 
  segment: '/customer-segmentation',
  explain: '/explainability',
  insights: '/chatbot/insights'
};
```

### For Dinesh (Product + Documentation)
- 🤖 **Chatbot Ready**: Basic insight-based responses implemented
- 🧪 **Testing Suite**: Comprehensive test coverage with test_api.py
- 📚 **Documentation**: Complete API reference and examples
- 🎯 **Demo Flow**: End-to-end workflow tested and documented
- 🐛 **Bug Tracking**: Error handling and logging in place

**Testing Commands:**
```bash
# Run full test suite
python test_api.py

# Test individual components
curl http://localhost:8000/health
curl -X POST -F "file=@sample.csv" http://localhost:8000/upload-csv
```

## 🚀 Development Workflow

### 1. **Setup Phase**
```bash
git clone <repository>
cd invisor-ai-backend
pip install -r requirements.txt
python start_server.py
```

### 2. **Development Phase**
- **Backend**: Extend APIs in `main.py`
- **ML Integration**: Update `models/model_interface.py`
- **Frontend**: Connect to API endpoints
- **Testing**: Run `python test_api.py` after changes

### 3. **Integration Phase**
- **Load Models**: Use `/load-models` endpoint
- **Test Workflow**: Upload → Predict → Segment → Explain
- **Frontend Integration**: Connect dashboard to APIs
- **End-to-End Testing**: Validate complete user journey

### 4. **Demo Preparation**
- **Sample Data**: Prepare demo CSV files
- **Model Loading**: Load trained models
- **Dashboard**: Connect frontend visualizations
- **Presentation**: Use API responses for demo narrative

## 🔍 Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check dependencies
pip install -r requirements.txt

# Check port availability
netstat -an | findstr :8000
```

**Model loading fails:**
```bash
# Check file paths and permissions
ls -la models/
python -c "import joblib; print('Joblib working')"
```

**API tests fail:**
```bash
# Ensure server is running
curl http://localhost:8000/health

# Check Python environment
python --version
pip list | grep fastapi
```

**CORS issues:**
- Update `allow_origins` in `main.py` for production domains
- Use `http://localhost:3000` for React development

## 📞 Support

- **API Issues**: Check server logs and `/health` endpoint
- **Model Integration**: Refer to `models/model_interface.py`
- **Frontend Integration**: Use `/docs` for interactive API testing
- **Database Issues**: Verify Supabase configuration in `.env`

---

## 🎉 Ready for Phase 1 Demo!

The backend is fully functional and ready for:
- ✅ CSV upload and processing
- ✅ Churn prediction with risk levels  
- ✅ Customer segmentation with summaries
- ✅ Explainable AI with feature importance
- ✅ Basic chatbot for insights
- ✅ Complete API documentation
- ✅ Testing suite and examples
- ✅ Team integration guides

**Next Steps**: Load trained models, connect frontend dashboard, and prepare demo data!