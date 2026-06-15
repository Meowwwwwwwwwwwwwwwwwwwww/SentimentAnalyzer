import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Ensure output directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

# 1. Download and save raw data
URL = "https://raw.githubusercontent.com/rasvob/VSB-FEI-Deep-Learning-Exercises/main/datasets/yelp_labelled.txt"
RAW_DATA_PATH = os.path.join('data', 'yelp_labelled.txt')

print("Downloading Yelp dataset...")
df = pd.read_csv(URL, names=['review', 'label'], sep='\t')
df.to_csv(RAW_DATA_PATH, sep='\t', index=False, header=False)
print(f"Raw data saved to {RAW_DATA_PATH}")

X = df['review']
y = df['label']

# 2. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Vectorize text (fitting only on train data)
print("Vectorizing reviews...")
vectorizer = TfidfVectorizer(max_features=2500, stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. Train the model
print("Training Logistic Regression model...")
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# 5. Evaluate the model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"Training Complete! Test Accuracy: {accuracy * 100:.2f}%")

# 6. Save model and vectorizer inside models/
MODEL_PATH = os.path.join('models', 'sentiment_model.joblib')
VECTORIZER_PATH = os.path.join('models', 'tfidf_vectorizer.joblib')

joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print(f"Model saved to {MODEL_PATH}")
print(f"Vectorizer saved to {VECTORIZER_PATH}")
