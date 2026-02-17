import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "../model/job_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_top_3_roles(resume_text):
    probs = model.predict_proba([resume_text])[0]
    classes = model.classes_

    top3_idx = probs.argsort()[-3:][::-1]

    results = []
    for idx in top3_idx:
        results.append({
            "role": classes[idx],
            "confidence": round(probs[idx] * 100, 2)
        })

    return results
