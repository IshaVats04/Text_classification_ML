import React, { useState } from 'react';
import { Send, Sparkles, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';

const TextInput = ({ onAnalyze, isLoading }) => {
  const [text, setText] = useState('');

  const sampleTexts = [
    "The acting was amazing but the story was boring and predictable.",
    "Absolutely fantastic movie! Great direction, outstanding performances, and beautiful music.",
    "Terrible film with poor acting and a confusing plot. Not recommended at all.",
    "The cinematography was stunning, but the pacing was too slow for my taste."
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      toast.error('Please enter some text to analyze');
      return;
    }

    if (text.length < 10) {
      toast.error('Please enter at least 10 characters for better analysis');
      return;
    }

    onAnalyze(text);
  };

  const handleSampleText = (sampleText) => {
    setText(sampleText);
    toast.success('Sample text loaded! Click Analyze to see results.');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="glass-morphism rounded-2xl p-6 shadow-xl">
        <div className="mb-4">
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            Enter Your Text
          </h2>
          <p className="text-gray-600">
            Type or paste your text below for comprehensive AI-powered analysis
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter your movie review, product feedback, or any text you'd like to analyze..."
              className="w-full h-40 p-4 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all duration-200 resize-none text-gray-700 placeholder-gray-400"
              disabled={isLoading}
            />
            <div className="absolute bottom-2 right-2 text-sm text-gray-500">
              {text.length} characters
            </div>
          </div>

          <div className="flex items-center justify-between">
            <button
              type="submit"
              disabled={isLoading || !text.trim()}
              className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-xl hover:from-primary-700 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>Analyze Text</span>
                </>
              )}
            </button>

            <button
              type="button"
              onClick={() => setText('')}
              disabled={isLoading}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors duration-200"
            >
              Clear
            </button>
          </div>
        </form>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center space-x-2 mb-3">
            <Sparkles className="w-4 h-4 text-primary-600" />
            <span className="text-sm font-medium text-gray-700">Try these examples:</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {sampleTexts.map((sample, index) => (
              <button
                key={index}
                onClick={() => handleSampleText(sample)}
                className="text-left p-3 text-sm bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200 text-gray-700 hover:text-gray-900"
              >
                "{sample.substring(0, 60)}..."
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextInput;
