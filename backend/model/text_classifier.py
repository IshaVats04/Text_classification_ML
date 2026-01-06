import numpy as np
import re
import pickle
import os
import pandas as pd
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

class TextClassifier:
    def __init__(self):
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except:
            # Fallback if VADER lexicon is not available
            self.sentiment_analyzer = None
        
        self.sentiment_vectorizer = None
        self.sentiment_model = None
        self.topic_vectorizer = None
        self.topic_models = {}
        
        # Initialize models
        try:
            self._initialize_models()
        except Exception as e:
            print(f"Warning: Could not initialize models: {e}")
            # Initialize with basic rule-based fallback
            self._initialize_fallback_models()
    
    def load_dataset(self, csv_path):
        """Load dataset from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            if 'Text' in df.columns and 'Label' in df.columns:
                return df['Text'].tolist(), df['Label'].tolist()
            else:
                raise ValueError("CSV must have 'Text' and 'Label' columns")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None, None
    
    def _initialize_models(self):
        """Initialize and train the ML models"""
        # Try to load custom dataset first
        dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'df_file.csv')
        texts, labels = self.load_dataset(dataset_path)
        
        if texts and labels:
            print(f"Loaded {len(texts)} samples from custom dataset")
            # Train sentiment model with custom data
            self._train_sentiment_model_with_data(texts, labels)
        else:
            # Fallback to hardcoded training data
            sentiment_texts = [
                ("excellent amazing fantastic wonderful brilliant outstanding", "positive"),
                ("great good nice pleasant enjoyable satisfying", "positive"),
                ("terrible awful horrible disgusting worst pathetic", "negative"),
                ("bad poor disappointing annoying frustrating boring", "negative"),
                ("okay fine average normal typical standard", "neutral"),
                ("mediocre decent acceptable reasonable", "neutral")
            ]
            self._train_sentiment_model(sentiment_texts)
        
        # Training data for topics (always use hardcoded for topics)
        topic_data = {
            'acting': [
                "acting performance actor actress cast role character portrayal",
                "brilliant acting outstanding performance amazing cast",
                "terrible acting poor performance weak cast"
            ],
            'story': [
                "story plot narrative script screenplay storyline",
                "engaging story brilliant plot amazing narrative",
                "boring story weak plot terrible narrative"
            ],
            'music': [
                "music soundtrack score song audio sound",
                "beautiful music amazing soundtrack great score",
                "annoying music terrible soundtrack poor audio"
            ],
            'direction': [
                "direction director cinematography visuals camera",
                "excellent direction brilliant cinematography stunning",
                "poor direction amateur cinematography weak"
            ],
            'overall': [
                "movie film cinema picture overall",
                "fantastic movie excellent film great",
                "terrible movie awful film worst"
            ]
        }
        
        # Train topic models
        self._train_topic_models(topic_data)
    
    def _train_sentiment_model(self, training_data):
        """Train sentiment classification model"""
        texts, labels = zip(*training_data)
        
        # Create TF-IDF vectorizer
        self.sentiment_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        # Transform texts
        X = self.sentiment_vectorizer.fit_transform(texts)
        y = list(labels)
        
        # Train model
        self.sentiment_model = LogisticRegression(random_state=42)
        self.sentiment_model.fit(X, y)
    
    def _train_sentiment_model_with_data(self, texts, labels):
        """Train sentiment model with custom dataset"""
        # Convert numeric labels to sentiment names if needed
        unique_labels = list(set(labels))
        label_mapping = {}
        
        # If labels are numeric, map them to sentiment names
        if all(isinstance(label, (int, float)) for label in unique_labels):
            if len(unique_labels) == 2:
                label_mapping = {unique_labels[0]: 'positive', unique_labels[1]: 'negative'}
            elif len(unique_labels) == 3:
                label_mapping = {unique_labels[0]: 'positive', unique_labels[1]: 'negative', unique_labels[2]: 'neutral'}
            else:
                # Default mapping for multi-class
                for i, label in enumerate(unique_labels):
                    label_mapping[label] = f'class_{i}'
        else:
            # Labels are already strings
            for label in unique_labels:
                label_mapping[label] = label
        
        # Map labels
        mapped_labels = [label_mapping[label] for label in labels]
        
        # Create TF-IDF vectorizer
        self.sentiment_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2,
            max_df=0.8
        )
        
        # Transform texts
        X = self.sentiment_vectorizer.fit_transform(texts)
        y = mapped_labels
        
        # Split for evaluation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.sentiment_model = LogisticRegression(random_state=42, max_iter=1000)
        self.sentiment_model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.sentiment_model.score(X_train, y_train)
        test_score = self.sentiment_model.score(X_test, y_test)
        print(f"Model trained - Train accuracy: {train_score:.3f}, Test accuracy: {test_score:.3f}")
        
        # Store label mapping for predictions
        self.label_mapping = label_mapping
    
    def _train_topic_models(self, topic_data):
        """Train multi-label topic classification models"""
        self.topic_vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        # Prepare training data for each topic
        all_texts = []
        for topic, texts in topic_data.items():
            all_texts.extend(texts)
        
        # Fit vectorizer on all texts
        self.topic_vectorizer.fit(all_texts)
        
        # Train a model for each topic (binary classification)
        for topic, texts in topic_data.items():
            # Create labels: 1 for texts belonging to this topic, 0 for others
            topic_texts = texts
            other_texts = []
            for other_topic, other_text_list in topic_data.items():
                if other_topic != topic:
                    other_texts.extend(other_text_list)
            
            # Balance the dataset
            other_texts = random.sample(other_texts, min(len(other_texts), len(topic_texts) * 2))
            
            training_texts = topic_texts + other_texts
            training_labels = [1] * len(topic_texts) + [0] * len(other_texts)
            
            # Transform and train
            X = self.topic_vectorizer.transform(training_texts)
            y = training_labels
            
            model = LogisticRegression(random_state=42)
            model.fit(X, y)
            
            self.topic_models[topic] = model
    
    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _initialize_fallback_models(self):
        """Initialize with basic rule-based models if ML fails"""
        # Simple rule-based sentiment vocabulary
        self.sentiment_vocab = {
            'positive': {
                'excellent': 0.9, 'amazing': 0.9, 'fantastic': 0.9, 'wonderful': 0.9,
                'great': 0.8, 'good': 0.7, 'nice': 0.6, 'enjoyable': 0.8,
                'love': 0.9, 'awesome': 0.9, 'brilliant': 0.9
            },
            'negative': {
                'terrible': 0.9, 'awful': 0.9, 'horrible': 0.9, 'disgusting': 0.9,
                'bad': 0.7, 'poor': 0.7, 'hate': 0.9, 'boring': 0.8,
                'disappointing': 0.8, 'annoying': 0.7
            },
            'neutral': {
                'okay': 0.6, 'fine': 0.6, 'average': 0.6, 'normal': 0.5,
                'mediocre': 0.6, 'decent': 0.6, 'acceptable': 0.6
            }
        }
        
        # Simple topic vocabulary
        self.topic_vocab = {
            'acting': ['acting', 'performance', 'actor', 'actress', 'cast', 'role'],
            'story': ['story', 'plot', 'narrative', 'script', 'screenplay'],
            'music': ['music', 'soundtrack', 'score', 'song', 'audio'],
            'direction': ['direction', 'director', 'cinematography', 'visuals']
        }
    
    def _calculate_vader_sentiment(self, text):
        """Calculate sentiment using VADER"""
        if self.sentiment_analyzer is None:
            # Fallback to rule-based sentiment
            text_lower = text.lower()
            positive_score = sum(self.sentiment_vocab['positive'].get(word, 0) for word in text_lower.split())
            negative_score = sum(self.sentiment_vocab['negative'].get(word, 0) for word in text_lower.split())
            
            if positive_score > negative_score:
                return 'Positive'
            elif negative_score > positive_score:
                return 'Negative'
            else:
                return 'Neutral'
        else:
            scores = self.sentiment_analyzer.polarity_scores(text)
            
            if scores['compound'] >= 0.05:
                return 'Positive'
            elif scores['compound'] <= -0.05:
                return 'Negative'
            else:
                return 'Neutral'
    
    def predict_sentiment(self, text):
        """Predict sentiment with confidence score"""
        if not text:
            return {"label": "Neutral", "confidence": 0.5, "scores": {"positive": 0.33, "negative": 0.33, "neutral": 0.34}}
        
        # Preprocess
        processed_text = self._preprocess_text(text)
        
        # Get VADER sentiment
        vader_sentiment = self._calculate_vader_sentiment(text)
        vader_scores = self.sentiment_analyzer.polarity_scores(text)
        
        # Get ML model prediction
        try:
            X = self.sentiment_vectorizer.transform([processed_text])
            ml_prediction = self.sentiment_model.predict(X)[0]
            ml_proba = self.sentiment_model.predict_proba(X)[0]
            
            # Map to our labels
            label_map = {'positive': 'Positive', 'negative': 'Negative', 'neutral': 'Neutral'}
            ml_sentiment = label_map.get(ml_prediction, 'Neutral')
            
            # Combine VADER and ML results
            if ml_proba.max() > 0.7:
                final_sentiment = ml_sentiment
                confidence = ml_proba.max()
            else:
                final_sentiment = vader_sentiment
                confidence = abs(vader_scores['compound'])
            
            # Calculate detailed scores
            scores = {
                'positive': max(0, vader_scores['pos']),
                'negative': max(0, vader_scores['neg']),
                'neutral': max(0, vader_scores['neu'])
            }
            
            # Normalize scores
            total = sum(scores.values())
            if total > 0:
                scores = {k: v/total for k, v in scores.items()}
            else:
                scores = {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
            
        except:
            # Fallback to VADER
            final_sentiment = vader_sentiment
            confidence = abs(vader_scores['compound'])
            scores = {
                'positive': max(0, vader_scores['pos']),
                'negative': max(0, vader_scores['neg']),
                'neutral': max(0, vader_scores['neu'])
            }
        
        return {
            'label': final_sentiment,
            'confidence': min(confidence, 1.0),
            'scores': {k: round(v, 3) for k, v in scores.items()}
        }
    
    def predict_topics(self, text):
        """Predict topics for multi-label classification"""
        if not text:
            return ["Overall"]
        
        processed_text = self._preprocess_text(text)
        detected_topics = []
        
        # Try ML approach first
        if self.topic_vectorizer is not None and self.topic_models:
            try:
                X = self.topic_vectorizer.transform([processed_text])
                
                for topic, model in self.topic_models.items():
                    try:
                        prediction = model.predict(X)[0]
                        probability = model.predict_proba(X)[0][1]  # Probability of being this topic
                        
                        if prediction == 1 and probability > 0.3:  # Threshold for topic detection
                            detected_topics.append(topic.capitalize())
                    except:
                        continue
            except:
                pass
        
        # Fallback to keyword-based detection if ML fails or no models
        if not detected_topics:
            text_lower = text.lower()
            topic_vocab = getattr(self, 'topic_vocab', {
                'acting': ['acting', 'performance', 'actor', 'actress', 'cast', 'role', 'character'],
                'story': ['story', 'plot', 'narrative', 'script', 'screenplay', 'storyline'],
                'music': ['music', 'soundtrack', 'score', 'song', 'audio', 'sound'],
                'direction': ['direction', 'director', 'cinematography', 'visuals', 'camera']
            })
            
            for topic, keywords in topic_vocab.items():
                if any(keyword in text_lower for keyword in keywords):
                    detected_topics.append(topic.capitalize())
        
        # If no topics detected, default to 'Overall'
        if not detected_topics:
            detected_topics = ['Overall']
        
        return detected_topics
