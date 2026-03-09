import joblib
import os

# Updated to point to the correct model folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "job_model.pkl")

def predict_top_3_roles(resume_text: str):
    if not os.path.exists(MODEL_PATH):
        return [{"role": "Model not trained yet", "confidence": 0}]
    
    model = joblib.load(MODEL_PATH)
    # The pipeline handles the TF-IDF internally
    probabilities = model.predict_proba([resume_text])[0]
    classes = model.classes_

    role_probs = list(zip(classes, probabilities))
    role_probs.sort(key=lambda x: x[1], reverse=True)

    return [
        {"role": role, "confidence": round(float(conf * 100), 2)}
        for role, conf in role_probs[:3]
    ]