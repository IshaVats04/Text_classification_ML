import React from 'react';
import { 
  Brain, 
  Target, 
  TrendingUp, 
  Hash, 
  Smile, 
  BarChart3, 
  Zap,
  CheckCircle
} from 'lucide-react';

const FeatureShowcase = () => {
  const features = [
    {
      icon: <Target className="w-6 h-6" />,
      title: "Multi-Label Classification",
      description: "Advanced AI that identifies multiple topics simultaneously - Sentiment, Acting, Story, Music, Direction, and Overall analysis.",
      color: "from-blue-500 to-blue-600"
    },
    {
      icon: <Brain className="w-6 h-6" />,
      title: "Aspect-wise Sentiment Analysis",
      description: "Granular sentiment breakdown for different aspects. Understand exactly what users like or dislike about specific elements.",
      color: "from-purple-500 to-purple-600"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Confidence Scoring",
      description: "Probability scores for all predictions. Know exactly how confident the AI is about each analysis result.",
      color: "from-green-500 to-green-600"
    },
    {
      icon: <Hash className="w-6 h-6" />,
      title: "Keyword Extraction",
      description: "Intelligent keyword identification using TF-IDF and frequency analysis. Extract the most important terms automatically.",
      color: "from-orange-500 to-orange-600"
    },
    {
      icon: <Smile className="w-6 h-6" />,
      title: "Emotion Detection",
      description: "Detect emotions like Happy, Sad, Angry, and Neutral. Understand the emotional tone behind the text.",
      color: "from-yellow-500 to-yellow-600"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Text Analysis",
      description: "Comprehensive text metrics including length, tone, formality, sentiment strength, and complexity analysis.",
      color: "from-red-500 to-red-600"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Batch Processing",
      description: "Upload CSV files to analyze hundreds of texts at once. Perfect for large-scale sentiment analysis projects.",
      color: "from-indigo-500 to-indigo-600"
    }
  ];

  const capabilities = [
    "Real-time analysis with sub-second response times",
    "Support for multiple languages and dialects",
    "Scalable architecture for enterprise deployments",
    "RESTful API for easy integration",
    "Comprehensive documentation and examples",
    "Privacy-focused - no data storage required"
  ];

  return (
    <div className="space-y-12">
      {/* Features Grid */}
      <div>
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Advanced NLP Features
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Cutting-edge natural language processing capabilities that provide deep insights into your text data
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="glass-morphism rounded-xl p-6 card-hover group"
            >
              <div className={`inline-flex p-3 rounded-lg bg-gradient-to-r ${feature.color} text-white mb-4 group-hover:scale-110 transition-transform duration-300`}>
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Capabilities Section */}
      <div className="glass-morphism rounded-2xl p-8">
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Why Choose Our Text Classification AI?
          </h3>
          <p className="text-gray-600">
            Built with state-of-the-art machine learning techniques for maximum accuracy and reliability
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {capabilities.map((capability, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0 mt-1">
                <CheckCircle className="w-5 h-5 text-green-600" />
              </div>
              <p className="text-gray-700">{capability}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Use Cases */}
      <div>
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Perfect For Multiple Use Cases
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Brain className="w-8 h-8 text-blue-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Customer Feedback</h4>
            <p className="text-gray-600 text-sm">
              Analyze customer reviews and feedback to improve products and services
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Target className="w-8 h-8 text-purple-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Social Media</h4>
            <p className="text-gray-600 text-sm">
              Monitor social media sentiment and trends in real-time
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <BarChart3 className="w-8 h-8 text-green-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Market Research</h4>
            <p className="text-gray-600 text-sm">
              Gain insights from survey responses and market analysis
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeatureShowcase;
