import joblib
import os

# Use the absolute path provided by Render's environment
MODEL_PATH = "/opt/render/project/src/backend/ml/job_model.pkl"

def predict_top_3_roles(resume_text: str):
    # Try the absolute path first, then fallback to local
    if not os.path.exists(MODEL_PATH):
        local_path = os.path.join(os.path.dirname(__file__), "job_model.pkl")
        path_to_use = local_path if os.path.exists(local_path) else None
    else:
        path_to_use = MODEL_PATH

    if not path_to_use:
        return [{"role": "System Initializing...", "confidence": 0}]
    
    try:
        model = joblib.load(path_to_use)
        probabilities = model.predict_proba([resume_text])[0]
        classes = model.classes_
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        return [
            {"role": role, "confidence": round(float(conf * 100), 2)}
            for role, conf in role_probs[:3]
        ]
    except Exception as e:
        print(f"Prediction error: {e}")
        # Different fallback to know if it's working
        return [{"role": "Role Analysis Pending", "confidence": 50}]