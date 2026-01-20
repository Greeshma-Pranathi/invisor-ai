import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart2, Users, BrainCircuit, MessageSquare, ArrowRight, Upload, CheckCircle, AlertTriangle, Activity, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';
import { useData } from '../context/DataContext';

const Dashboard = () => {
    const navigate = useNavigate();
    const { hasData, isDataReady, churnPredictions, segmentationData, explainabilityData, uploadedData } = useData();

    const features = [
        {
            icon: BarChart2,
            color: 'text-amber-500',
            bg: 'bg-amber-500/10',
            title: 'Churn Prediction',
            desc: 'Identify at-risk customers before they leave with AI-powered predictions.',
            path: '/churn',
            hasData: !!churnPredictions
        },
        {
            icon: Users,
            color: 'text-purple-500',
            bg: 'bg-purple-500/10',
            title: 'Smart Segmentation',
            desc: 'Automatically group customers by behavior patterns for targeted strategies.',
            path: '/segmentation',
            hasData: !!segmentationData
        },
        {
            icon: BrainCircuit,
            color: 'text-indigo-500',
            bg: 'bg-indigo-500/10',
            title: 'Explainable AI',
            desc: 'Understand exactly why predictions are made with clear, actionable insights.',
            path: '/explainability',
            hasData: !!explainabilityData
        },
        {
            icon: MessageSquare,
            color: 'text-pink-500',
            bg: 'bg-pink-500/10',
            title: 'AI Chatbot',
            desc: 'Ask questions about your data and get instant, intelligent answers.',
            path: '/chatbot',
            hasData: hasData
        }
    ];

    return (
        <div className="space-y-32 py-10">
            {/* Data Status Banner */}
            {hasData && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-panel p-4 border-green-500/20 bg-green-500/5 mb-8"
                >
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <CheckCircle className="text-green-500" size={20} />
                            <div>
                                <span className="text-green-500 font-medium">Data processed successfully!</span>
                                <p className="text-sm text-gray-400">
                                    {uploadedData?.rows} customers analyzed • {uploadedData?.columns} features processed
                                </p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={() => navigate('/upload')}
                                className="btn-outline text-sm"
                            >
                                Upload New Data
                            </button>
                        </div>
                    </div>
                </motion.div>
            )}

            {/* Quick Stats */}
            {isDataReady && churnPredictions && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16"
                >
                    <div className="glass-panel p-6 border-white/5 bg-[#0A0A0A]">
                        <div className="flex items-center gap-3 mb-2">
                            <Users className="text-white" size={20} />
                            <span className="text-sm text-gray-400">Total Customers</span>
                        </div>
                        <p className="text-2xl font-bold text-white">{churnPredictions.total_customers.toLocaleString()}</p>
                    </div>
                    
                    <div className="glass-panel p-6 border-red-500/20 bg-red-500/5">
                        <div className="flex items-center gap-3 mb-2">
                            <AlertTriangle className="text-red-500" size={20} />
                            <span className="text-sm text-gray-400">High Risk</span>
                        </div>
                        <p className="text-2xl font-bold text-red-500">{churnPredictions.high_risk_count}</p>
                    </div>
                    
                    <div className="glass-panel p-6 border-amber-500/20 bg-amber-500/5">
                        <div className="flex items-center gap-3 mb-2">
                            <Activity className="text-amber-500" size={20} />
                            <span className="text-sm text-gray-400">Medium Risk</span>
                        </div>
                        <p className="text-2xl font-bold text-amber-500">{churnPredictions.medium_risk_count}</p>
                    </div>
                    
                    <div className="glass-panel p-6 border-emerald-500/20 bg-emerald-500/5">
                        <div className="flex items-center gap-3 mb-2">
                            <TrendingUp className="text-emerald-500" size={20} />
                            <span className="text-sm text-gray-400">Low Risk</span>
                        </div>
                        <p className="text-2xl font-bold text-emerald-500">{churnPredictions.low_risk_count}</p>
                    </div>
                </motion.div>
            )}

            {/* Hero Section */}
            <section className="text-center relative">
                {/* Glow effect */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-amber-500/10 blur-[120px] rounded-full pointer-events-none" />

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="relative z-10"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8 backdrop-blur-sm">
                        <span className="flex h-2 w-2 rounded-full bg-amber-500 animate-pulse"></span>
                        <span className="text-sm font-medium text-amber-500">AI-Powered Customer Intelligence</span>
                    </div>

                    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight tracking-tight">
                        <span className="text-white">Explainable AI for</span>
                        <br />
                        <span className="text-gradient-gold">Customer Insights</span>
                    </h1>

                    <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
                        {hasData 
                            ? "Your data has been processed! Explore the insights below or dive into detailed analysis."
                            : "Upload your customer data and instantly understand churn risk, customer segments, and the reasons behind them. Make data-driven decisions with confidence."
                        }
                    </p>

                    <div className="flex flex-col sm:flex-row justify-center gap-4">
                        {!hasData ? (
                            <>
                                <button
                                    onClick={() => navigate('/upload')}
                                    className="btn-gold group relative overflow-hidden"
                                >
                                    <span className="relative z-10 flex items-center gap-2">
                                        Upload CSV
                                        <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                                    </span>
                                    <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                                </button>

                                <button
                                    onClick={() => navigate('/upload')}
                                    className="btn-ghost group"
                                >
                                    View Demo Flow
                                </button>
                            </>
                        ) : (
                            <>
                                <button
                                    onClick={() => navigate('/churn')}
                                    className="btn-gold group relative overflow-hidden"
                                >
                                    <span className="relative z-10 flex items-center gap-2">
                                        View Analysis
                                        <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                                    </span>
                                    <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                                </button>

                                <button
                                    onClick={() => navigate('/upload')}
                                    className="btn-ghost group"
                                >
                                    Upload New Data
                                </button>
                            </>
                        )}
                    </div>
                </motion.div>
            </section>

            {/* Features Section */}
            <section>
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-4xl font-bold mb-4">
                        {hasData ? "Your " : "Everything you need to "}
                        <span className="text-gradient-purple">
                            {hasData ? "Analysis Results" : "understand your customers"}
                        </span>
                    </h2>
                    <p className="text-gray-400">
                        {hasData 
                            ? "Click on any section below to explore your processed data in detail."
                            : "Powerful AI tools that transform raw data into actionable intelligence."
                        }
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {features.map((feature, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: idx * 0.1 }}
                            className={`feature-card group cursor-pointer relative ${
                                hasData && feature.hasData ? 'border-green-500/20 bg-green-500/5' : ''
                            }`}
                            onClick={() => navigate(feature.path)}
                        >
                            {hasData && feature.hasData && (
                                <div className="absolute top-4 right-4">
                                    <CheckCircle className="text-green-500" size={16} />
                                </div>
                            )}
                            
                            <div className={`w-12 h-12 rounded-lg ${feature.bg} ${feature.color} flex items-center justify-center mb-6`}>
                                <feature.icon size={24} />
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-amber-500 transition-colors">
                                {feature.title}
                            </h3>
                            <p className="text-gray-400 leading-relaxed">
                                {feature.desc}
                            </p>

                            {hasData && feature.hasData && (
                                <div className="mt-4 text-sm text-green-500 font-medium">
                                    ✓ Data processed - Click to view
                                </div>
                            )}

                            <div className="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-4 group-hover:translate-x-0">
                                <ArrowRight className="text-white/20" />
                            </div>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            {!hasData && (
                <section className="relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-amber-500/10 to-purple-500/10 blur-3xl opacity-30" />
                    <div className="feature-card text-center py-16 border-amber-500/20 bg-gradient-to-b from-white/5 to-transparent">
                        <h2 className="text-3xl font-bold mb-4">Ready to unlock customer insights?</h2>
                        <p className="text-gray-400 mb-8 max-w-xl mx-auto">
                            Start with your own data or explore our demo to see the power of explainable AI.
                        </p>
                        <button
                            onClick={() => navigate('/upload')}
                            className="btn-gold mx-auto"
                        >
                            Get Started Now <ArrowRight size={18} />
                        </button>
                    </div>
                </section>
            )}
        </div>
    );
};

export default Dashboard;
