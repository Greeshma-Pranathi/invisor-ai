import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle, X, ArrowRight, Users, BarChart3, Brain } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useData } from '../context/DataContext';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [dragActive, setDragActive] = useState(false);
    const [localError, setLocalError] = useState('');
    const fileInputRef = useRef(null);
    const navigate = useNavigate();
    
    const { uploadCSV, isProcessing, processingStep, hasData, clearData, error } = useData();

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            validateAndSetFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            validateAndSetFile(e.target.files[0]);
        }
    };

    const validateAndSetFile = (selectedFile) => {
        if (selectedFile.type !== 'text/csv' && !selectedFile.name.endsWith('.csv')) {
            setLocalError('Please upload a valid CSV file.');
            return;
        }
        setFile(selectedFile);
        setLocalError('');
    };

    const handleUpload = async () => {
        if (!file) return;

        const result = await uploadCSV(file);
        
        if (result.success) {
            // Auto-navigate to dashboard after successful processing
            setTimeout(() => {
                navigate('/');
            }, 2000);
        } else {
            setLocalError(result.error || 'Upload failed. Please try again.');
        }
    };

    const processingSteps = [
        { step: 'Uploading file...', icon: UploadIcon, path: '/upload' },
        { step: 'Generating churn predictions...', icon: Users, path: '/churn' },
        { step: 'Creating customer segments...', icon: BarChart3, path: '/segmentation' },
        { step: 'Generating explanations...', icon: Brain, path: '/explainability' },
        { step: 'Complete!', icon: CheckCircle, path: '/' }
    ];

    const currentStepIndex = processingSteps.findIndex(s => s.step === processingStep);

    return (
        <div className="max-w-4xl mx-auto py-10 space-y-8">
            <div className="text-center space-y-4">
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    Upload Your <span className="text-amber-500">Customer Data</span>
                </h1>
                <p className="text-gray-400 max-w-2xl mx-auto text-lg">
                    Upload a CSV file with customer data to start your analysis.
                    We'll automatically process it to generate churn predictions, segments, and explanations.
                </p>
            </div>

            {/* Processing Pipeline Visualization */}
            {isProcessing && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-panel p-6 space-y-4"
                >
                    <h3 className="text-lg font-semibold text-white mb-4">Processing Your Data</h3>
                    <div className="space-y-3">
                        {processingSteps.map((step, index) => {
                            const isActive = index === currentStepIndex;
                            const isCompleted = index < currentStepIndex;
                            const Icon = step.icon;
                            
                            return (
                                <div key={index} className={`flex items-center gap-3 p-3 rounded-lg transition-all ${
                                    isActive ? 'bg-amber-500/10 border border-amber-500/20' : 
                                    isCompleted ? 'bg-green-500/10' : 'bg-white/5'
                                }`}>
                                    <div className={`p-2 rounded-lg ${
                                        isActive ? 'bg-amber-500/20 text-amber-500' :
                                        isCompleted ? 'bg-green-500/20 text-green-500' : 'bg-white/10 text-gray-400'
                                    }`}>
                                        <Icon size={16} />
                                    </div>
                                    <span className={`flex-1 ${
                                        isActive ? 'text-amber-500' :
                                        isCompleted ? 'text-green-500' : 'text-gray-400'
                                    }`}>
                                        {step.step}
                                    </span>
                                    {isActive && (
                                        <div className="w-4 h-4 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
                                    )}
                                    {isCompleted && (
                                        <CheckCircle size={16} className="text-green-500" />
                                    )}
                                </div>
                            );
                        })}
                    </div>
                    
                    {processingStep === 'Complete!' && (
                        <div className="mt-4 p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                            <div className="flex items-center justify-between">
                                <span className="text-green-500 font-medium">Processing complete! Redirecting to dashboard...</span>
                                <button
                                    onClick={() => navigate('/')}
                                    className="btn-gold text-sm"
                                >
                                    View Results <ArrowRight size={16} />
                                </button>
                            </div>
                        </div>
                    )}
                </motion.div>
            )}

            {/* Upload Area */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-panel p-1 rounded-2xl relative overflow-hidden"
            >
                <div
                    className={`
                        relative rounded-xl border-2 border-dashed transition-all duration-300 p-16 text-center
                        ${dragActive
                            ? 'border-amber-500 bg-amber-500/5'
                            : 'border-white/10 hover:border-white/20 bg-[#0A0A0A]'}
                        ${isProcessing ? 'opacity-50 pointer-events-none' : ''}
                    `}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".csv"
                        onChange={handleChange}
                        className="hidden"
                        disabled={isProcessing}
                    />

                    <AnimatePresence mode="wait">
                        {!file ? (
                            <motion.div
                                key="empty"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="flex flex-col items-center gap-6"
                            >
                                <div className="w-20 h-20 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500 mb-2">
                                    <UploadIcon size={40} />
                                </div>
                                <div className="space-y-2">
                                    <h3 className="text-xl font-semibold text-white">
                                        Drag and drop your CSV file here
                                    </h3>
                                    <p className="text-gray-500">
                                        or <button 
                                            onClick={() => fileInputRef.current?.click()} 
                                            className="text-amber-500 hover:text-amber-400 font-medium transition-colors"
                                            disabled={isProcessing}
                                        >
                                            click to browse
                                        </button>
                                    </p>
                                </div>
                            </motion.div>
                        ) : (
                            <motion.div
                                key="selected"
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0 }}
                                className="flex flex-col items-center gap-6"
                            >
                                <div className="w-20 h-20 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-500 mb-2">
                                    <FileText size={40} />
                                </div>
                                <div className="space-y-1">
                                    <h3 className="text-xl font-medium text-white break-all max-w-md">
                                        {file.name}
                                    </h3>
                                    <p className="text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
                                </div>

                                <div className="flex gap-4 mt-2">
                                    <button
                                        onClick={handleUpload}
                                        disabled={isProcessing}
                                        className="btn-gold min-w-[140px]"
                                    >
                                        {isProcessing ? (
                                            <span className="flex items-center gap-2">
                                                <span className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                                                Processing...
                                            </span>
                                        ) : 'Start Analysis'}
                                    </button>
                                    <button
                                        onClick={() => { setFile(null); setLocalError(''); }}
                                        disabled={isProcessing}
                                        className="p-3 rounded-xl bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white transition-colors disabled:opacity-50"
                                    >
                                        <X size={20} />
                                    </button>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Error Message */}
                    {(localError || error) && (
                        <div className="mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium bg-red-500/10 text-red-500">
                            <AlertCircle size={16} />
                            {localError || error}
                        </div>
                    )}
                </div>
            </motion.div>

            {/* Previous Data Notice */}
            {hasData && !isProcessing && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-panel p-4 border-blue-500/20 bg-blue-500/5"
                >
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <CheckCircle className="text-blue-500" size={20} />
                            <span className="text-blue-500 font-medium">You have processed data available</span>
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={() => navigate('/')}
                                className="btn-secondary text-sm"
                            >
                                View Results
                            </button>
                            <button
                                onClick={clearData}
                                className="btn-outline text-sm"
                            >
                                Clear Data
                            </button>
                        </div>
                    </div>
                </motion.div>
            )}

            {/* Quick Navigation */}
            {hasData && !isProcessing && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="grid grid-cols-2 md:grid-cols-4 gap-4"
                >
                    {[
                        { name: 'Dashboard', path: '/', icon: BarChart3, desc: 'Overview' },
                        { name: 'Churn Analysis', path: '/churn', icon: Users, desc: 'Risk Assessment' },
                        { name: 'Segmentation', path: '/segmentation', icon: BarChart3, desc: 'Customer Groups' },
                        { name: 'Explainability', path: '/explainability', icon: Brain, desc: 'AI Insights' }
                    ].map((item) => {
                        const Icon = item.icon;
                        return (
                            <button
                                key={item.path}
                                onClick={() => navigate(item.path)}
                                className="glass-panel p-4 hover:bg-white/10 transition-colors text-left group"
                            >
                                <div className="flex items-center gap-3 mb-2">
                                    <Icon size={20} className="text-amber-500" />
                                    <span className="font-medium text-white group-hover:text-amber-500 transition-colors">
                                        {item.name}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-400">{item.desc}</p>
                            </button>
                        );
                    })}
                </motion.div>
            )}

            {/* Format Requirements */}
            <div className="glass-panel p-6 border-white/5 bg-white/[0.02]">
                <div className="flex items-start gap-4">
                    <FileText className="text-gray-600 mt-1 shrink-0" />
                    <div>
                        <h4 className="text-white font-medium mb-1">CSV Format Requirements</h4>
                        <p className="text-sm text-gray-500 leading-relaxed">
                            Your CSV should include customer attributes like demographics (Age, Gender, Location),
                            transaction history (Tenure, Balance, NumProducts), and engagement metrics.
                            We'll automatically handle missing values and feature engineering.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Upload;