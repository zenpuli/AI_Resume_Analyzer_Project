from fastapi import APIRouter
from pydantic import BaseModel
from utils.resume_parser import extract_text_from_resume
from ml.predict_roles import predict_top_3_roles
from ml.skill_gap import skill_gap_analysis

router = APIRouter(prefix="/screen2", tags=["Resume Analysis"])

class ResumeRequest(BaseModel):
    resume_text: str


@router.post("/analyze")
def analyze_resume(data: ResumeRequest):
    resume_text = data.resume_text

    # 1️⃣ Predict roles from resume
    predicted_roles = predict_top_3_roles(resume_text)

    # Take TOP 3 only
    top_roles = predicted_roles[:3]

    # 2️⃣ Skill gap + score
    report = skill_gap_analysis(
        resume_text=resume_text,
        predicted_roles=top_roles
    )

    results = []

    for role in top_roles:
        role_data = report.get(role, {})

        results.append({
            "role": role,
            "resume_score": role_data.get("match_percentage", 0),
            "confidence": round(role_data.get("match_percentage", 0) / 100, 2),
            "matched_skills": role_data.get("matched_skills", []),
            "missing_skills": role_data.get("missing_skills", [])
        })

    return {
        "top_3_roles": results
    }
