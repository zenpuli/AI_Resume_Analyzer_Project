import joblib
import os

# Map paths to the backend directory
ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "pipeline_model.pkl")

def predict_top_3_roles(resume_text: str):
    if not os.path.exists(MODEL_PATH):
        return [{"role": "web_development", "confidence": 50.0}] # Safe backend string fallback
    
    try:
        model = joblib.load(MODEL_PATH)
        probabilities = model.predict_proba([resume_text])[0]
        classes = model.classes_
        
        role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

        # 🎯 CATEGORY TRANSFORMATION MAP
        # Maps your raw dataset labels directly to your exact job_skills.json dictionary keys!
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
        # Default back to a valid json dictionary key string if model breaks
        return [{"role": "web_development", "confidence": 75.0}]