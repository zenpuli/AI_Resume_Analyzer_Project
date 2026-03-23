import joblib
import os

# 🎯 THIS IS THE FIX: It looks in the SAME folder as this script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "job_model.pkl")

def predict_top_3_roles(resume_text: str):
    # This print will help us see the path in Render logs if it fails
    if not os.path.exists(MODEL_PATH):
        print(f"❌ MODEL NOT FOUND AT: {MODEL_PATH}")
        return [{"role": "Model not trained yet", "confidence": 0}]
    
    # Load the real model
    model = joblib.load(MODEL_PATH)
    probabilities = model.predict_proba([resume_text])[0]
    classes = model.classes_

    role_probs = list(zip(classes, probabilities))
    role_probs.sort(key=lambda x: x[1], reverse=True)

    return [
        {"role": role, "confidence": round(float(conf * 100), 2)}
        for role, conf in role_probs[:3]
    ]