# Sentiment Analyzer Web App

A clean, production-grade Machine Learning web application that classifies text reviews as positive or negative in real-time. The model uses TF-IDF vectorization and Logistic Regression, achieving **79.82% accuracy** trained on 2,748 Yelp reviews.

## Project Structure
```text
sentiment_analyzer/
├── app/                       # Web Application folder
│   ├── app.py                 # Flask server
│   ├── static/                # Styles and javascript scripting
│   │   ├── script.js          # Dynamic UI and API fetching
│   │   └── style.css          # Glassmorphism dark-mode styles
│   └── templates/             # HTML templates
│       └── index.html         # Page structure
├── data/                      # Data storage
│   └── yelp_labelled.txt      # Downloaded raw dataset
├── models/                    # Saved ML model binaries
│   ├── sentiment_model.joblib # Trained Logistic Regression weights
│   └── tfidf_vectorizer.joblib# Trained TF-IDF feature extractor
├── src/                       # Production scripts
│   ├── predict.py             # Inference module
│   └── train.py               # Model training script
├── requirements.txt           # Dependencies
└── README.md                  # Project Documentation
```

## Setup & Running the Application

### 1. Set up Virtual Environment
If you haven't already, create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Train the Model
Train the model and save the joblib files:
```bash
python src/train.py
```

### 4. Run the Web Server
Launch the Flask development server:
```bash
python app/app.py
```

Open your browser and navigate to **`http://127.0.0.1:5000`** to view the app!
