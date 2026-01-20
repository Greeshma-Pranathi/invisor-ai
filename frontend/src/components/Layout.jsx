import React from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from './Navbar';
import { motion, AnimatePresence } from 'framer-motion';

const Layout = ({ children }) => {
    const location = useLocation();

    return (
        <div className="min-h-screen flex flex-col bg-[#050505]">
            <Navbar />

            {/* Add padding-top to account for fixed navbar */}
            <main className="flex-1 pt-24 pb-12 px-6">
                <div className="container-width">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={location.pathname}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3 }}
                        >
                            {children}
                        </motion.div>
                    </AnimatePresence>
                </div>
            </main>

            {/* Simple Footer */}
            <footer className="border-t border-white/5 py-8 mt-auto">
                <div className="container-width text-center text-gray-500 text-sm">
                    <p>© 2026 Invisor.ai. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
