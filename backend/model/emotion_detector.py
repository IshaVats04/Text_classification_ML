import re
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

class EmotionDetector:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.emotion_vectorizer = None
        self.emotion_model = None
        
        # Initialize models
        self._initialize_emotion_models()
    
    def _initialize_emotion_models(self):
        """Initialize and train emotion classification models"""
        # Training data for emotions
        emotion_data = {
            'happy': [
                "ecstatic joyful delighted thrilled elated euphoric",
                "wonderful amazing brilliant outstanding fantastic",
                "love adore cherish treasure blissful happy",
                "excellent superb magnificent perfect incredible",
                "great good nice pleasant enjoyable cheerful"
            ],
            'sad': [
                "devastated heartbroken miserable grief-stricken crushed",
                "terrible awful horrible disgusting worst pathetic",
                "disappointed let down underwhelmed unimpressed",
                "sad unhappy down blue depressed gloomy",
                "lonely alone sorrowful melancholy forlorn"
            ],
            'angry': [
                "furious enraged outraged infuriated livid irate",
                "hate despise loathe detest abysmal",
                "annoying frustrating irritating aggravating perturbed",
                "angry mad upset resentful indignant exasperated",
                "disaster useless dreadful atrocious appalling"
            ],
            'neutral': [
                "okay fine average normal typical standard",
                "decent acceptable reasonable ordinary regular",
                "indifferent unconcerned detached impartial objective",
                "balanced calm composed serene moderate",
                "normal typical standard regular common"
            ]
        }
        
        # Train emotion model
        self._train_emotion_model(emotion_data)
    
    def _train_emotion_model(self, emotion_data):
        """Train emotion classification model"""
        # Prepare training data
        all_texts = []
        all_labels = []
        
        for emotion, texts in emotion_data.items():
            for text in texts:
                all_texts.append(text)
                all_labels.append(emotion)
        
        # Create TF-IDF vectorizer
        self.emotion_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        # Transform texts
        X = self.emotion_vectorizer.fit_transform(all_texts)
        y = all_labels
        
        # Train model
        self.emotion_model = LogisticRegression(random_state=42, max_iter=1000)
        self.emotion_model.fit(X, y)
    
    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_emotion_keywords(self, text):
        """Extract emotion keywords from text"""
        emotion_keywords = {
            'happy': [
                'ecstatic', 'joyful', 'delighted', 'thrilled', 'elated', 'euphoric',
                'excellent', 'amazing', 'fantastic', 'wonderful', 'brilliant',
                'love', 'adore', 'cherish', 'treasure', 'blissful',
                'great', 'good', 'nice', 'enjoyable', 'pleasant', 'cheerful'
            ],
            'sad': [
                'devastated', 'heartbroken', 'miserable', 'grief-stricken', 'crushed',
                'terrible', 'awful', 'horrible', 'disgusting', 'worst', 'pathetic',
                'disappointed', 'let down', 'underwhelmed', 'unimpressed',
                'sad', 'unhappy', 'down', 'blue', 'depressed', 'gloomy',
                'lonely', 'alone', 'sorrowful', 'melancholy', 'forlorn'
            ],
            'angry': [
                'furious', 'enraged', 'outraged', 'infuriated', 'livid', 'irate',
                'hate', 'despise', 'loathe', 'detest', 'abysmal',
                'annoying', 'frustrating', 'irritating', 'aggravating', 'perturbed',
                'angry', 'mad', 'upset', 'resentful', 'indignant', 'exasperated'
            ],
            'neutral': [
                'okay', 'fine', 'average', 'normal', 'typical', 'standard',
                'decent', 'acceptable', 'reasonable', 'ordinary', 'regular',
                'indifferent', 'unconcerned', 'detached', 'impartial', 'objective',
                'balanced', 'calm', 'composed', 'serene', 'moderate'
            ]
        }
        
        text_lower = text.lower()
        found_emotions = defaultdict(int)
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                count = text_lower.count(keyword)
                if count > 0:
                    found_emotions[emotion] += count
        
        return found_emotions
    
    def _calculate_vader_emotion(self, text):
        """Calculate emotion using VADER sentiment analysis"""
        scores = self.sentiment_analyzer.polarity_scores(text)
        
        # Map VADER scores to emotions
        if scores['compound'] >= 0.6:
            return 'Happy', scores['compound']
        elif scores['compound'] <= -0.6:
            return 'Angry', abs(scores['compound'])
        else:
            return 'Neutral', abs(scores['compound'])
    
    def _calculate_lexical_emotion(self, text):
        """Calculate emotion using lexical analysis"""
        emotion_keywords = self._extract_emotion_keywords(text)
        
        if not emotion_keywords:
            return 'Neutral', 0.5
        
        # Find dominant emotion
        max_emotion = max(emotion_keywords, key=emotion_keywords.get)
        max_count = emotion_keywords[max_emotion]
        
        # Calculate confidence based on keyword density
        total_keywords = sum(emotion_keywords.values())
        confidence = max_count / total_keywords if total_keywords > 0 else 0.5
        
        # Map to our labels
        emotion_map = {
            'happy': 'Happy',
            'sad': 'Sad',
            'angry': 'Angry',
            'neutral': 'Neutral'
        }
        
        return emotion_map.get(max_emotion, 'Neutral'), confidence
    
    def detect_emotion(self, text):
        """Main method to detect emotion with confidence"""
        if not text:
            return {
                'label': 'Neutral',
                'confidence': 0.5,
                'scores': {'happy': 0.25, 'sad': 0.25, 'angry': 0.25, 'neutral': 0.25}
            }
        
        # Get emotion from different methods
        vader_emotion, vader_confidence = self._calculate_vader_emotion(text)
        lexical_emotion, lexical_confidence = self._calculate_lexical_emotion(text)
        
        # Get ML model prediction
        try:
            processed_text = self._preprocess_text(text)
            X = self.emotion_vectorizer.transform([processed_text])
            ml_prediction = self.emotion_model.predict(X)[0]
            ml_proba = self.emotion_model.predict_proba(X)[0]
            
            # Get probability for predicted emotion
            emotion_classes = list(self.emotion_model.classes_)
            if ml_prediction in emotion_classes:
                ml_index = emotion_classes.index(ml_prediction)
                ml_confidence = ml_proba[ml_index]
            else:
                ml_confidence = 0.5
            
            # Map to our labels
            emotion_map = {
                'happy': 'Happy',
                'sad': 'Sad',
                'angry': 'Angry',
                'neutral': 'Neutral'
            }
            ml_emotion = emotion_map.get(ml_prediction, 'Neutral')
            
            # Combine results with weighted voting
            if ml_confidence > 0.7:
                final_emotion = ml_emotion
                confidence = ml_confidence
            elif lexical_confidence > vader_confidence:
                final_emotion = lexical_emotion
                confidence = lexical_confidence
            else:
                final_emotion = vader_emotion
                confidence = vader_confidence
            
        except:
            # Fallback to lexical analysis
            final_emotion = lexical_emotion
            confidence = lexical_confidence
        
        # Calculate emotion distribution scores
        emotion_keywords = self._extract_emotion_keywords(text)
        total_keywords = sum(emotion_keywords.values()) if emotion_keywords else 1
        
        scores = {
            'happy': emotion_keywords.get('happy', 0) / total_keywords,
            'sad': emotion_keywords.get('sad', 0) / total_keywords,
            'angry': emotion_keywords.get('angry', 0) / total_keywords,
            'neutral': emotion_keywords.get('neutral', 0) / total_keywords
        }
        
        # Normalize scores
        score_sum = sum(scores.values())
        if score_sum > 0:
            scores = {k: round(v/score_sum, 3) for k, v in scores.items()}
        else:
            scores = {'happy': 0.25, 'sad': 0.25, 'angry': 0.25, 'neutral': 0.25}
        
        return {
            'label': final_emotion,
            'confidence': min(confidence, 1.0),
            'scores': scores
        }
