import os
import joblib

# Determine file paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'sentiment_model.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.joblib')

# Load the model and vectorizer once when the module is imported
# This is an industry best practice for performance (lazy loading or load-on-start)
model = None
vectorizer = None

def load_resources():
    global model, vectorizer
    if model is None or vectorizer is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError(
                "Model files not found. Please run 'python src/train.py' first to train the model."
            )
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

def predict_sentiment(text: str):
    """
    Predicts the sentiment of a given text review.
    Returns a dictionary with sentiment classification and confidence score.
    """
    load_resources()
    
    # 1. Transform input text using the loaded vectorizer
    text_tfidf = vectorizer.transform([text])
    
    # 2. Make prediction
    prediction = model.predict(text_tfidf)[0]
    probabilities = model.predict_proba(text_tfidf)[0]
    
    # 3. Format result
    sentiment = "positive" if prediction == 1 else "negative"
    confidence = probabilities[prediction]
    
    return {
        "sentiment": sentiment,
        "confidence": float(confidence),
        "probabilities": {
            "positive": float(probabilities[1]),
            "negative": float(probabilities[0])
        }
    }

# If this file is run directly, allow terminal testing
if __name__ == '__main__':
    print("Testing predictor...")
    try:
        res = predict_sentiment("This is a fantastic place!")
        print(f"Test Result: {res}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
