import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import client from '../api/client';

const DataContext = createContext();

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

export const DataProvider = ({ children }) => {
  const [uploadedData, setUploadedData] = useState(null);
  const [churnPredictions, setChurnPredictions] = useState(null);
  const [segmentationData, setSegmentationData] = useState(null);
  const [explainabilityData, setExplainabilityData] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStep, setProcessingStep] = useState('');
  const [error, setError] = useState(null);

  // Load data from localStorage on mount
  useEffect(() => {
    const savedData = localStorage.getItem('invisor-data');
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData);
        setUploadedData(parsed.uploadedData);
        setChurnPredictions(parsed.churnPredictions);
        setSegmentationData(parsed.segmentationData);
        setExplainabilityData(parsed.explainabilityData);
      } catch (error) {
        console.error('Failed to load saved data:', error);
        localStorage.removeItem('invisor-data');
      }
    }
  }, []);

  // Save data to localStorage whenever it changes
  useEffect(() => {
    if (uploadedData || churnPredictions || segmentationData || explainabilityData) {
      const dataToSave = {
        uploadedData,
        churnPredictions,
        segmentationData,
        explainabilityData,
        timestamp: Date.now()
      };
      localStorage.setItem('invisor-data', JSON.stringify(dataToSave));
    }
  }, [uploadedData, churnPredictions, segmentationData, explainabilityData]);

  const uploadCSV = useCallback(async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    setIsProcessing(true);
    setProcessingStep('Uploading file...');
    setError(null);
    
    try {
      // Upload CSV
      const uploadResponse = await client.post('/upload-csv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setUploadedData(uploadResponse.data);
      setProcessingStep('Generating churn predictions...');
      
      // Auto-trigger churn predictions
      const churnResponse = await client.post('/predict-churn');
      setChurnPredictions(churnResponse.data);
      setProcessingStep('Creating customer segments...');
      
      // Auto-trigger segmentation
      const segmentResponse = await client.post('/customer-segmentation');
      setSegmentationData(segmentResponse.data);
      setProcessingStep('Generating explanations...');
      
      // Auto-trigger explainability
      const explainResponse = await client.post('/explainability');
      setExplainabilityData(explainResponse.data);
      
      setProcessingStep('Complete!');
      return { success: true, data: uploadResponse.data };
      
    } catch (error) {
      console.error('Processing failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Processing failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsProcessing(false);
      setTimeout(() => setProcessingStep(''), 2000);
    }
  }, []);

  const clearData = useCallback(() => {
    setUploadedData(null);
    setChurnPredictions(null);
    setSegmentationData(null);
    setExplainabilityData(null);
    setIsProcessing(false);
    setProcessingStep('');
    setError(null);
    localStorage.removeItem('invisor-data');
  }, []);

  const refreshData = useCallback(async () => {
    if (!uploadedData) return;
    
    setIsProcessing(true);
    setError(null);
    
    try {
      setProcessingStep('Refreshing predictions...');
      const churnResponse = await client.post('/predict-churn');
      setChurnPredictions(churnResponse.data);
      
      setProcessingStep('Refreshing segments...');
      const segmentResponse = await client.post('/customer-segmentation');
      setSegmentationData(segmentResponse.data);
      
      setProcessingStep('Refreshing explanations...');
      const explainResponse = await client.post('/explainability');
      setExplainabilityData(explainResponse.data);
      
      setProcessingStep('Refresh complete!');
      return { success: true };
      
    } catch (error) {
      console.error('Refresh failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Refresh failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsProcessing(false);
      setTimeout(() => setProcessingStep(''), 2000);
    }
  }, [uploadedData]);

  const value = {
    // Data states
    uploadedData,
    churnPredictions,
    segmentationData,
    explainabilityData,
    
    // Processing states
    isProcessing,
    processingStep,
    error,
    
    // Actions
    uploadCSV,
    clearData,
    refreshData,
    
    // Computed states
    hasData: !!uploadedData,
    isDataReady: !!(uploadedData && churnPredictions && segmentationData && explainabilityData),
    
    // Data counts for navigation
    totalCustomers: uploadedData?.rows || 0,
    highRiskCount: churnPredictions?.high_risk_count || 0,
    mediumRiskCount: churnPredictions?.medium_risk_count || 0,
    lowRiskCount: churnPredictions?.low_risk_count || 0
  };

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};