import joblib
import os

# 🎯 Get the 'backend/ml/' directory path
ML_DIR = os.path.dirname(os.path.abspath(__file__))

# 🎯 Go up one level to look directly inside 'backend/' where job_model.pkl lives
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "job_model.pkl")

def predict_top_3_roles(resume_text: str):
    # 🚩 Only check for the model file since vectorizer is bundled inside it!
    if not os.path.exists(MODEL_PATH):
        return [{"role": "Missing job_model.pkl inside backend folder", "confidence": 0.0}]
    
    try:
        model = joblib.load(MODEL_PATH)
        
        # ⚡ Since it's a bundled pipeline model, pass the text straight into it!
        probabilities = model.predict_proba([resume_text])[0]
        classes = model.classes_
        
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        return [
            {"role": str(role), "confidence": round(float(conf * 100), 2)}
            for role, conf in role_probs[:3]
        ]
    except Exception as e:
        print(f"💥 MODEL INFERENCE CRASH: {str(e)}")
        return [{"role": f"Model Error: {str(e)}", "confidence": 0.0}]