import React from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Info, User, Upload as UploadIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useData } from '../context/DataContext';

const Explainability = () => {
    const navigate = useNavigate();
    const { explainabilityData, hasData, isProcessing } = useData();

    if (isProcessing) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="text-center space-y-4">
                    <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
                    <p className="text-gray-400">Processing your data...</p>
                </div>
            </div>
        );
    }

    if (!hasData || !explainabilityData) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="text-center space-y-6">
                    <div className="w-20 h-20 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500 mx-auto">
                        <UploadIcon size={40} />
                    </div>
                    <div className="space-y-2">
                        <h3 className="text-xl font-semibold text-white">No Data Available</h3>
                        <p className="text-gray-400 max-w-md">
                            Upload a CSV file to generate AI explanations and feature importance analysis.
                        </p>
                    </div>
                    <button
                        onClick={() => navigate('/upload')}
                        className="btn-gold"
                    >
                        Upload Data
                    </button>
                </div>
            </div>
        );
    }

    const data = explainabilityData;

    // Transform global importance for the chart
    // Backend returns list of objects: { feature: "name", importance: 0.123, ... }
    const chartData = (data.global_feature_importance || [])
        .map(item => ({
            name: item.feature,
            value: Math.abs(item.importance) * 100 // Convert to percentage and ensure positive
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 6);

    return (
        <div className="py-8 space-y-12">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold text-white">
                    Explainable <span className="text-amber-500">AI Insights</span>
                </h1>
                <p className="text-gray-400">Understand exactly why predictions are made with clear, actionable explanations.</p>
            </div>

            {/* Global Feature Importance Section */}
            <div className="space-y-6">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-panel p-8 border border-white/5 bg-[#0A0A0A]"
                >
                    <div className="flex items-start gap-4 mb-8">
                        <div className="p-2 bg-amber-500/10 rounded-lg text-amber-500">
                            <Info size={20} />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-white">Global Feature Importance</h3>
                            <p className="text-sm text-gray-500">These factors contribute most to churn risk predictions across all customers.</p>
                        </div>
                    </div>

                    {chartData.length > 0 ? (
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart
                                    layout="vertical"
                                    data={chartData}
                                    margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
                                >
                                    <XAxis type="number" hide />
                                    <YAxis
                                        type="category"
                                        dataKey="name"
                                        width={150}
                                        tick={{ fill: '#e5e5e5', fontSize: 13, fontWeight: 500 }}
                                        axisLine={false}
                                        tickLine={false}
                                    />
                                    <Tooltip
                                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                        content={({ active, payload }) => {
                                            if (active && payload && payload.length) {
                                                return (
                                                    <div className="bg-[#1a1a1a] border border-white/10 p-3 rounded-lg shadow-xl">
                                                        <p className="text-white font-bold mb-1">{payload[0].payload.name}</p>
                                                        <p className="text-sm text-gray-400">
                                                            Importance: <span className="text-amber-500">{payload[0].value.toFixed(1)}%</span>
                                                        </p>
                                                    </div>
                                                );
                                            }
                                            return null;
                                        }}
                                    />
                                    <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={36}>
                                        {chartData.map((entry, index) => (
                                            <Cell
                                                key={`cell-${index}`}
                                                fill={index < 2 ? '#FFAA00' : index < 4 ? '#A855F7' : '#64748B'}
                                            />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    ) : (
                        <div className="h-[300px] flex items-center justify-center text-gray-500">
                            <p>No feature importance data available</p>
                        </div>
                    )}
                </motion.div>

                {/* Detailed Definitions Grid */}
                {chartData.length > 0 && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {chartData.map((feature, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                className="glass-panel p-4 border border-white/5 bg-[#0A0A0A] flex flex-col justify-center"
                            >
                                <h4 className="font-bold text-white text-sm mb-1">{feature.name}</h4>
                                <p className="text-xs text-gray-500">
                                    Feature importance: {feature.value.toFixed(1)}%
                                </p>
                            </motion.div>
                        ))}
                    </div>
                )}
            </div>

            {/* Individual Explanations Section */}
            {data.individual_explanations && data.individual_explanations.length > 0 && (
                <div className="space-y-6">
                    <h2 className="text-2xl font-bold text-white">Individual Customer Explanations</h2>

                    <div className="space-y-4">
                        {data.individual_explanations.slice(0, 3).map((customer, index) => (
                            <motion.div
                                key={customer.customer_id || index}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.2 }}
                                className="glass-panel p-6 border border-white/5 bg-[#0A0A0A] relative overflow-hidden group"
                            >
                                {/* Card Glow */}
                                <div className={`absolute -left-1 top-0 bottom-0 w-1 ${customer.risk_level === 'High' ? 'bg-red-500' :
                                        customer.risk_level === 'Medium' ? 'bg-amber-500' : 'bg-emerald-500'
                                    }`} />

                                <div className="flex flex-col md:flex-row gap-6 items-start">
                                    {/* User Info */}
                                    <div className="flex items-center gap-4 min-w-[200px]">
                                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${customer.risk_level === 'High' ? 'bg-red-500/10 text-red-500' :
                                                customer.risk_level === 'Medium' ? 'bg-amber-500/10 text-amber-500' : 'bg-emerald-500/10 text-emerald-500'
                                            }`}>
                                            <User size={24} />
                                        </div>
                                        <div>
                                            <h3 className="text-lg font-bold text-white">
                                                {customer.customer_id || `Customer ${index + 1}`}
                                            </h3>
                                            <p className="text-sm text-gray-500">ID: {customer.customer_id}</p>
                                        </div>
                                        <div className={`px-3 py-1 rounded-full text-xs font-bold border ml-auto md:ml-4 ${customer.risk_level === 'High' ? 'bg-red-500/10 text-red-500 border-red-500/20' :
                                                customer.risk_level === 'Medium' ? 'bg-amber-500/10 text-amber-500 border-amber-500/20' :
                                                    'bg-emerald-500/10 text-emerald-500 border-emerald-500/20'
                                            }`}>
                                            {Math.round((customer.churn_probability || 0) * 100)}% risk
                                        </div>
                                    </div>

                                    {/* Factors & Summary */}
                                    <div className="flex-1 space-y-4">
                                        {customer.top_features && (
                                            <div>
                                                <p className="text-sm text-gray-400 mb-2">Top Contributing Features</p>
                                                <div className="flex flex-wrap gap-2">
                                                    {Object.entries(customer.top_features).slice(0, 3).map(([feature, value], i) => (
                                                        <span key={i} className={`px-3 py-1.5 rounded-lg text-xs font-medium border ${value > 0 ? 'bg-red-500/5 text-red-500 border-red-500/10' : 'bg-emerald-500/5 text-emerald-500 border-emerald-500/10'
                                                            }`}>
                                                            {feature}: {value > 0 ? '+' : ''}{value.toFixed(3)}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                        )}

                                        <div className="bg-white/5 rounded-xl p-4 border border-white/5">
                                            <p className="text-sm text-gray-300 leading-relaxed">
                                                {customer.explanation || `This customer has a ${customer.risk_level?.toLowerCase() || 'unknown'} risk level based on their feature profile.`}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>

                    {data.individual_explanations.length > 3 && (
                        <div className="text-center">
                            <p className="text-sm text-gray-500">
                                Showing 3 of {data.individual_explanations.length} customer explanations
                            </p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Explainability;