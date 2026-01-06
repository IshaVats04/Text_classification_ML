import re
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import random

class AspectAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.aspect_vectorizer = None
        self.aspect_models = {}
        
        # Initialize models
        self._initialize_aspect_models()
    
    def _initialize_aspect_models(self):
        """Initialize aspect-based sentiment models"""
        # Training data for each aspect
        aspect_data = {
            'acting': {
                'positive': [
                    "brilliant acting outstanding performance amazing cast",
                    "excellent performance wonderful acting superb cast",
                    "fantastic acting great performance amazing role",
                    "outstanding cast brilliant acting wonderful performance"
                ],
                'negative': [
                    "terrible acting poor performance weak cast",
                    "awful acting horrible performance terrible cast",
                    "bad acting poor performance weak role",
                    "disappointing acting mediocre performance terrible cast"
                ],
                'neutral': [
                    "average acting decent performance okay cast",
                    "mediocre acting ordinary performance normal cast",
                    "typical acting standard performance regular cast"
                ]
            },
            'story': {
                'positive': [
                    "brilliant story engaging plot amazing narrative",
                    "excellent story fantastic plot wonderful narrative",
                    "amazing story great plot engaging narrative",
                    "outstanding storyline brilliant plot fantastic narrative"
                ],
                'negative': [
                    "terrible story boring plot weak narrative",
                    "awful story horrible plot terrible narrative",
                    "bad story poor plot weak storyline",
                    "disappointing story mediocre plot terrible narrative"
                ],
                'neutral': [
                    "average story decent plot okay narrative",
                    "mediocre story ordinary plot normal narrative",
                    "typical story standard plot regular narrative"
                ]
            },
            'music': {
                'positive': [
                    "beautiful music amazing soundtrack great score",
                    "excellent music fantastic soundtrack wonderful score",
                    "amazing music great soundtrack beautiful score",
                    "outstanding music brilliant soundtrack fantastic score"
                ],
                'negative': [
                    "terrible music annoying soundtrack poor score",
                    "awful music horrible soundtrack terrible score",
                    "bad music poor soundtrack weak score",
                    "disappointing music mediocre soundtrack terrible score"
                ],
                'neutral': [
                    "average music decent soundtrack okay score",
                    "mediocre music ordinary soundtrack normal score",
                    "typical music standard soundtrack regular score"
                ]
            },
            'direction': {
                'positive': [
                    "brilliant direction excellent cinematography amazing visuals",
                    "excellent direction fantastic cinematography wonderful visuals",
                    "amazing direction great cinematography beautiful visuals",
                    "outstanding direction brilliant cinematography fantastic visuals"
                ],
                'negative': [
                    "terrible direction poor cinematography weak visuals",
                    "awful direction horrible cinematography terrible visuals",
                    "bad direction poor cinematography weak camera",
                    "disappointing direction mediocre cinematography terrible visuals"
                ],
                'neutral': [
                    "average direction decent cinematography okay visuals",
                    "mediocre direction ordinary cinematography normal camera",
                    "typical direction standard cinematography regular visuals"
                ]
            }
        }
        
        # Train models for each aspect
        self._train_aspect_models(aspect_data)
    
    def _train_aspect_models(self, aspect_data):
        """Train sentiment models for each aspect"""
        self.aspect_vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        # Prepare all training texts
        all_texts = []
        for aspect, sentiments in aspect_data.items():
            for sentiment, texts in sentiments.items():
                all_texts.extend(texts)
        
        # Fit vectorizer
        self.aspect_vectorizer.fit(all_texts)
        
        # Train model for each aspect-sentiment combination
        for aspect, sentiments in aspect_data.items():
            self.aspect_models[aspect] = {}
            
            for sentiment, texts in sentiments.items():
                # Create training data
                positive_texts = sentiments.get('positive', [])
                negative_texts = sentiments.get('negative', [])
                neutral_texts = sentiments.get('neutral', [])
                
                # Balance dataset
                min_size = min(len(positive_texts), len(negative_texts), len(neutral_texts))
                if min_size == 0:
                    continue
                
                training_texts = positive_texts[:min_size] + negative_texts[:min_size] + neutral_texts[:min_size]
                training_labels = ['positive'] * min_size + ['negative'] * min_size + ['neutral'] * min_size
                
                # Shuffle
                combined = list(zip(training_texts, training_labels))
                random.shuffle(combined)
                training_texts, training_labels = zip(*combined)
                
                # Train model
                X = self.aspect_vectorizer.transform(training_texts)
                y = list(training_labels)
                
                model = LogisticRegression(random_state=42)
                model.fit(X, y)
                
                self.aspect_models[aspect][sentiment] = model
    
    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_aspect_sentences(self, text):
        """Extract sentences that mention specific aspects"""
        sentences = sent_tokenize(text)
        aspect_sentences = defaultdict(list)
        
        aspect_keywords = {
            'acting': ['acting', 'performance', 'actor', 'actress', 'cast', 'role', 'character'],
            'story': ['story', 'plot', 'narrative', 'script', 'screenplay', 'storyline'],
            'music': ['music', 'soundtrack', 'score', 'song', 'audio', 'sound'],
            'direction': ['direction', 'director', 'cinematography', 'visuals', 'camera']
        }
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for aspect, keywords in aspect_keywords.items():
                if any(keyword in sentence_lower for keyword in keywords):
                    aspect_sentences[aspect].append(sentence)
                    break
        
        return aspect_sentences
    
    def _predict_aspect_sentiment_ml(self, text, aspect):
        """Predict sentiment for a specific aspect using ML"""
        try:
            processed_text = self._preprocess_text(text)
            X = self.aspect_vectorizer.transform([processed_text])
            
            # Get predictions from all sentiment models for this aspect
            sentiment_scores = {}
            for sentiment, model in self.aspect_models.get(aspect, {}).items():
                try:
                    probability = model.predict_proba(X)[0]
                    sentiment_index = list(model.classes_).index(sentiment)
                    sentiment_scores[sentiment] = probability[sentiment_index]
                except:
                    sentiment_scores[sentiment] = 0.0
            
            # Find best sentiment
            if sentiment_scores:
                best_sentiment = max(sentiment_scores, key=sentiment_scores.get)
                confidence = sentiment_scores[best_sentiment]
                
                # Map to our labels
                sentiment_map = {
                    'positive': 'Positive',
                    'negative': 'Negative', 
                    'neutral': 'Neutral'
                }
                
                return sentiment_map.get(best_sentiment, 'Neutral'), confidence
            else:
                return 'Neutral', 0.5
                
        except:
            return 'Neutral', 0.5
    
    def _predict_aspect_sentiment_vader(self, text):
        """Predict sentiment using VADER as fallback"""
        scores = self.sentiment_analyzer.polarity_scores(text)
        
        if scores['compound'] >= 0.05:
            return 'Positive'
        elif scores['compound'] <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    
    def analyze_aspects(self, text):
        """Main method to analyze aspects and their sentiments"""
        if not text:
            return {}
        
        # Extract aspect-specific sentences
        aspect_sentences = self._extract_aspect_sentences(text)
        
        # Analyze each aspect
        results = {}
        
        for aspect in ['acting', 'story', 'music', 'direction']:
            if aspect in aspect_sentences and aspect_sentences[aspect]:
                # Use ML if available, otherwise fallback to VADER
                aspect_text = ' '.join(aspect_sentences[aspect])
                
                if aspect in self.aspect_models:
                    sentiment, confidence = self._predict_aspect_sentiment_ml(aspect_text, aspect)
                else:
                    sentiment = self._predict_aspect_sentiment_vader(aspect_text)
                    confidence = 0.5
                
                results[aspect] = sentiment
            else:
                # If no aspect-specific sentences, analyze overall text
                if aspect in self.aspect_models:
                    sentiment, confidence = self._predict_aspect_sentiment_ml(text, aspect)
                else:
                    sentiment = self._predict_aspect_sentiment_vader(text)
                    confidence = 0.5
                
                results[aspect] = sentiment
        
        return results
