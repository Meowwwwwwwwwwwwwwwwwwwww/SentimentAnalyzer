import os
import sys
from flask import Flask, request, jsonify, render_template

# 1. Add the project root to sys.path so we can import src.predict
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.predict import predict_sentiment

# 2. Initialize Flask app
# We explicitly point it to the templates and static folders inside the app directory
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'app', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'app', 'static')
)

@app.route('/')
def home():
    """Renders the main dashboard page."""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint that accepts JSON format: {"text": "user review"}
    and returns predicted sentiment and confidence.
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' parameter in request body"}), 400
    
    text = data['text'].strip()
    if not text:
        return jsonify({
            "sentiment": "neutral",
            "confidence": 1.0,
            "probabilities": {"positive": 0.5, "negative": 0.5}
        })
    
    try:
        result = predict_sentiment(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000...")
    app.run(debug=True, port=5000)
