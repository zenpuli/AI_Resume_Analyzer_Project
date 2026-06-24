import os
import sys

# 🎯 Force Python to look at the 'backend' root directory for custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from utils.resume_parser import clean_resume_text 

# Point directly to 'dataset.csv' inside your 'ml/' subfolder
ML_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ML_DIR, "dataset.csv")

def run_model_training_pipeline():
    print("⏳ Loading resume matching dataset...")
    if not os.path.exists(DATA_PATH):
        print(f"❌ ERROR: Cannot find dataset.csv at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    # Ingesting custom target columns safely
    print("🧹 Cleaning raw corpus columns using resume parser utils...")
    df['cleaned_resume'] = df['Resume'].apply(clean_resume_text)

    X = df['cleaned_resume']
    y = df['Category']

    # Stratified test splitter
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ⚡ Building unified Machine Learning Pipeline...
    print("⚡ Building unified Machine Learning Pipeline...")
    model_pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(sublinear_tf=True, stop_words='english', max_features=1500)),
        ('classifier', LogisticRegression(max_iter=1000, C=1.0))
    ])

    # Train the entire pipeline at once
    print("🧠 Training model on resume features...")
    model_pipeline.fit(X_train, y_train)

    # Calculate model accuracy score
    train_acc = model_pipeline.score(X_train, y_train) * 100
    test_acc = model_pipeline.score(X_test, y_test) * 100
    print(f"📊 Training Accuracy: {train_acc:.2f}%")
    print(f"📊 Test Validation Accuracy: {test_acc:.2f}%")

    # Save under the brand-new distinct filename directly in the root backend folder
    BACKEND_DIR = os.path.dirname(ML_DIR)
    OUTPUT_PATH = os.path.join(BACKEND_DIR, "pipeline_model.pkl")
    joblib.dump(model_pipeline, OUTPUT_PATH)

    print(f"🔥 Successfully saved true trained Pipeline to: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_model_training_pipeline()