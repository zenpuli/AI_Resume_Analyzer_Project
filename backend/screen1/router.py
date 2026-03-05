from fastapi import APIRouter
from pydantic import BaseModel
from utils.job_skill_loader import get_skills_for_role
from screen1.skill_gap_simple import analyze_skill_gap

router = APIRouter(prefix="/screen1", tags=["Manual Role Analysis"])


class Screen1Request(BaseModel):
    user_skills: list[str]
    target_role: str


@router.post("/analyze")
def analyze_screen1(data: Screen1Request):
    role = data.target_role.lower()

    required_skills = get_skills_for_role(role)

    if not required_skills:
        return {"error": "Role not found in job_skills.json"}

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