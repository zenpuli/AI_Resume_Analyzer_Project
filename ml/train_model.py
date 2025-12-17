import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv('dataset.csv')

X = df['Resume']
y = df['Category']

# -------------------------
# Split data
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------
# Vectorize text
# -------------------------
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# -------------------------
# Train model
# -------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_vect, y_train)

# -------------------------
# Test accuracy
# -------------------------
accuracy = model.score(X_test_vect, y_test)
print(f"Model Accuracy: {accuracy*100:.2f}%")

# -------------------------
# Save model and vectorizer
# -------------------------
with open('job_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully!")
