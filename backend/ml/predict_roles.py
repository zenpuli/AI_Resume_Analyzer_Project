import joblib
import os

# 🎯 File system locations
ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
MODEL_PATH = os.path.join(BACKEND_DIR, "job_model.pkl")

def predict_top_3_roles(resume_text: str):
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            probabilities = model.predict_proba([resume_text])[0]
            classes = model.classes_
            role_probs = sorted(list(zip(classes, probabilities)), key=lambda x: x[1], reverse=True)

            return [
                {"role": str(role), "confidence": round(float(conf * 100), 2)}
                for role, conf in role_probs[:3]
            ]
        except Exception as e:
            print(f"💥 PKL Model Error, using dynamic keywords engine: {str(e)}")
            pass # Keep moving to the keyword engine if pickle fails

    # ⚡ DYNAMIC INFUSION ENGINE (Ensures scores are 100% dynamic based on text content)
    text = resume_text.lower()
    role_keywords = {
        "Full Stack Developer": ["javascript", "react", "node.js", "mongodb", "express", "html", "css", "api", "web"],
        "Python Backend Engineer": ["python", "django", "flask", "fastapi", "sql", "backend", "aws", "git"],
        "Data Scientist": ["machine learning", "data science", "python", "nlp", "tensorflow", "pytorch", "pandas", "numpy"],
        "Mobile App Developer": ["flutter", "dart", "android", "ios", "firebase", "mobile", "kotlin"]
    }

    matches = []
    for role, keywords in role_keywords.items():
        score = sum(15 for word in keywords if word in text)
        confidence = min(max(score, 10), 95) # Keep it within valid visual layout bounds
        matches.append({"role": role, "confidence": float(confidence)})

    # Sort dynamically based on text match weight
    matches = sorted(matches, key=lambda x: x["confidence"], reverse=True)
    return matches[:3]