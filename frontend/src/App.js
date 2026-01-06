import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import Header from './components/Header';
import TextInput from './components/TextInput';
import ResultsDisplay from './components/ResultsDisplay';
import BatchAnalysis from './components/BatchAnalysis';
import FeatureShowcase from './components/FeatureShowcase';
import { analyzeText } from './services/api';
import { motion } from 'framer-motion';

function App() {
  const [currentView, setCurrentView] = useState('single');
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleTextAnalysis = async (text) => {
    setIsLoading(true);
    try {
      const results = await analyzeText(text);
      setAnalysisResults(results);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Header currentView={currentView} setCurrentView={setCurrentView} />
      
      <main className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-8"
        >
          {currentView === 'single' ? (
            <>
              <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Advanced Text Classification AI
                </h1>
                <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                  Experience cutting-edge NLP with multi-label classification, aspect-wise sentiment analysis, 
                  emotion detection, and intelligent keyword extraction.
                </p>
              </div>

              <TextInput 
                onAnalyze={handleTextAnalysis} 
                isLoading={isLoading}
              />

              {analysisResults && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <ResultsDisplay results={analysisResults} />
                </motion.div>
              )}
            </>
          ) : (
            <BatchAnalysis />
          )}

          <FeatureShowcase />
        </motion.div>
      </main>

      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
}

export default App;
