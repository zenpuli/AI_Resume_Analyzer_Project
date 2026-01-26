import re

def compute_skill_score(skills_report):
    percentages = [
        data["match_percentage"]
        for data in skills_report.values()
        if "match_percentage" in data
    ]
    return round(sum(percentages) / len(percentages)) if percentages else 50


def compute_experience_score(resume_text):
    text = resume_text.lower()
    years = re.findall(r"(\d+)\+?\s+years", text)
    years = max(map(int, years)) if years else 0

    senior_keywords = ["lead", "senior", "architect", "managed", "mentor"]
    senior_hits = sum(1 for k in senior_keywords if k in text)

    score = years * 10 + senior_hits * 5
    return min(100, max(40, score))


def compute_education_score(resume_text):
    text = resume_text.lower()
    degree = ["b.tech", "b.e", "bachelor", "m.tech", "mca", "msc"]
    certs = ["certified", "certification", "coursera", "udemy"]

    score = 50
    if any(k in text for k in degree):
        score += 30
    if any(k in text for k in certs):
        score += 20

    return min(100, score)


def compute_formatting_score(resume_text):
    score = 100
    if len(resume_text) < 500:
        score -= 20
    if resume_text.count("\n") < 5:
        score -= 10
    if "@" not in resume_text:
        score -= 15
    return max(50, score)


def compute_scores(resume_text, skills_report):
    skills = compute_skill_score(skills_report)
    experience = compute_experience_score(resume_text)
    education = compute_education_score(resume_text)
    formatting = compute_formatting_score(resume_text)

    overall = round(
        skills * 0.4 +
        experience * 0.25 +
        education * 0.2 +
        formatting * 0.15
    )

    return {
        "overall": overall,
        "skills": skills,
        "experience": experience,
        "education": education,
        "formatting": formatting
    }
