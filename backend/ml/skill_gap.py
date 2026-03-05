from utils.skill_extractor import extract_skills_from_text
from utils.job_skill_loader import get_skills_for_role


def skill_gap_analysis(resume_text: str, predicted_roles: list):
    resume_skills = set(extract_skills_from_text(resume_text))

    report = {}

    for role in predicted_roles:
        role = role.lower()

        required_skills = get_skills_for_role(role)

        if not required_skills:
            report[role] = {
                "status": "no_skill_mapping"
            }
            continue

        required_set = set(required_skills)

        matched = required_set & resume_skills
        missing = required_set - resume_skills

        match_percentage = round(
            (len(matched) / len(required_set)) * 100
        ) if required_set else 0

        report[role] = {
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "match_percentage": match_percentage
        }

    return report