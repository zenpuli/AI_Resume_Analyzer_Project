import joblib
import numpy as np

# Load trained model
MODEL_PATH = "../backend/model/job_model.pkl"
model = joblib.load(MODEL_PATH)

def predict_top_3(resume_text):
    """
    Predict top 3 job roles from resume text
    """
    probabilities = model.predict_proba([resume_text])[0]
    classes = model.classes_

    # Get top 3 indices
    top_indices = np.argsort(probabilities)[-3:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "role": classes[idx],
            "confidence": round(probabilities[idx] * 100, 2)
        })

    return results

# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    sample_resume = """
    Skills: Python, Machine Learning, Pandas, NumPy, NLP,
    TensorFlow, Data Analysis, SQL, Scikit-learn
    """

    predictions = predict_top_3(sample_resume)

    print("\nTop 3 Job Role Predictions:\n")
    for p in predictions:
        print(f"{p['role']} - {p['confidence']}%")
