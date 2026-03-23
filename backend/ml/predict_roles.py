import joblib
import os

# 🎯 ATOMIC PATH: Look in the backend root folder
# This goes up one level from 'ml' to 'backend'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "job_model.pkl")

def predict_top_3_roles(resume_text: str):
    if not os.path.exists(MODEL_PATH):
        # We change the name so we KNOW if it found the file
        return [{"role": "Searching Model...", "confidence": 0}]
    
    try:
        model = joblib.load(MODEL_PATH)
        probabilities = model.predict_proba([resume_text])[0]
        classes = model.classes_
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        return [
            {"role": role, "confidence": round(float(conf * 100), 2)}
            for role, conf in role_probs[:3]
        ]
    except Exception as e:
        # If it fails, we show a different number so we know it tried
        return [{"role": "ML Processing", "confidence": 88.88}]