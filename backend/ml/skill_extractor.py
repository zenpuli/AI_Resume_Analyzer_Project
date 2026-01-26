import re

KNOWN_SKILLS = [
    # Programming
    "python", "java", "kotlin", "c", "c++",

    # Android
    "android studio", "xml", "firebase",
    "mvvm", "room database",

    # Web
    "html", "css", "javascript", "react",
    "node.js",

    # Backend
    "flask", "django", "spring", "hibernate",

    # Databases
    "sql", "mysql", "postgresql",

    # Tools & Concepts
    "git", "rest api", "ui/ux",
    "data structures", "algorithms",
    "system design"
]

def extract_skills(resume_text: str):
    resume_text = resume_text.lower()
    found_skills = set()

    for skill in KNOWN_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", resume_text):
            found_skills.add(skill)

    return found_skills
