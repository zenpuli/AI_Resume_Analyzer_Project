from ml.predict_roles import predict_top_3_roles
from ml.skill_gap import skill_gap_analysis
from ml.scoring import compute_scores
from ml.recommendations import generate_recommendations
from utils.resume_parser import clean_resume_text
from utils.skill_extractor import extract_skills_from_text

def analyze_resume(resume_text: str):
    # ⚡ FAST CLEANING
    cleaned_text = clean_resume_text(resume_text)
    
    # 🚩 STRICT LIVE VALIDATION (Requires multiple sections to look like a real resume)
    professional_keywords = ["education", "experience", "skills", "projects", "summary", "objective", "intern", "certifications"]
    hits = sum(1 for word in professional_keywords if word in cleaned_text.lower())
    
    print(f"--- [RAILWAY LOG] Length: {len(cleaned_text)}, Keyword Hits: {hits}/8 ---")

    # Reject if it doesn't meet stricter resume layout conditions
    if len(cleaned_text) < 250 or hits < 3:
        return {"error": "The uploaded file is not a valid resume. Please include standard sections like Education, Experience, and Skills."}

    # ⚡ CORE ML COMPONENTS
    resume_skills = extract_skills_from_text(cleaned_text)
    predictions = predict_top_3_roles(cleaned_text)
    
    if not predictions:
        predictions = [{"role": "General Developer", "confidence": 50}]

    predicted_role_names = [p["role"] for p in predictions]
    skills_analysis = skill_gap_analysis(cleaned_text, predicted_role_names)

    scores = compute_scores(cleaned_text, skills_analysis)
    recommendations = generate_recommendations(skills_analysis, cleaned_text)

    # --- DYNAMIC MAPPING ---
    top_role_name = predictions[0]["role"]
    top_role_analysis = skills_analysis.get(top_role_name, {})
    dynamic_missing_skills = top_role_analysis.get("missing_skills", [])

    return {
        "resume_skills": resume_skills,
        "top_3_roles": predictions,
        "missing_skills": dynamic_missing_skills, 
        "scores": scores,
        "recommendations": recommendations
    }