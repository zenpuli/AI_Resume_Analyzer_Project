import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "job_role_model_v1.pkl")

# Load full pipeline model
model = joblib.load(MODEL_PATH)


def predict_top_3_roles(resume_text: str):

    # Directly send raw text (NO manual vectorizing)
    probabilities = model.predict_proba([resume_text])[0]

    classes = model.classes_
    print(model.classes_)

    role_probs = list(zip(classes, probabilities))
    role_probs.sort(key=lambda x: x[1], reverse=True)

    top_3 = role_probs[:3]

    return [
        {
            "role": role,
            "confidence": round(float(confidence * 100), 2)
        }
        for role, confidence in top_3
    ]