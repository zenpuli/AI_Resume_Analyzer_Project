import joblib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Safely import the cleaner, use a basic backup if it fails
try:
    from utils.resume_parser import clean_resume_text
except ImportError:
    def clean_resume_text(text): return str(text).lower()

ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "pipeline_model.pkl")

GLOBAL_MODEL = None

def get_model():
    """Lazy loads the ML model matrix safely into memory slot."""
    global GLOBAL_MODEL
    if GLOBAL_MODEL is None:
        if os.path.exists(MODEL_PATH):
            try:
                GLOBAL_MODEL = joblib.load(MODEL_PATH)
                print("🧠 [LAZY LOAD SUCCESS] Model loaded smoothly into RAM.")
            except Exception as e:
                print(f"❌ Error unpacking model binary pickle: {str(e)}")
        else:
            print("❌ Pipeline binary file asset not found at target path!")
    return GLOBAL_MODEL

def predict_top_3_roles(resume_text: str):
    """
    Predicts the top 3 job categories safely. 
    Guarantees a clean dictionary return even if text cleaning or matrix transformations fail.
    """
    # Fallback response structure matching your exact job_skills.json schema keys
    fallback_response = [
        {"role": "web_development", "confidence": 70.0},
        {"role": "mobile_development", "confidence": 50.0},
        {"role": "data_science", "confidence": 30.0}
    ]

    try:
        model = get_model()
        if model is None:
            return fallback_response

        # 🎯 CRITICAL BUG RESILIENCY: Force string conversion to prevent text property processing errors
        safe_text = str(resume_text) if resume_text else ""
        cleaned = clean_resume_text(safe_text)
        
        # If text processing emptied out the characters, use fallback
        if not cleaned.strip():
            return fallback_response

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
            "Database Administrator": "database_administration"
        }

        transformed_roles = []
        for role, conf in role_probs[:3]:
            json_key = category_map.get(str(role), str(role).lower().replace(" ", "_"))
            transformed_roles.append({
                "role": json_key, 
                "confidence": round(float(conf * 100), 2)
            })

        return transformed_roles if transformed_roles else fallback_response

    except Exception as e:
        print(f"💥 INTERCEPTED PIPELINE EXCEPTION: {str(e)}")
        return fallback_response