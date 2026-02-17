import os
import joblib

# Path to the trained pipeline model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "job_model.pkl")

# Load full pipeline (TFIDF + LogisticRegression)
model = joblib.load(MODEL_PATH)


def predict_top_3_roles(resume_text: str):
    # 🚀 DO NOT manually transform — pipeline handles it
    probs = model.predict_proba([resume_text])[0]
    classes = model.classes_

    top_idx = probs.argsort()[::-1][:3]

    results = []
    for i in top_idx:
        results.append({
            "role": classes[i],
            "confidence": round(float(probs[i]) * 100, 2)
        })

    return results
