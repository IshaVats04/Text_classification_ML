import React from 'react';
import { Brain, FileText, BarChart3 } from 'lucide-react';

const Header = ({ currentView, setCurrentView }) => {
  return (
    <header className="glass-morphism sticky top-0 z-50 border-b border-white/20">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">TextAI Classifier</h1>
              <p className="text-sm text-gray-600">Advanced NLP Analysis</p>
            </div>
          </div>

          <nav className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentView('single')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                currentView === 'single'
                  ? 'bg-primary-600 text-white shadow-lg'
                  : 'bg-white/50 text-gray-700 hover:bg-white/70'
              }`}
            >
              <FileText className="w-4 h-4" />
              <span className="hidden sm:inline">Single Analysis</span>
            </button>
            
            <button
              onClick={() => setCurrentView('batch')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                currentView === 'batch'
                  ? 'bg-primary-600 text-white shadow-lg'
                  : 'bg-white/50 text-gray-700 hover:bg-white/70'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span className="hidden sm:inline">Batch Analysis</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
