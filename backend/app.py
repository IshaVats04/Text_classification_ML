from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import pandas as pd
import pickle
import re
import os
from collections import Counter
import io
import csv

from model.text_classifier import TextClassifier
from model.aspect_analyzer import AspectAnalyzer
from model.emotion_detector import EmotionDetector
from utils.text_processor import TextProcessor
from utils.keyword_extractor import KeywordExtractor

app = Flask(__name__)
CORS(app)

# Initialize models
text_classifier = TextClassifier()
aspect_analyzer = AspectAnalyzer()
emotion_detector = EmotionDetector()
text_processor = TextProcessor()
keyword_extractor = KeywordExtractor()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Text Classification API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "classify": "/classify (POST)",
            "sentiment_only": "/sentiment-only (POST)",
            "topics_only": "/topics-only (POST)",
            "batch_analyze": "/batch-analyze (POST)",
            "upload_csv": "/upload-csv (POST)"
        },
        "usage": "Send POST requests to classify text with sentiment, topics, emotions, and aspects"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Text Classification API is running"})

@app.route('/classify', methods=['POST'])
def classify_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Multi-label classification
        sentiment_result = text_classifier.predict_sentiment(text)
        topic_result = text_classifier.predict_topics(text)
        
        # Aspect-wise sentiment analysis
        aspect_result = aspect_analyzer.analyze_aspects(text)
        
        # Emotion detection
        emotion_result = emotion_detector.detect_emotion(text)
        
        # Text analysis
        text_analysis = text_processor.analyze_text(text)
        
        # Keyword extraction
        keywords = keyword_extractor.extract_keywords(text)
        
        return jsonify({
            "text": text,
            "sentiment": sentiment_result,
            "topics": topic_result,
            "aspects": aspect_result,
            "emotion": emotion_result,
            "text_analysis": text_analysis,
            "keywords": keywords
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/debug-upload', methods=['POST'])
def debug_upload():
    try:
        print("=== DEBUG UPLOAD REQUEST ===")
        print(f"Request files: {list(request.files.keys())}")
        print(f"Request form: {list(request.form.keys())}")
        print(f"Request headers: {dict(request.headers)}")
        
        if 'file' not in request.files:
            return jsonify({"error": "No file provided", "files_received": list(request.files.keys())}), 400
        
        file = request.files['file']
        return jsonify({
            "message": "File received successfully",
            "filename": file.filename,
            "content_length": file.content_length,
            "mimetype": file.mimetype
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/simple-batch', methods=['POST'])
def simple_batch():
    try:
        print("=== SIMPLE BATCH REQUEST ===")
        
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        print(f"Simple batch file: {file.filename}")
        
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files are supported"}), 400
        
        # Read CSV
        df = pd.read_csv(file)
        print(f"Simple batch processing {len(df)} rows")
        
        # Find text column
        text_column = None
        for col in df.columns:
            if col.lower() == 'text':
                text_column = col
                break
        
        if text_column is None:
            return jsonify({"error": "CSV must have a 'text' column"}), 400
        
        # Simple processing - just sentiment and basic info
        results = []
        for index, row in df.head(20).iterrows():  # Max 20 rows for simple test
            text = str(row[text_column])
            
            # Only do sentiment analysis (fastest)
            try:
                sentiment_result = text_classifier.predict_sentiment(text)
            except Exception as e:
                print(f"Sentiment error: {e}")
                sentiment_result = {"label": "Neutral", "confidence": 0.5}
            
            result = {
                "id": index + 1,
                "text": text[:100] + "..." if len(text) > 100 else text,  # Truncate for display
                "sentiment": sentiment_result,
                "length": len(text)
            }
            results.append(result)
        
        # Create simple CSV response
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Text', 'Sentiment', 'Confidence', 'Length'])
        
        for result in results:
            writer.writerow([
                result['id'],
                result['text'],
                result['sentiment']['label'],
                result['sentiment']['confidence'],
                result['length']
            ])
        
        print(f"Simple batch completed: {len(results)} rows")
        
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='simple_analysis_results.csv'
        )
        
    except Exception as e:
        print(f"Simple batch error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    try:
        print("=== BATCH ANALYSIS REQUEST RECEIVED ===")
        
        if 'file' not in request.files:
            print("ERROR: No file in request.files")
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}, Size: {file.content_length}")
        
        # Check file size (max 10MB)
        if hasattr(file, 'content_length') and file.content_length > 10 * 1024 * 1024:
            return jsonify({"error": "File size must be less than 10MB"}), 400
        
        if file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith('.csv'):
            print(f"ERROR: Invalid file extension: {file.filename}")
            return jsonify({"error": "Only CSV files are supported"}), 400
        
        # Read CSV file with error handling
        try:
            df = pd.read_csv(file)
        except Exception as e:
            return jsonify({"error": f"Failed to read CSV file: {str(e)}"}), 400
        
        # Check if dataframe is empty
        if df.empty:
            return jsonify({"error": "CSV file is empty"}), 400
        
        # Limit processing to first 50 rows for performance (reduced from 100)
        max_rows = 50
        if len(df) > max_rows:
            df = df.head(max_rows)
            print(f"Limited processing to first {max_rows} rows for performance")
        
        # Debug: Print column names
        print(f"CSV columns found: {list(df.columns)}")
        print(f"Processing {len(df)} rows...")
        
        # Check for 'text' column (case insensitive)
        text_column = None
        for col in df.columns:
            if col.lower() == 'text':
                text_column = col
                break
        
        if text_column is None:
            return jsonify({
                "error": f"CSV must have a 'text' column. Found columns: {list(df.columns)}",
                "suggestion": "Make sure your CSV has a column named 'text' (case-sensitive)"
            }), 400
        
        # Check if text column has data
        if df[text_column].isna().all():
            return jsonify({"error": "Text column is empty"}), 400
        
        results = []
        total_rows = len(df)
        
        for index, row in df.iterrows():
            try:
                # Progress tracking
                if (index + 1) % 5 == 0 or index == total_rows - 1:
                    print(f"Processing row {index + 1}/{total_rows}...")
                
                text = str(row[text_column])
                
                # Skip empty texts
                if not text or text.strip() == '':
                    continue
                
                # Simplified analysis for batch processing (faster)
                sentiment_result = text_classifier.predict_sentiment(text)
                topic_result = text_classifier.predict_topics(text)
                
                # Simplified aspect and emotion analysis for speed
                try:
                    aspect_result = aspect_analyzer.analyze_aspects(text)
                except:
                    aspect_result = {'acting': 'Neutral', 'story': 'Neutral', 'music': 'Neutral', 'direction': 'Neutral'}
                
                try:
                    emotion_result = emotion_detector.detect_emotion(text)
                except:
                    emotion_result = {'label': 'Neutral', 'confidence': 0.5}
                
                try:
                    text_analysis = text_processor.analyze_text(text)
                except:
                    text_analysis = {'length': len(text), 'tone': 'Casual'}
                
                try:
                    keywords = keyword_extractor.extract_keywords(text, max_keywords=5)  # Reduced keywords
                except:
                    keywords = ['text']  # Fallback
                
                result = {
                    "id": index + 1,
                    "text": text,
                    "sentiment": sentiment_result,
                    "topics": topic_result,
                    "aspects": aspect_result,
                    "emotion": emotion_result,
                    "text_analysis": text_analysis,
                    "keywords": keywords
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error processing row {index}: {str(e)}")
                continue
        
        print(f"Completed processing {len(results)} rows successfully")
        
        # Create downloadable CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Text', 'Sentiment', 'Sentiment_Confidence', 'Topics',
            'Acting_Sentiment', 'Story_Sentiment', 'Music_Sentiment', 'Direction_Sentiment',
            'Emotion', 'Emotion_Confidence', 'Text_Length', 'Tone', 'Keywords'
        ])
        
        # Write data
        for result in results:
            try:
                writer.writerow([
                    result['id'],
                    result['text'],
                    result['sentiment']['label'],
                    result['sentiment']['confidence'],
                    ', '.join(result['topics']),
                    result['aspects'].get('acting', 'Neutral'),
                    result['aspects'].get('story', 'Neutral'),
                    result['aspects'].get('music', 'Neutral'),
                    result['aspects'].get('direction', 'Neutral'),
                    result['emotion']['label'],
                    result['emotion']['confidence'],
                    result['text_analysis']['length'],
                    result['text_analysis']['tone'],
                    ', '.join(result['keywords'])
                ])
            except Exception as e:
                print(f"Error writing CSV row {result.get('id', 'unknown')}: {str(e)}")
                continue
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='text_analysis_results.csv'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sentiment-only', methods=['POST'])
def sentiment_only():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = text_classifier.predict_sentiment(text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/topics-only', methods=['POST'])
def topics_only():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = text_classifier.predict_topics(text)
        return jsonify({"topics": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
