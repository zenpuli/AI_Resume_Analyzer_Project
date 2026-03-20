from ml.predict_roles import predict_top_3_roles
from ml.skill_gap import skill_gap_analysis
from ml.scoring import compute_scores
from ml.recommendations import generate_recommendations
from utils.resume_parser import clean_resume_text
from utils.skill_extractor import extract_skills_from_text

def analyze_resume(resume_text: str):
    # ⚡ FAST CLEANING: Process only essential text
    cleaned_text = clean_resume_text(resume_text)
    
    # 🚩 IMMEDIATE VALIDATION: Prevents model hanging on invalid files
    professional_keywords = ["education", "experience", "skills", "projects", "summary", "objective", "intern"]
    hits = sum(1 for word in professional_keywords if word in cleaned_text.lower())
    
    if len(cleaned_text) < 150 or hits < 1:
        return {"error": "provide a valid resume"}

    # ⚡ PARALLEL-READY PROCESSING: Only run core ML components
    resume_skills = extract_skills_from_text(cleaned_text)
    predictions = predict_top_3_roles(cleaned_text)
    
    # Speed Optimization: Run skill gap only on predicted roles to save 4-5 seconds
    predicted_role_names = [p["role"] for p in predictions]
    skills_analysis = skill_gap_analysis(cleaned_text, predicted_role_names)

    scores = compute_scores(cleaned_text, skills_analysis)
    recommendations = generate_recommendations(skills_analysis, cleaned_text)

    return {
        "resume_skills": resume_skills,
        "top_3_roles": predictions,
        "skills_analysis": skills_analysis,
        "scores": scores,
        "recommendations": recommendations
    }