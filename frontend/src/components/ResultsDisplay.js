import React from 'react';
import { 
  Heart, 
  ThumbsUp, 
  ThumbsDown, 
  Minus, 
  Brain, 
  Target, 
  BarChart3, 
  FileText,
  TrendingUp,
  Hash,
  Eye,
  Smile,
  Frown,
  Meh,
  Zap
} from 'lucide-react';

const ResultsDisplay = ({ results }) => {
  const getSentimentIcon = (sentiment) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return <ThumbsUp className="w-5 h-5" />;
      case 'negative':
        return <ThumbsDown className="w-5 h-5" />;
      default:
        return <Minus className="w-5 h-5" />;
    }
  };

  const getEmotionIcon = (emotion) => {
    switch (emotion.toLowerCase()) {
      case 'happy':
        return <Smile className="w-5 h-5" />;
      case 'sad':
        return <Frown className="w-5 h-5" />;
      case 'angry':
        return <Zap className="w-5 h-5" />;
      default:
        return <Meh className="w-5 h-5" />;
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return 'sentiment-positive';
      case 'negative':
        return 'sentiment-negative';
      default:
        return 'sentiment-neutral';
    }
  };

  const getEmotionColor = (emotion) => {
    switch (emotion.toLowerCase()) {
      case 'happy':
        return 'emotion-happy';
      case 'sad':
        return 'emotion-sad';
      case 'angry':
        return 'emotion-angry';
      default:
        return 'emotion-neutral';
    }
  };

  const ConfidenceBar = ({ confidence, label }) => (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-bold text-primary-600">{(confidence * 100).toFixed(1)}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-500"
          style={{ width: `${confidence * 100}%` }}
        />
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Analysis Results</h2>
        <p className="text-gray-600">Comprehensive AI-powered insights for your text</p>
      </div>

      {/* Original Text */}
      <div className="glass-morphism rounded-xl p-6">
        <div className="flex items-center space-x-2 mb-3">
          <FileText className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">Original Text</h3>
        </div>
        <p className="text-gray-700 bg-gray-50 p-4 rounded-lg italic">
          "{results.text}"
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Analysis */}
        <div className="glass-morphism rounded-xl p-6 card-hover">
          <div className="flex items-center space-x-2 mb-4">
            <Heart className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Sentiment Analysis</h3>
          </div>
          
          <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full ${getSentimentColor(results.sentiment.label)} mb-4`}>
            {getSentimentIcon(results.sentiment.label)}
            <span className="font-semibold">{results.sentiment.label}</span>
          </div>

          <ConfidenceBar 
            confidence={results.sentiment.confidence} 
            label="Confidence" 
          />

          <div className="mt-4 space-y-2">
            <div className="text-sm font-medium text-gray-700">Detailed Scores:</div>
            {Object.entries(results.sentiment.scores).map(([sentiment, score]) => (
              <div key={sentiment} className="flex justify-between items-center">
                <span className="text-sm text-gray-600 capitalize">{sentiment}:</span>
                <span className="text-sm font-medium">{score.toFixed(3)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Topics */}
        <div className="glass-morphism rounded-xl p-6 card-hover">
          <div className="flex items-center space-x-2 mb-4">
            <Target className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Multi-Label Topics</h3>
          </div>
          
          <div className="flex flex-wrap gap-2">
            {results.topics.map((topic, index) => (
              <span 
                key={index}
                className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm font-medium"
              >
                {topic}
              </span>
            ))}
          </div>
          
          <p className="text-sm text-gray-600 mt-4">
            The AI identified {results.topics.length} relevant topics in your text.
          </p>
        </div>

        {/* Aspect-wise Sentiment */}
        <div className="glass-morphism rounded-xl p-6 card-hover">
          <div className="flex items-center space-x-2 mb-4">
            <Eye className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Aspect-wise Sentiment</h3>
          </div>
          
          <div className="space-y-3">
            {Object.entries(results.aspects).map(([aspect, sentiment]) => (
              <div key={aspect} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-900 capitalize">{aspect}</span>
                <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-sm ${getSentimentColor(sentiment)}`}>
                  {getSentimentIcon(sentiment)}
                  <span>{sentiment}</span>
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Emotion Detection */}
        <div className="glass-morphism rounded-xl p-6 card-hover">
          <div className="flex items-center space-x-2 mb-4">
            <Brain className="w-5 h-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Emotion Detection</h3>
          </div>
          
          <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full ${getEmotionColor(results.emotion.label)} mb-4`}>
            {getEmotionIcon(results.emotion.label)}
            <span className="font-semibold">{results.emotion.label}</span>
          </div>

          <ConfidenceBar 
            confidence={results.emotion.confidence} 
            label="Emotion Confidence" 
          />

          <div className="mt-4 space-y-2">
            <div className="text-sm font-medium text-gray-700">Emotion Distribution:</div>
            {Object.entries(results.emotion.scores).map(([emotion, score]) => (
              <div key={emotion} className="flex justify-between items-center">
                <span className="text-sm text-gray-600 capitalize">{emotion}:</span>
                <span className="text-sm font-medium">{(score * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Text Analysis */}
      <div className="glass-morphism rounded-xl p-6">
        <div className="flex items-center space-x-2 mb-4">
          <BarChart3 className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">Text Analysis</h3>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-primary-600">{results.text_analysis.length}</div>
            <div className="text-sm text-gray-600">Characters</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-primary-600">{results.text_analysis.word_count}</div>
            <div className="text-sm text-gray-600">Words</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-primary-600">{results.text_analysis.sentence_count}</div>
            <div className="text-sm text-gray-600">Sentences</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-lg font-bold text-primary-600">{results.text_analysis.tone}</div>
            <div className="text-sm text-gray-600">Tone</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="text-sm font-medium text-gray-700 mb-1">Formality</div>
            <div className="text-lg font-semibold text-gray-900">{results.text_analysis.formality}</div>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="text-sm font-medium text-gray-700 mb-1">Sentiment Strength</div>
            <div className="text-lg font-semibold text-gray-900">{results.text_analysis.sentiment_strength}</div>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="text-sm font-medium text-gray-700 mb-1">Complexity</div>
            <div className="text-lg font-semibold text-gray-900">{results.text_analysis.complexity}</div>
          </div>
        </div>
      </div>

      {/* Keywords */}
      <div className="glass-morphism rounded-xl p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Hash className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">Key Keywords</h3>
        </div>
        
        <div className="flex flex-wrap gap-2">
          {results.keywords.map((keyword, index) => (
            <span 
              key={index}
              className="px-3 py-1 bg-gradient-to-r from-primary-100 to-primary-200 text-primary-800 rounded-full text-sm font-medium hover:from-primary-200 hover:to-primary-300 transition-colors duration-200"
            >
              {keyword}
            </span>
          ))}
        </div>
        
        <p className="text-sm text-gray-600 mt-4">
          {results.keywords.length} important keywords extracted from your text.
        </p>
      </div>
    </div>
  );
};

export default ResultsDisplay;
