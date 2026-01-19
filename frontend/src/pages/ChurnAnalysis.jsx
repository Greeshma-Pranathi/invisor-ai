import React from 'react';
import { motion } from 'framer-motion';
import { Users, AlertTriangle, Activity, TrendingUp, Upload as UploadIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useData } from '../context/DataContext';

const ChurnAnalysis = () => {
    const navigate = useNavigate();
    const { churnPredictions, hasData, isProcessing } = useData();

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

    if (!hasData || !churnPredictions) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="text-center space-y-6">
                    <div className="w-20 h-20 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500 mx-auto">
                        <UploadIcon size={40} />
                    </div>
                    <div className="space-y-2">
                        <h3 className="text-xl font-semibold text-white">No Data Available</h3>
                        <p className="text-gray-400 max-w-md">
                            Upload a CSV file to generate churn predictions and risk analysis.
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

    const data = churnPredictions;

    return (
        <div className="py-8 space-y-8">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold text-white">
                    Churn <span className="text-amber-500">Prediction</span>
                </h1>
                <p className="text-gray-400">Identify customers at risk of leaving and take proactive action.</p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Total Customers"
                    value={data.total_customers.toLocaleString()}
                    icon={Users}
                    color="text-white"
                    bg="bg-white/5"
                    borderColor="border-white/5"
                />
                <KPICard
                    title="High Risk"
                    value={data.high_risk_count.toLocaleString()}
                    icon={AlertTriangle}
                    color="text-red-500"
                    bg="bg-red-500/10"
                    borderColor="border-red-500/20"
                />
                <KPICard
                    title="Medium Risk"
                    value={data.medium_risk_count.toLocaleString()}
                    icon={Activity}
                    color="text-amber-500"
                    bg="bg-amber-500/10"
                    borderColor="border-amber-500/20"
                />
                <KPICard
                    title="Low Risk"
                    value={data.low_risk_count.toLocaleString()}
                    icon={TrendingUp}
                    color="text-emerald-500"
                    bg="bg-emerald-500/10"
                    borderColor="border-emerald-500/20"
                />
            </div>

            {/* Customer Risk Table */}
            <div className="glass-panel p-6 border border-white/5 bg-[#0A0A0A]">
                <div className="flex items-center justify-between mb-8">
                    <h2 className="text-xl font-bold text-white">Customer Churn Risk</h2>
                    <span className="text-sm text-gray-500">
                        Showing {Math.min(data.predictions?.length || 0, 10)} of {data.total_customers} customers
                    </span>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-white/5 text-left text-sm text-gray-500">
                                <th className="pb-4 font-medium pl-4">Customer ID</th>
                                <th className="pb-4 font-medium">Churn Probability</th>
                                <th className="pb-4 font-medium pr-4 text-right">Risk Level</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {(data.predictions || []).slice(0, 10).map((customer, index) => (
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
                                    <td className="py-4 w-1/2">
                                        <div className="flex items-center gap-4">
                                            <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full rounded-full transition-all duration-1000 ${
                                                        customer.risk_level === 'High' ? 'bg-red-500' :
                                                        customer.risk_level === 'Medium' ? 'bg-amber-500' : 'bg-emerald-500'
                                                    }`}
                                                    style={{ 
                                                        width: `${Math.round((customer.churn_probability || 0) * 100)}%` 
                                                    }}
                                                />
                                            </div>
                                            <span className="text-sm text-gray-400 w-12">
                                                {Math.round((customer.churn_probability || 0) * 100)}%
                                            </span>
                                        </div>
                                    </td>
                                    <td className="py-4 pr-4 text-right">
                                        <span className={`
                                            inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border
                                            ${customer.risk_level === 'High'
                                                ? 'bg-red-500/10 text-red-500 border-red-500/20'
                                                : customer.risk_level === 'Medium'
                                                    ? 'bg-amber-500/10 text-amber-500 border-amber-500/20'
                                                    : 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20'}
                                        `}>
                                            {customer.risk_level}
                                        </span>
                                    </td>
                                </motion.tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {data.predictions && data.predictions.length > 10 && (
                    <div className="mt-4 text-center">
                        <p className="text-sm text-gray-500">
                            Showing first 10 customers. Total: {data.predictions.length}
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

const KPICard = ({ title, value, icon: Icon, color, bg, borderColor }) => (
    <div className={`p-6 rounded-2xl bg-[#0A0A0A] border ${borderColor} relative overflow-hidden group`}>
        <div className="flex justify-between items-start mb-4">
            <div>
                <p className="text-gray-500 text-sm font-medium mb-1">{title}</p>
                <h3 className="text-3xl font-bold text-white">{value}</h3>
            </div>
            <div className={`p-3 rounded-xl ${bg} ${color}`}>
                <Icon size={20} />
            </div>
        </div>
        {/* Glow effect on hover */}
        <div className={`absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-500 pointer-events-none ${color.replace('text-', 'bg-')}`} />
    </div>
);

export default ChurnAnalysis;