from ml.predict_top3 import predict_top_3
from ml.skill_gap import skill_gap_analysis
from ml.role_enricher import enrich_roles
from ml.scoring import compute_scores
from ml.recommendations import generate_recommendations
from utils.resume_parser import clean_resume_text
from utils.skill_extractor import extract_skills_from_text

def analyze_resume(resume_text: str):
    cleaned = clean_resume_text(resume_text)

    predictions = predict_top_3(cleaned)
    predicted_roles = [p["role"] for p in predictions]

    skills_report = skill_gap_analysis(cleaned, predicted_roles)
    scores = compute_scores(cleaned, skills_report)
    enriched_roles = enrich_roles(predictions, skills_report)
    recommendations = generate_recommendations(skills_report)

    return {
        "score": scores["overall"],
        "skills": extract_skills_from_text(cleaned),
        "missing_skills": sorted({
            s for r in skills_report.values()
            if "missing_skills" in r
            for s in r["missing_skills"]
        }),
        "top_jobs": enriched_roles,
        "recommendations": recommendations
    }
