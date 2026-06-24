import joblib
import os
import sys

# Ensure cross-folder imports resolve smoothly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.resume_parser import clean_resume_text

ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "pipeline_model.pkl")

# Keep memory slot empty at bootup
GLOBAL_MODEL = None

def get_model():
    """
    Lazy loads the machine learning model.
    Loads it from disk ONCE only when called, then caches it in RAM.
    """
    global GLOBAL_MODEL
    if GLOBAL_MODEL is None:
        if os.path.exists(MODEL_PATH):
            print("🧠 [LAZY LOAD] Loading pipeline binary asset into RAM...")
            GLOBAL_MODEL = joblib.load(MODEL_PATH)
        else:
            print("❌ [LAZY LOAD] Core pipeline binary file not found!")
    return GLOBAL_MODEL

def predict_top_3_roles(resume_text: str):
    # Fetch the cached or newly loaded model instance
    model = get_model()
    
    if model is None:
        return [{"role": "web_development", "confidence": 50.0}]
    
    try:
        cleaned = clean_resume_text(resume_text)
        probabilities = model.predict_proba([cleaned])[0]
        classes = model.classes_
        
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        category_map = {
            "Python Backend Engineer": "web_development",
            "Full Stack Developer": "web_development",
            "Web Development": "web_development",
            "Mobile App Developer": "mobile_development",
            "Data Scientist / AI Engineer": "data_science",
            "Data Science": "data_science",
            "Database Administrator": "database_administrator"
        }

        transformed_roles = []
        for role, conf in role_probs[:3]:
            json_key = category_map.get(str(role), str(role).lower().replace(" ", "_"))
            transformed_roles.append({
                "role": json_key, 
                "confidence": round(float(conf * 100), 2)
            })

        return transformed_roles
    except Exception as e:
        print(f"💥 MODEL PIPELINE CRASH: {str(e)}")
        return [{"role": "web_development", "confidence": 75.0}]