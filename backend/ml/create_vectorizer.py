import json
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOB_SKILLS_PATH = os.path.join(BASE_DIR, "job_skills.json")

# load job skills
with open(JOB_SKILLS_PATH, "r", encoding="utf-8") as f:
    job_skills = json.load(f)

# create training text from roles + skills
texts = []
for role, skills in job_skills.items():
    combined = role + " " + " ".join(skills)
    texts.append(combined)

vectorizer = TfidfVectorizer(stop_words="english")
vectorizer.fit(texts)

joblib.dump(vectorizer, os.path.join(BASE_DIR, "ml", "tfidf_vectorizer.pkl"))

print("TF-IDF vectorizer created successfully from job_skills.json")
