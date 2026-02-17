import re

KNOWN_SKILLS = [
    # Programming
    "python", "java", "c", "c++", "go",

    # Web
    "html", "css", "javascript", "react", "node.js",

    # Mobile
    "android", "kotlin", "flutter", "dart",

    # Backend
    "flask", "django", "spring", "fastapi",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "firebase",

    # Cloud & DevOps
    "aws", "azure", "docker", "kubernetes", "ci/cd",

    # AI / ML
    "machine learning", "deep learning",
    "tensorflow", "pytorch", "nlp",
    "data analysis", "pandas", "numpy",

    # Security
    "cybersecurity", "ethical hacking",
    "cryptography", "network security",

    # Core CS
    "data structures", "algorithms",
    "oops", "system design",

    # Tools
    "git", "linux", "postman"
]


def extract_skills_from_text(text: str):
    text = text.lower()
    found = set()

    for skill in KNOWN_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)

    return sorted(list(found))
