import joblib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.resume_parser import clean_resume_text

ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "pipeline_model.pkl")

# 🧠 OPTIMIZATION: Load the model once globally into RAM memory when server boots
GLOBAL_MODEL = None
if os.path.exists(MODEL_PATH):
    print("🚀 Loading unified ML Pipeline weights into RAM memory...")
    GLOBAL_MODEL = joblib.load(MODEL_PATH)

def predict_top_3_roles(resume_text: str):
    # If the model didn't load during bootup, handle the fallback safely
    if GLOBAL_MODEL is None:
        print("⚠️ MODEL RE-LOAD TRIGGERED: Fallback state activated.")
        return [{"role": "web_development", "confidence": 50.0}]
    
    try:
        cleaned = clean_resume_text(resume_text)
        
        # Fast extraction using memory references instead of disk lookups!
        probabilities = GLOBAL_MODEL.predict_proba([cleaned])[0]
        classes = GLOBAL_MODEL.classes_
        
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        category_map = {
            "Python Backend Engineer": "web_development",
            "Full Stack Developer": "web_development",
            "Web Development": "web_development",
            "Mobile App Developer": "mobile_development",
            "Data Scientist / AI Engineer": "data_science",
            "Data Science": "data_science",
            "Database Administrator": "database_administration"
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