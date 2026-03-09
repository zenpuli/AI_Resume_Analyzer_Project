import re

KNOWN_SKILLS = [
    # Programming
    "python", "java", "c", "c++", "kotlin", "dart",

    # Web
    "html", "css", "javascript", "react", "node.js", "express",

    # Mobile
    "android studio", "flutter", "xml",

    "flutter", "dart", "kotlin", "swift", "android studio", "xcode", "firebase", "retrofit", "mvvm", "bloc", "provider",

    "kotlin", "dart", "flutter", "android studio", "firebase", "xml", "mvvm", "retrofit", "bloc", "provider",

    "react", "angular", "vue", "tailwind css", "bootstrap", "redux", "next.js", "typescript",

    # Backend
    "django", "flask", "fastapi", "spring", "spring boot",

    # Databases
    "sql", "mysql", "postgresql", "mongodb",

    # AI / ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",

    # DevOps / Cloud
    "docker", "kubernetes", "ci/cd", "aws", "azure", "gcp",
    "cloud computing", "linux",

    # Security
    "cryptography", "network security", "ethical hacking",

    # CS Fundamentals
    "data structures", "algorithms", "oops", "system design",

    # Tools
    "git", "firebase", "rest api", "ui/ux"
]

def extract_skills_from_text(text: str):
    text = text.lower()
    found = set()

    for skill in KNOWN_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)

    return sorted(found)
