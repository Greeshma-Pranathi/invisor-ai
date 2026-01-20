import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DataProvider } from './context/DataContext';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
// Import other pages as we create them
import Upload from './pages/Upload';
import ChurnAnalysis from './pages/ChurnAnalysis';
import Segmentation from './pages/Segmentation';
import Explainability from './pages/Explainability';
import Chatbot from './pages/Chatbot';

function App() {
  return (
    <DataProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/churn" element={<ChurnAnalysis />} />
            <Route path="/segmentation" element={<Segmentation />} />
            <Route path="/explainability" element={<Explainability />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </DataProvider>
  );
}

export default App;
