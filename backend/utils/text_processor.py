import re
import string
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy as np

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # Linguistic indicators
        self.formal_indicators = self._load_formal_indicators()
        self.informal_indicators = self._load_informal_indicators()
        self.sentiment_strength_indicators = self._load_sentiment_strength_indicators()
    
    def _load_formal_indicators(self):
        """Load indicators of formal language"""
        return {
            'words': [
                'furthermore', 'moreover', 'consequently', 'therefore', 'nevertheless',
                'however', 'additionally', 'subsequently', 'accordingly', 'henceforth',
                'heretofore', 'whence', 'thence', 'thus', 'albeit', 'notwithstanding',
                'whereas', 'whilst', 'hence', 'thus', 'thereby', 'thereof'
            ],
            'phrases': [
                'in conclusion', 'on the other hand', 'in addition', 'as a result',
                'for instance', 'for example', 'in fact', 'in reality',
                'it is important to note', 'it should be noted', 'in my opinion',
                'from my perspective', 'accordingly', 'therefore', 'nevertheless'
            ],
            'punctuation_patterns': [
                r';',  # Semicolons
                r':',  # Colons
                r'\b-\b'  # Em dashes
            ]
        }
    
    def _load_informal_indicators(self):
        """Load indicators of informal language"""
        return {
            'words': [
                'awesome', 'cool', 'great', 'amazing', 'fantastic', 'wow', 'omg',
                'lol', 'lmao', 'rofl', 'btw', 'idk', 'tbh', 'ngl', 'iykyk',
                'gonna', 'wanna', 'kinda', 'sorta', 'yeah', 'nah', 'yep',
                'nope', 'yass', 'slay', 'fire', 'lit', 'dope', 'sick'
            ],
            'abbreviations': [
                'u', 'r', 'ur', 'lol', 'omg', 'btw', 'idk', 'tbh', 'ngl',
                'iykyk', 'rn', 'fr', 'nvm', 'smh', 'ikr', 'wyd', 'hmu'
            ],
            'punctuation_patterns': [
                r'!',  # Exclamation marks
                r'\.\.\.',  # Ellipsis
                r'\?\?'  # Double question marks
            ]
        }
    
    def _load_sentiment_strength_indicators(self):
        """Load indicators for sentiment strength"""
        return {
            'strong_positive': [
                'excellent', 'amazing', 'fantastic', 'wonderful', 'brilliant',
                'outstanding', 'superb', 'magnificent', 'perfect', 'incredible',
                'love', 'adore', 'cherish', 'treasure', 'ecstatic', 'thrilled'
            ],
            'moderate_positive': [
                'good', 'great', 'nice', 'enjoyable', 'pleasant', 'satisfying',
                'like', 'enjoy', 'appreciate', 'happy', 'pleased', 'content'
            ],
            'strong_negative': [
                'terrible', 'awful', 'horrible', 'disgusting', 'worst', 'pathetic',
                'disaster', 'useless', 'dreadful', 'atrocious', 'hate', 'despise',
                'loathe', 'detest', 'abysmal', 'appalling'
            ],
            'moderate_negative': [
                'bad', 'poor', 'disappointing', 'annoying', 'frustrating',
                'dislike', 'unpleasant', 'mediocre', 'subpar', 'inadequate'
            ]
        }
    
    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _count_words(self, text):
        """Count words in text"""
        words = text.split()
        return len(words)
    
    def _count_characters(self, text):
        """Count characters in text"""
        return len(text)
    
    def _count_sentences(self, text):
        """Count sentences in text"""
        sentences = sent_tokenize(text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences)
    
    def _calculate_average_word_length(self, text):
        """Calculate average word length"""
        words = text.split()
        if not words:
            return 0
        
        total_length = sum(len(word.strip(string.punctuation)) for word in words)
        return total_length / len(words)
    
    def _calculate_lexical_diversity(self, text):
        """Calculate lexical diversity (unique words / total words)"""
        words = [word.lower().strip(string.punctuation) for word in text.split()]
        if not words:
            return 0
        
        unique_words = set(words)
        return len(unique_words) / len(words)
    
    def _detect_formality(self, text):
        """Detect if text is formal or informal"""
        text_lower = text.lower()
        formal_score = 0
        informal_score = 0
        
        # Check formal indicators
        for word in self.formal_indicators['words']:
            formal_score += text_lower.count(word) * 2
        
        for phrase in self.formal_indicators['phrases']:
            formal_score += text_lower.count(phrase) * 3
        
        for pattern in self.formal_indicators['punctuation_patterns']:
            formal_score += len(re.findall(pattern, text))
        
        # Check informal indicators
        for word in self.informal_indicators['words']:
            informal_score += text_lower.count(word) * 2
        
        for word in self.informal_indicators['abbreviations']:
            informal_score += text_lower.count(word) * 2
        
        for pattern in self.informal_indicators['punctuation_patterns']:
            informal_score += len(re.findall(pattern, text))
        
        # Check for contractions (informal)
        contractions = re.findall(r"\b\w+'\w+\b", text_lower)
        informal_score += len(contractions) * 1.5
        
        # Determine formality
        if formal_score > informal_score * 1.5:
            formality = 'Formal'
        elif informal_score > formal_score * 1.5:
            formality = 'Informal'
        else:
            formality = 'Neutral'
        
        return {
            'formality': formality,
            'formal_score': formal_score,
            'informal_score': informal_score
        }
    
    def _detect_sentiment_strength(self, text):
        """Detect the strength of sentiment"""
        text_lower = text.lower()
        strong_score = 0
        moderate_score = 0
        
        # Count strong indicators
        for word in self.sentiment_strength_indicators['strong_positive']:
            strong_score += text_lower.count(word)
        
        for word in self.sentiment_strength_indicators['strong_negative']:
            strong_score += text_lower.count(word)
        
        # Count moderate indicators
        for word in self.sentiment_strength_indicators['moderate_positive']:
            moderate_score += text_lower.count(word)
        
        for word in self.sentiment_strength_indicators['moderate_negative']:
            moderate_score += text_lower.count(word)
        
        # Check for exclamation marks (strong sentiment)
        exclamation_count = text.count('!')
        strong_score += exclamation_count * 2
        
        # Check for ALL CAPS (strong sentiment)
        all_caps_words = re.findall(r'\b[A-Z]{2,}\b', text)
        strong_score += len(all_caps_words)
        
        # Determine strength
        if strong_score > moderate_score * 1.5:
            strength = 'Strong'
        elif moderate_score > strong_score * 1.5:
            strength = 'Moderate'
        else:
            strength = 'Mild'
        
        return {
            'strength': strength,
            'strong_score': strong_score,
            'moderate_score': moderate_score
        }
    
    def _analyze_complexity(self, text):
        """Analyze text complexity"""
        word_count = self._count_words(text)
        sentence_count = self._count_sentences(text)
        avg_word_length = self._calculate_average_word_length(text)
        lexical_diversity = self._calculate_lexical_diversity(text)
        
        # Calculate average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Determine complexity
        complexity_score = 0
        
        # Word length contribution
        if avg_word_length > 6:
            complexity_score += 1
        elif avg_word_length > 5:
            complexity_score += 0.5
        
        # Sentence length contribution
        if avg_sentence_length > 20:
            complexity_score += 1
        elif avg_sentence_length > 15:
            complexity_score += 0.5
        
        # Lexical diversity contribution
        if lexical_diversity > 0.7:
            complexity_score += 1
        elif lexical_diversity > 0.5:
            complexity_score += 0.5
        
        if complexity_score >= 2:
            complexity = 'Complex'
        elif complexity_score >= 1:
            complexity = 'Moderate'
        else:
            complexity = 'Simple'
        
        return {
            'complexity': complexity,
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'lexical_diversity': round(lexical_diversity, 3)
        }
    
    def analyze_text(self, text):
        """Main method to analyze text characteristics"""
        if not text:
            return {
                'length': 0,
                'word_count': 0,
                'sentence_count': 0,
                'tone': 'Neutral',
                'formality': 'Neutral',
                'sentiment_strength': 'Mild',
                'complexity': 'Simple'
            }
        
        # Basic metrics
        length = self._count_characters(text)
        word_count = self._count_words(text)
        sentence_count = self._count_sentences(text)
        
        # Advanced analysis
        formality_analysis = self._detect_formality(text)
        sentiment_strength_analysis = self._detect_sentiment_strength(text)
        complexity_analysis = self._analyze_complexity(text)
        
        # Determine overall tone
        tone_components = [
            formality_analysis['formality'],
            sentiment_strength_analysis['strength'],
            complexity_analysis['complexity']
        ]
        
        # Simple tone determination
        if sentiment_strength_analysis['strength'] == 'Strong':
            if formality_analysis['formality'] == 'Informal':
                tone = 'Casual Expressive'
            else:
                tone = 'Formal Expressive'
        elif formality_analysis['formality'] == 'Formal':
            tone = 'Formal Neutral'
        elif formality_analysis['formality'] == 'Informal':
            tone = 'Casual Neutral'
        else:
            tone = 'Neutral'
        
        return {
            'length': length,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'tone': tone,
            'formality': formality_analysis['formality'],
            'sentiment_strength': sentiment_strength_analysis['strength'],
            'complexity': complexity_analysis['complexity'],
            'detailed_analysis': {
                'formality': formality_analysis,
                'sentiment_strength': sentiment_strength_analysis,
                'complexity': complexity_analysis
            }
        }
