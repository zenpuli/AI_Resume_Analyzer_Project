from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

from screen1.skill_gap_simple import analyze_skill_gap

router = APIRouter(prefix="/screen1", tags=["Screen 1"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOB_SKILLS_PATH = os.path.join(BASE_DIR, "job_skills.json")

with open(JOB_SKILLS_PATH, "r", encoding="utf-8") as f:
    JOB_SKILLS = json.load(f)


class Screen1Request(BaseModel):
    user_skills: list[str]
    target_role: str


@router.post("/analyze")
def analyze_screen1(data: Screen1Request):
    role = data.target_role.lower()

    if role not in JOB_SKILLS:
        return {"error": "Role not found in job_skills.json"}

    required_skills = JOB_SKILLS[role]

    analysis = analyze_skill_gap(
        user_skills=data.user_skills,
        required_skills=required_skills
    )

    recommendations = [
        f"Learn {skill} through projects"
        for skill in analysis["missing_skills"]
    ]

    return {
        "role": role,
        "required_skills": required_skills,
        "matched_skills": analysis["matched_skills"],
        "missing_skills": analysis["missing_skills"],
        "match_percentage": analysis["match_percentage"],
        "recommendations": recommendations
    }
