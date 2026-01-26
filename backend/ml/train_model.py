import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

from role_normalizer import normalize_role

# -----------------------------
# Load dataset
# -----------------------------
print("Loading dataset...")
df = pd.read_csv("dataset.csv", usecols=["Resume", "Category"])
df.dropna(inplace=True)

# -----------------------------
# Normalize job roles (🔥 CRITICAL)
# -----------------------------
df["Category"] = df["Category"].apply(normalize_role)
df = df[df["Category"].notna()]

# -----------------------------
# 🔥 HARD ROLE WHITELIST (FINAL)
# -----------------------------
GOLD_ROLES = [
    # Core software
    "python developer",
    "java developer",
    "software engineer",
    "full stack developer",
    "frontend developer",
    "backend developer",
    "android developer",
    "ios developer",

    # Data & AI
    "data analyst",
    "data scientist",
    "machine learning engineer",
    "ai engineer",

    # Infra
    "devops engineer",
    "cloud engineer",

    # IT & Security
    "database administrator",
    "system administrator",
    "network engineer",
    "security analyst",

    # QA
    "software tester",
    "automation tester",

    # Management
    "project manager",
    "business analyst",
    "product manager",

    # Design & Support
    "ui/ux designer",
    "technical support engineer"
]

df = df[df["Category"].isin(GOLD_ROLES)]

# -----------------------------
# Filter rare job roles
# -----------------------------
MIN_SAMPLES_PER_ROLE = 40

role_counts = df["Category"].value_counts()
valid_roles = role_counts[role_counts >= MIN_SAMPLES_PER_ROLE].index
df = df[df["Category"].isin(valid_roles)]

print(f"Using {df['Category'].nunique()} canonical job roles")

# -----------------------------
# Safety cap (laptop friendly)
# -----------------------------
MAX_SAMPLES = 50000
if len(df) > MAX_SAMPLES:
    df = df.sample(n=MAX_SAMPLES, random_state=42)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["Resume"],
    df["Category"],
    test_size=0.2,
    random_state=42,
    stratify=df["Category"]
)

# -----------------------------
# Optimized ML pipeline
# -----------------------------
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=7000,
        ngram_range=(1, 1),
        stop_words="english",
        min_df=5,
        max_df=0.9,
        sublinear_tf=True
    )),
    ("clf", LogisticRegression(
        solver="saga",
        max_iter=3000,
        tol=1e-2,
        C=1.2,
        class_weight="balanced",
    ))
])

# -----------------------------
# Train model
# -----------------------------
print("Training model...")
pipeline.fit(X_train, y_train)

# -----------------------------
# Evaluate
# -----------------------------
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy * 100:.2f}%")

# -----------------------------
# Save model
# -----------------------------
os.makedirs("../backend/model", exist_ok=True)
joblib.dump(pipeline, "../backend/model/job_model.pkl")

print("\n✅ Model trained and saved successfully.")
