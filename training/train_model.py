import pandas as pd
import re
import joblib


from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import cross_val_score


# ----------------------
# 1. Load Dataset
# ----------------------
df = pd.read_csv("UpdatedResumeDataSet.csv")
df = df.dropna(subset=["Resume", "Category"])


# ----------------------
# 2. Normalize Categories
# ----------------------
df["Category"] = df["Category"].str.lower().str.strip()


def normalize_role(role):
    role = role.lower()

    if "python" in role:
        return "python developer"
    if "java" in role:
        return "java developer"
    if "front" in role and "developer" in role:
        return "front end developer"
    if "full" in role and "developer" in role:
        return "full stack developer"
    if "data scientist" in role:
        return "data scientist"
    if "data analyst" in role:
        return "data analyst"
    if "database" in role or "dba" in role:
        return "database administrator"
    if "network" in role:
        return "network engineer"
    if "security" in role:
        return "cyber security"
    if "project manager" in role:
        return "project manager"
    if "business analyst" in role:
        return "business analyst"
    if "software engineer" in role:
        return "software engineer"
    if "software developer" in role:
        return "software developer"
    if "system" in role and "admin" in role:
        return "system administrator"
    if "it support" in role or "support" in role:
        return "it support"

    return "other"

# Reduce 'other' size
other_df = df[df["Category"] == "other"]

if len(other_df) > 5000:
    other_df = other_df.sample(n=5000, random_state=42)

non_other_df = df[df["Category"] != "other"]

df = pd.concat([other_df, non_other_df])
df["Category"] = df["Category"].apply(normalize_role)


# ----------------------
# 3. Remove Small Classes
# ----------------------
min_samples = 50
category_counts = df["Category"].value_counts()
valid_categories = category_counts[category_counts >= min_samples].index
df = df[df["Category"].isin(valid_categories)]

print("\nFinal Total Rows:", len(df))
print("\nFinal Class Distribution:\n")
print(df["Category"].value_counts())
print("\nFinal Category Count:", df["Category"].nunique())


# ----------------------
# 4. Clean Resume Text
# ----------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9#+.]', ' ', text)
    return text


df["clean_resume"] = df["Resume"].apply(clean_text)


# ----------------------
# 5. Train Test Split
# ----------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_resume"],
    df["Category"],
    test_size=0.2,
    random_state=42,
    stratify=df["Category"]
)


# ----------------------
# 6. Build Optimized Pipeline
# ----------------------
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=15000,
        ngram_range=(1, 3),
        stop_words="english",
        min_df=3,
        max_df=0.85,
        sublinear_tf=True
    )),
    ("clf", CalibratedClassifierCV(
        LinearSVC(max_iter=1500, class_weight="balanced"),
        method='sigmoid'
    ))
])

# ----------------------
# 6.5 Cross Validation
# ----------------------
print("\nRunning 5-Fold Cross Validation...")

cv_scores = cross_val_score(
    pipeline,
    df["clean_resume"],
    df["Category"],
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)

print("Cross Validation Scores:", cv_scores)
print("Mean CV Accuracy:", round(cv_scores.mean() * 100, 2), "%")
print("Std Deviation:", round(cv_scores.std() * 100, 2), "%")

# ----------------------
# 7. Train Model
# ----------------------
pipeline.fit(X_train, y_train)


# ----------------------
# 8. Evaluate
# ----------------------
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# ----------------------
# 9. Save Model
# ----------------------
joblib.dump(pipeline, "job_role_model_v3.pkl")

print("\nModel saved as job_role_model_v3.pkl")

def predict_with_confidence(text):
    text = clean_text(text)
    prediction = pipeline.predict([text])[0]
    probabilities = pipeline.predict_proba([text])[0]
    
    confidence = max(probabilities) * 100
    
    print("\nPredicted Role:", prediction)
    print("Confidence:", round(confidence, 2), "%")