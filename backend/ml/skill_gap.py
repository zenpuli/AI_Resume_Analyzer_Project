import json
import os
from utils.skill_extractor import extract_skills_from_text


def skill_gap_analysis(resume_text: str, predicted_roles: list):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    JOB_SKILLS_PATH = os.path.join(BASE_DIR, "job_skills.json")

    with open(JOB_SKILLS_PATH, "r", encoding="utf-8") as f:
        job_skills = json.load(f)

    resume_skills = set(extract_skills_from_text(resume_text))

    report = {}

    for role in predicted_roles:
        role = role.lower()

        # fallback if role not found
        if role not in job_skills:
            job_skills[role] = list(resume_skills)[:5]

        required = set(job_skills[role])

        matched = required & resume_skills
        missing = required - resume_skills

        match_percentage = round(
            (len(matched) / len(required)) * 100
        ) if required else 50

        report[role] = {
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "match_percentage": match_percentage
        }

    return report
