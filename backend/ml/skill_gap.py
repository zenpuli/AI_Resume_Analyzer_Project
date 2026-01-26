import json
import os
from ml.skill_extractor import extract_skills


def skill_gap_analysis(resume_text: str, predicted_roles: list):
    """
    Performs skill gap analysis between resume skills
    and predefined job role requirements.
    """

    # Absolute path to backend directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    JOB_SKILLS_PATH = os.path.join(BASE_DIR, "job_skills.json")

    # Load job skills safely
    try:
        with open(JOB_SKILLS_PATH, "r", encoding="utf-8") as file:
            job_skills = json.load(file)
    except FileNotFoundError:
        return {
            "error": "job_skills.json not found",
            "expected_path": JOB_SKILLS_PATH
        }
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON format",
            "message": "Please fix job_skills.json"
        }

    # Extract and normalize resume skills
    resume_skills = set(
        skill.lower() for skill in extract_skills(resume_text)
    )

    if not predicted_roles:
        return {
            "warning": "No predicted roles available",
            "resume_skills": sorted(resume_skills)
        }

    report = {}

    for role in predicted_roles:
        role_name = role.lower().strip()

        # If no mapping exists
        if role_name not in job_skills:
            report[role_name] = {
                "status": "no_skill_mapping",
                "message": "No predefined skills for this role"
            }
            continue

        required_skills = set(
            skill.lower() for skill in job_skills[role_name]
        )

        matched_skills = required_skills & resume_skills
        missing_skills = required_skills - resume_skills

        match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100, 2
        ) if required_skills else 0.0

        report[role_name] = {
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills),
            "total_required_skills": len(required_skills),
            "matched_count": len(matched_skills),
            "match_percentage": match_percentage
        }

    return report
