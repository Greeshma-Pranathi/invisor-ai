# Invisor.ai - Customer Intelligence Platform

![Invisor.ai Banner](https://via.placeholder.com/1200x500.png?text=Invisor.ai)

**Invisor.ai** is an advanced AI-powered dashboard designed to provide deep insights into customer behavior. It combines churn prediction, customer segmentation, and explainable AI to help businesses make data-driven decisions.

## 🚀 Features

-   **📊 Churn Prediction**: Identify at-risk customers with high accuracy using ML models.
-   **🎯 Smart Segmentation**: Automatically group customers based on behavior and value.
-   **🧠 Explainable AI**: Understand *why* a customer is at risk with SHAP-based feature importance.
-   **💬 AI Chatbot**: Query your data using natural language to get instant insights.
-   **📂 Easy Data Upload**: Drag-and-drop CSV upload with automatic validation and processing.

## 🏗️ Architecture

The project is divided into two main components:

-   **Frontend (`/frontend`)**: A modern, responsive React application built with Vite, Tailwind CSS, and Framer Motion.
-   **Backend (`/backend`)**: A robust FastAPI server handling ML inference, data processing, and API endpoints.

## 🛠️ System Requirements

-   **Node.js**: v18+
-   **Python**: v3.9+
-   **OS**: Windows, macOS, or Linux

## 🏁 Getting Started

### 1. Backend Setup
Navigate to the backend directory and set up the Python environment.

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python start_server.py
```
The backend API will run at `http://localhost:8000`.

### 2. Frontend Setup
Navigate to the frontend directory and start the development server.

```bash
cd frontend
npm install
npm run dev
```
The frontend UI will run at `http://localhost:5173` (or the next available port).

## 🧪 Testing

-   **Backend**: `pytest` (in `backend/` directory)
-   **Frontend**: `npm run test` (if configured)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
