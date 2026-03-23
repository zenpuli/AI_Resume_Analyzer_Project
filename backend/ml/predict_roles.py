import joblib
import os

# This tells Render: "The model is right here in this same folder"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "job_model.pkl")

def predict_top_3_roles(resume_text: str):
    if not os.path.exists(MODEL_PATH):
        # This will show up in your Render logs if there's a path issue
        print(f"❌ MODEL NOT FOUND AT: {MODEL_PATH}")
        return [{"role": "System Initializing", "confidence": 0}]
    
    model = joblib.load(MODEL_PATH)
    probabilities = model.predict_proba([resume_text])[0]
    classes = model.classes_

    role_probs = list(zip(classes, probabilities))
    role_probs.sort(key=lambda x: x[1], reverse=True)

    return [
        {"role": role, "confidence": round(float(conf * 100), 2)}
        for role, conf in role_probs[:3]
    ]