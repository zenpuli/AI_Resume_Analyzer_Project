from utils.skill_extractor import extract_skills_from_text
from utils.job_skill_loader import get_skills_for_role
import json
import os

# Resolve paths to target job_skills.json accurately
ML_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(ML_DIR)
JSON_PATH = os.path.join(BACKEND_DIR, "job_skills.json")

def skill_gap_analysis(resume_text: str, predicted_roles: list):
    """
    Accepts raw resume text and an array of predicted role dictionaries.
    Extracts nested sub-skills from job_skills.json fields safely.
    """
    resume_skills = set(extract_skills_from_text(resume_text))
    report = {}

    # Load nested file values locally to prevent lookup miss traps
    if not os.path.exists(JSON_PATH):
        return report
        
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        skills_data = json.load(f).get("domains", {})

    for role_item in predicted_roles:
        # Extract the dictionary role string element safely
        role_key = role_item.get("role", "").lower()
        
        # Pull flat skill items out of nested sub-roles (frontend, backend, etc.)
        required_skills = []
        domain_data = skills_data.get(role_key, {})
        
        if isinstance(domain_data, dict):
            for sub_role, skills_list in domain_data.items():
                required_skills.extend(skills_list)
        else:
            required_skills = list(domain_data)

        if not required_skills:
            report[role_key] = {
                "matched_skills": [],
                "missing_skills": [],
                "match_percentage": 0
            }
            continue

        required_set = set(required_skills)
        matched = required_set & resume_skills
        missing = required_set - resume_skills

        match_percentage = round((len(matched) / len(required_set)) * 100) if required_set else 0

        report[role_key] = {
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "match_percentage": match_percentage
        }

    return report