import joblib
import os

ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "pipeline_model.pkl")

def predict_top_3_roles(resume_text: str):
    if not os.path.exists(MODEL_PATH):
        return [{"role": "Missing pipeline_model.pkl binary asset", "confidence": 0.0}]
    
    try:
        # Load your integrated pipeline
        model = joblib.load(MODEL_PATH)
        
        # ⚡ Pass raw text array straight in — the Pipeline vectorizer handles it perfectly now!
        probabilities = model.predict_proba([resume_text])[0]
        classes = model.classes_
        
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        return [
            {"role": str(role), "confidence": round(float(conf * 100), 2)}
            for role, conf in role_probs[:3]
        ]
    except Exception as e:
        print(f"💥 MODEL PIPELINE CRASH: {str(e)}")
        return [{"role": f"Model Error: {str(e)}", "confidence": 0.0}]