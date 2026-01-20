import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Upload as UploadIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';
import { motion, AnimatePresence } from 'framer-motion';
import { useData } from '../context/DataContext';

const Chatbot = () => {
    const navigate = useNavigate();
    const { hasData } = useData();
    
    const [messages, setMessages] = useState([
        {
            type: 'bot',
            content: hasData 
                ? "Hello! I'm your AI insights assistant. I can see you have processed customer data. Ask me questions about your churn predictions, customer segments, or any insights from your analysis. What would you like to know?"
                : "Hello! I'm your AI insights assistant. I can help you understand customer data, churn predictions, and segmentation analysis. Please upload your CSV data first, then I'll be able to answer specific questions about your customers."
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (text = input) => {
        if (!text.trim()) return;

        setMessages(prev => [...prev, { type: 'user', content: text }]);
        setInput('');
        setIsLoading(true);

        try {
            if (!hasData) {
                setMessages(prev => [...prev, { 
                    type: 'bot', 
                    content: "I'd love to help, but I need you to upload your customer data first. Once you upload a CSV file, I'll be able to answer specific questions about your customers, churn predictions, and segments. Would you like to upload data now?" 
                }]);
                setIsLoading(false);
                return;
            }

            const response = await client.post('/chatbot/query', { query: text });
            setMessages(prev => [...prev, { type: 'bot', content: response.data.response }]);
        } catch (error) {
            console.error("Chat error:", error);
            setMessages(prev => [...prev, { type: 'bot', content: "I'm having trouble connecting to the insights engine right now. Please try again." }]);
        } finally {
            setIsLoading(false);
        }
    };

    if (!hasData) {
        return (
            <div className="max-w-4xl mx-auto py-8 flex items-center justify-center min-h-[60vh]">
                <div className="text-center space-y-6">
                    <div className="w-20 h-20 rounded-2xl bg-purple-500/10 flex items-center justify-center text-purple-500 mx-auto">
                        <UploadIcon size={40} />
                    </div>
                    <div className="space-y-2">
                        <h3 className="text-xl font-semibold text-white">No Data Available</h3>
                        <p className="text-gray-400 max-w-md">
                            Upload a CSV file to start chatting with your AI assistant about customer insights.
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

    const suggestions = hasData ? [
        "Which segment has highest churn risk?",
        "What features influence churn most?",
        "How many customers are at high risk?",
        "Summarize the customer insights"
    ] : [
        "How does churn prediction work?",
        "What is customer segmentation?",
        "Tell me about explainable AI",
        "What data do I need to upload?"
    ];

    return (
        <div className="max-w-4xl mx-auto py-8 flex flex-col h-[calc(100vh-8rem)]">
            <div className="mb-6 space-y-2">
                <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                    <Bot className="text-purple-500" size={32} />
                    AI <span className="text-purple-500">Insights Chatbot</span>
                </h1>
                <p className="text-gray-400">Ask questions about your data and get instant, intelligent answers.</p>
            </div>

            {/* Chat Container */}
            <div className="flex-1 rounded-3xl bg-[#050505] border border-purple-500/20 relative flex flex-col overflow-hidden shadow-[0_0_50px_rgba(168,85,247,0.05)]">

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-purple-900/20">
                    {messages.map((msg, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex gap-4 ${msg.type === 'user' ? 'flex-row-reverse' : ''}`}
                        >
                            <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 
                    ${msg.type === 'bot' ? 'bg-purple-500/10 text-purple-500' : 'bg-gray-700/50 text-gray-300'}`}>
                                {msg.type === 'bot' ? <Bot size={20} /> : <User size={20} />}
                            </div>

                            <div className={`max-w-[80%] rounded-2xl p-4 text-sm leading-relaxed
                    ${msg.type === 'user'
                                    ? 'bg-purple-600 text-white rounded-tr-none'
                                    : 'bg-white/5 border border-white/5 text-gray-200 rounded-tl-none'
                                }
                `}>
                                {msg.content}
                            </div>
                        </motion.div>
                    ))}

                    {isLoading && (
                        <div className="flex gap-4">
                            <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center shrink-0 text-purple-500">
                                <Bot size={20} />
                            </div>
                            <div className="bg-white/5 border border-white/5 rounded-2xl rounded-tl-none p-4 flex items-center gap-2">
                                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" />
                                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce delay-100" />
                                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce delay-200" />
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-[#0A0A0A] border-t border-white/5 space-y-4">
                    {/* Suggestions Chips */}
                    <div className="flex flex-wrap gap-2">
                        {suggestions.map((q) => (
                            <button
                                key={q}
                                onClick={() => handleSend(q)}
                                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 text-xs text-gray-400 hover:text-white transition-all"
                            >
                                <Sparkles size={12} className="text-purple-500" />
                                {q}
                            </button>
                        ))}
                    </div>

                    <div className="relative">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask about churn, segments, or insights..."
                            className="w-full bg-[#151515] border border-white/10 rounded-xl py-4 pl-5 pr-14 text-white placeholder-gray-600 focus:outline-none focus:border-purple-500/50 transition-all"
                        />
                        <button
                            onClick={() => handleSend()}
                            disabled={!input.trim() || isLoading}
                            className="absolute right-2 top-2 p-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send size={18} />
                        </button>
                    </div>

                    <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-transparent via-purple-500/20 to-transparent pointer-events-none" />
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
