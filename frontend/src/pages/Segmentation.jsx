import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Upload as UploadIcon, Users, Activity, TrendingUp, AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useData } from '../context/DataContext';

const Segmentation = () => {
    const navigate = useNavigate();
    const { segmentationData, hasData, isProcessing } = useData();

    const COLORS = {
        'High Value': '#F59E0B',       // Amber
        'At Risk': '#EF4444',          // Red
        'New Customer': '#14B8A6',     // Teal
        'Loyal': '#10B981',            // Emerald
        'Price Sensitive': '#A855F7'   // Purple
    };

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

    if (!hasData || !segmentationData) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="text-center space-y-6">
                    <div className="w-20 h-20 rounded-2xl bg-purple-500/10 flex items-center justify-center text-purple-500 mx-auto">
                        <UploadIcon size={40} />
                    </div>
                    <div className="space-y-2">
                        <h3 className="text-xl font-semibold text-white">No Data Available</h3>
                        <p className="text-gray-400 max-w-md">
                            Upload a CSV file to generate customer segments and behavioral analysis.
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

    const data = segmentationData;

    // Transform backend summary for the chart
    const chartData = Object.entries(data.segment_summary || {}).map(([name, info]) => ({
        name,
        value: info.count || info,
        percentage: info.percentage || 0,
        color: COLORS[name] || '#CBD5E1'
    }));

    return (
        <div className="py-8 space-y-8">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold text-white">
                    Customer <span className="text-purple-500">Segmentation</span>
                </h1>
                <p className="text-gray-400">Segments group customers with similar behavior patterns for targeted strategies.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Chart Section */}
                <div className="glass-panel p-8 lg:col-span-1 bg-[#0A0A0A] border-white/5 flex flex-col items-center justify-center relative min-h-[400px]">
                    <h3 className="text-lg font-bold text-white absolute top-6 left-6">Segment Distribution</h3>
                    <div className="absolute top-20 left-6 bg-white/5 border border-white/5 px-3 py-2 rounded-lg text-xs text-gray-400">
                        Count: {data.total_customers} customers
                    </div>

                    <div className="w-full h-[250px] mt-8">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={chartData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    paddingAngle={2}
                                    dataKey="value"
                                    stroke="none"
                                >
                                    {chartData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#000', borderColor: '#333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Legend */}
                    <div className="flex flex-wrap justify-center gap-3 mt-4">
                        {chartData.map((item) => (
                            <div key={item.name} className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: item.color }} />
                                <span className="text-[10px] text-gray-400 uppercase tracking-wider">{item.name}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Legend / Details List */}
                <div className="lg:col-span-2 space-y-4">
                    <h3 className="text-lg font-bold text-white mb-6">Segment Details</h3>
                    <div className="space-y-3">
                        {chartData.map((segment, index) => (
                            <motion.div 
                                key={segment.name}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="glass-panel p-5 border border-white/5 bg-[#0A0A0A] flex items-center justify-between group hover:border-white/10 transition-all"
                            >
                                <div className="flex items-start gap-4">
                                    <div className="w-3 h-3 rounded-full mt-1.5" style={{ backgroundColor: segment.color }} />
                                    <div>
                                        <h4 className="font-bold text-white">{segment.name}</h4>
                                        <p className="text-sm text-gray-500">
                                            {segment.name === 'High Value' && 'High value customers with strong engagement'}
                                            {segment.name === 'At Risk' && 'Declining activity, needs attention'}
                                            {segment.name === 'New Customer' && 'Recently acquired, building habits'}
                                            {segment.name === 'Loyal' && 'Consistent engagement and loyalty'}
                                            {segment.name === 'Price Sensitive' && 'Cost-conscious customers'}
                                        </p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <span className="text-gray-400 font-mono text-lg">{segment.value}</span>
                                    {segment.percentage > 0 && (
                                        <p className="text-xs text-gray-500">{segment.percentage}%</p>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Customer List Table */}
            {data.segments && data.segments.length > 0 && (
                <div className="glass-panel p-6 border border-white/5 bg-[#0A0A0A]">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-xl font-bold text-white">Customer Segments</h2>
                        <span className="text-sm text-gray-500">
                            Showing {Math.min(data.segments.length, 10)} of {data.total_customers} customers
                        </span>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-white/5 text-left text-sm text-gray-500">
                                    <th className="pb-4 font-medium pl-4">Customer ID</th>
                                    <th className="pb-4 font-medium">Segment</th>
                                    <th className="pb-4 font-medium pr-4">Confidence</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {data.segments.slice(0, 10).map((customer, index) => (
                                    <motion.tr 
                                        key={customer.customer_id || index}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.05 }}
                                        className="group hover:bg-white/[0.02] transition-colors"
                                    >
                                        <td className="py-4 pl-4 font-mono text-sm text-gray-300">
                                            {customer.customer_id || `CUS-${String(index + 1).padStart(3, '0')}`}
                                        </td>
                                        <td className="py-4">
                                            <span 
                                                className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border border-white/5 bg-opacity-10" 
                                                style={{ color: COLORS[customer.segment_name] || '#CBD5E1' }}
                                            >
                                                <span 
                                                    className="w-1.5 h-1.5 rounded-full" 
                                                    style={{ backgroundColor: COLORS[customer.segment_name] || '#CBD5E1' }}
                                                />
                                                {customer.segment_name}
                                            </span>
                                        </td>
                                        <td className="py-4 pr-4">
                                            <div className="flex items-center gap-4 w-32">
                                                <div className="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden">
                                                    <div
                                                        className="h-full rounded-full transition-all duration-1000"
                                                        style={{ 
                                                            width: `${Math.round((customer.confidence || 0.8) * 100)}%`, 
                                                            backgroundColor: COLORS[customer.segment_name] || '#CBD5E1' 
                                                        }}
                                                    />
                                                </div>
                                                <span className="text-sm font-bold text-white w-8">
                                                    {Math.round((customer.confidence || 0.8) * 100)}
                                                </span>
                                            </div>
                                        </td>
                                    </motion.tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {data.segments.length > 10 && (
                        <div className="mt-4 text-center">
                            <p className="text-sm text-gray-500">
                                Showing first 10 customers. Total: {data.segments.length}
                            </p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Segmentation;