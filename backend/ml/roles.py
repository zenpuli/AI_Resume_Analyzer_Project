import joblib

model = joblib.load("../backend/model/job_model.pkl")

classes = model.named_steps["clf"].classes_

print(f"Total job roles: {len(classes)}")
print(classes)
