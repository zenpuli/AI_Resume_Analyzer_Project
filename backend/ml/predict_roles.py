import joblib
import os

# 🎯 FIX: Get the exact directory where this file lives (backend/ml/)
ML_DIR = os.path.dirname(os.path.abspath(__file__))

# Point directly to the binaries inside the same folder
MODEL_PATH = os.path.join(ML_DIR, "job_model.pkl")
VECTORIZER_PATH = os.path.join(ML_DIR, "vectorizer.pkl")

def predict_top_3_roles(resume_text: str):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        return [{"role": "Missing Model or Vectorizer inside ml/ folder", "confidence": 0.0}]
    
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        
        # Transform the raw resume text array using the correct vectorizer steps
        vectorized_text = vectorizer.transform([resume_text])
        
        probabilities = model.predict_proba(vectorized_text)[0]
        classes = model.classes_
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        return [
            {"role": str(role), "confidence": round(float(conf * 100), 2)}
            for role, conf in role_probs[:3]
        ]
    except Exception as e:
        print(f"💥 MODEL INFERENCE CRASH: {str(e)}")
        return [{"role": f"Model Error: {str(e)}", "confidence": 0.0}]