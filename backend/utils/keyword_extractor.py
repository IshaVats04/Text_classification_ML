import re
from collections import Counter, defaultdict
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import math

class KeywordExtractor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.tfidf_vectorizer = None
        
        # Initialize with some sample texts for TF-IDF
        self._initialize_tfidf()
    
    def _initialize_tfidf(self):
        """Initialize TF-IDF vectorizer with sample corpus"""
        sample_corpus = [
            "excellent amazing fantastic wonderful brilliant outstanding movie",
            "terrible awful horrible disgusting worst pathetic film",
            "great good nice enjoyable pleasant acting performance",
            "bad poor disappointing annoying frustrating boring story",
            "beautiful music amazing soundtrack great score audio",
            "weak poor terrible annoying soundtrack music audio",
            "brilliant direction excellent cinematography amazing visuals",
            "poor direction amateur cinematography weak camera"
        ]
        
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True,
            token_pattern=r'\b\w+\b'
        )
        
        self.tfidf_vectorizer.fit(sample_corpus)
    
    def _preprocess_text(self, text):
        """Preprocess text for keyword extraction"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stop words and lemmatize
        filtered_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                lemmatized = self.lemmatizer.lemmatize(token)
                filtered_tokens.append(lemmatized)
        
        return ' '.join(filtered_tokens)
    
    def _extract_ngrams(self, text, n=2):
        """Extract n-grams from text"""
        words = text.split()
        ngrams = []
        
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            # Only include n-grams that don't contain stop words
            if not any(word in self.stop_words for word in ngram.split()):
                ngrams.append(ngram)
        
        return ngrams
    
    def _calculate_word_frequency(self, text):
        """Calculate word frequency with TF-IDF"""
        processed_text = self._preprocess_text(text)
        
        # Get TF-IDF scores
        try:
            tfidf_matrix = self.tfidf_vectorizer.transform([processed_text])
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Create word-score mapping
            word_scores = {}
            for i, score in enumerate(tfidf_scores):
                if score > 0:
                    word = feature_names[i]
                    word_scores[word] = score
            
            return word_scores
        except:
            # Fallback to simple frequency
            words = processed_text.split()
            filtered_words = [
                word for word in words 
                if word not in self.stop_words and len(word) > 2
            ]
            return Counter(filtered_words)
    
    def _calculate_tfidf_scores(self, text):
        """Calculate simplified TF-IDF scores"""
        processed_text = self._preprocess_text(text)
        words = processed_text.split()
        
        if not words:
            return {}
        
        # Simple TF calculation
        word_freq = Counter(words)
        max_freq = max(word_freq.values()) if word_freq else 1
        tf_scores = {word: freq/max_freq for word, freq in word_freq.items()}
        
        # Simplified IDF (using log of document count assumption)
        # In practice, this would use a real corpus
        idf_scores = {word: math.log(1000 / (freq + 1)) for word, freq in word_freq.items()}
        
        # TF-IDF
        tfidf_scores = {word: tf * idf_scores[word] for word, tf in tf_scores.items()}
        
        return tfidf_scores
    
    def _extract_important_words(self, text):
        """Extract words that are likely to be important"""
        processed_text = self._preprocess_text(text)
        words = processed_text.split()
        
        # Important POS indicators (simplified for keyword extraction)
        important_patterns = {
            'nouns': [
                'acting', 'performance', 'actor', 'actress', 'cast', 'role', 'character',
                'story', 'plot', 'narrative', 'script', 'screenplay', 'storyline',
                'music', 'soundtrack', 'score', 'song', 'audio', 'sound', 'melody',
                'direction', 'director', 'cinematography', 'visuals', 'camera', 'editing'
            ],
            'adjectives': [
                'amazing', 'excellent', 'fantastic', 'wonderful', 'brilliant', 'outstanding',
                'terrible', 'awful', 'horrible', 'disgusting', 'worst', 'pathetic',
                'good', 'great', 'nice', 'enjoyable', 'pleasant', 'satisfying',
                'bad', 'poor', 'disappointing', 'annoying', 'frustrating', 'boring'
            ],
            'verbs': [
                'love', 'hate', 'enjoy', 'dislike', 'recommend', 'suggest', 'watch',
                'perform', 'act', 'direct', 'create', 'produce', 'write', 'compose'
            ]
        }
        
        important_words = []
        for word in words:
            for pos_type, word_list in important_patterns.items():
                if word in word_list:
                    important_words.append((pos_type, word))
                    break
        
        return important_words
    
    def _extract_sentiment_keywords(self, text):
        """Extract sentiment-bearing keywords"""
        processed_text = self._preprocess_text(text)
        words = processed_text.split()
        
        positive_words = [
            'excellent', 'amazing', 'fantastic', 'wonderful', 'brilliant', 'outstanding',
            'superb', 'magnificent', 'perfect', 'incredible', 'love', 'awesome',
            'great', 'good', 'nice', 'enjoyable', 'pleasant', 'satisfying'
        ]
        
        negative_words = [
            'terrible', 'awful', 'horrible', 'disgusting', 'worst', 'pathetic',
            'hate', 'despise', 'loathe', 'detest', 'abysmal',
            'bad', 'poor', 'disappointing', 'annoying', 'frustrating', 'boring'
        ]
        
        sentiment_keywords = []
        for word in words:
            if word in positive_words:
                sentiment_keywords.append(('positive', word))
            elif word in negative_words:
                sentiment_keywords.append(('negative', word))
        
        return sentiment_keywords
    
    def _extract_aspect_keywords(self, text):
        """Extract aspect-related keywords"""
        processed_text = self._preprocess_text(text)
        words = processed_text.split()
        
        aspect_keywords = {
            'acting': ['acting', 'performance', 'actor', 'actress', 'cast', 'role', 'character'],
            'story': ['story', 'plot', 'narrative', 'script', 'screenplay', 'storyline'],
            'music': ['music', 'soundtrack', 'score', 'song', 'audio', 'sound', 'melody'],
            'direction': ['direction', 'director', 'cinematography', 'visuals', 'camera']
        }
        
        found_aspects = []
        for word in words:
            for aspect, keywords in aspect_keywords.items():
                if word in keywords:
                    found_aspects.append((aspect, word))
                    break
        
        return found_aspects
    
    def extract_keywords(self, text, max_keywords=10):
        """Main method to extract keywords"""
        if not text:
            return []
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Extract different types of keywords
        tfidf_scores = self._calculate_tfidf_scores(text)
        important_words = self._extract_important_words(text)
        sentiment_keywords = self._extract_sentiment_keywords(text)
        aspect_keywords = self._extract_aspect_keywords(text)
        
        # Extract bigrams
        bigrams = self._extract_ngrams(processed_text, 2)
        bigram_freq = Counter(bigrams)
        
        # Combine all keywords with scores
        all_keywords = defaultdict(float)
        
        # Add TF-IDF based keywords
        for word, score in tfidf_scores.items():
            all_keywords[word] += score * 0.4
        
        # Add important words with higher weight
        for pos_type, word in important_words:
            all_keywords[word] += 0.5
        
        # Add sentiment keywords with higher weight
        for sentiment_type, word in sentiment_keywords:
            all_keywords[word] += 0.6
        
        # Add aspect keywords with higher weight
        for aspect_type, word in aspect_keywords:
            all_keywords[word] += 0.7
        
        # Add bigrams
        for bigram, freq in bigram_freq.items():
            all_keywords[bigram] += freq * 0.5
        
        # Sort by score and return top keywords
        sorted_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)
        
        # Return only the keywords (not scores)
        keywords = [keyword for keyword, score in sorted_keywords[:max_keywords]]
        
        return keywords
    
    def extract_keywords_with_metadata(self, text, max_keywords=10):
        """Extract keywords with additional metadata"""
        if not text:
            return []
        
        processed_text = self._preprocess_text(text)
        
        # Get basic keywords
        keywords = self.extract_keywords(text, max_keywords)
        
        # Add metadata for each keyword
        keywords_with_metadata = []
        
        for keyword in keywords:
            metadata = {
                'keyword': keyword,
                'type': 'unknown',
                'sentiment': 'neutral',
                'aspect': None,
                'frequency': 0,
                'importance_score': 0
            }
            
            # Determine type
            words = keyword.split()
            if len(words) == 1:
                important_words = self._extract_important_words(text)
                for pos_type, word in important_words:
                    if word == keyword:
                        metadata['type'] = pos_type
                        break
            
            if len(words) > 1:
                metadata['type'] = 'phrase'
            
            # Determine sentiment
            sentiment_keywords = self._extract_sentiment_keywords(text)
            positive_words = [kw for stype, kw in sentiment_keywords if stype == 'positive']
            negative_words = [kw for stype, kw in sentiment_keywords if stype == 'negative']
            
            if any(word in keyword for word in positive_words):
                metadata['sentiment'] = 'positive'
            elif any(word in keyword for word in negative_words):
                metadata['sentiment'] = 'negative'
            
            # Determine aspect
            aspect_keywords = self._extract_aspect_keywords(text)
            for aspect_type, word in aspect_keywords:
                if word in keyword:
                    metadata['aspect'] = aspect_type
                    break
            
            # Calculate frequency
            metadata['frequency'] = processed_text.count(keyword)
            
            # Calculate importance score
            tfidf_scores = self._calculate_tfidf_scores(text)
            metadata['importance_score'] = tfidf_scores.get(keyword, 0)
            
            keywords_with_metadata.append(metadata)
        
        return keywords_with_metadata
