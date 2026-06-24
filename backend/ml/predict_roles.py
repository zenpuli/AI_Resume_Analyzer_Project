import joblib
import os
import sys

# 🎯 Make sure Python can safely resolve cross-folder imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.resume_parser import clean_resume_text

# Map paths to the backend directory
ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "pipeline_model.pkl")

def predict_top_3_roles(resume_text: str):
    if not os.path.exists(MODEL_PATH):
        print("⚠️ MODEL NOT FOUND: Using safe backend key fallback.")
        return [{"role": "web_development", "confidence": 50.0}]
    
    try:
        model = joblib.load(MODEL_PATH)
        
        # 🎯 THE CRITICAL FIX: Clean the raw input text first so it matches your dataset vocabulary!
        cleaned = clean_resume_text(resume_text)
        
        probabilities = model.predict_proba([cleaned])[0]
        classes = model.classes_
        
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        # 🎯 CATEGORY TRANSFORMATION MAP
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
            # Convert name to match your json keys cleanly, default to lowercase string if missing
            json_key = category_map.get(str(role), str(role).lower().replace(" ", "_"))
            transformed_roles.append({
                "role": json_key, 
                "confidence": round(float(conf * 100), 2)
            })

        return transformed_roles
    except Exception as e:
        print(f"💥 MODEL PIPELINE CRASH: {str(e)}")
        return [{"role": "web_development", "confidence": 75.0}]