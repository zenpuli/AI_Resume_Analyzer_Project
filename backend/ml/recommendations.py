def generate_recommendations(skills_report, resume_text):
    recommendations = []
    resume_text = resume_text.lower()

    missing_skills = set()

    for role_data in skills_report.values():
        if "missing_skills" in role_data:
            missing_skills.update(role_data["missing_skills"])

    for skill in missing_skills:
        recommendations.append({
            "title": f"Learn {skill}",
            "severity": "High",
            "reason": f"{skill} is required for your target roles"
        })

    if "project" not in resume_text:
        recommendations.append({
            "title": "Add Projects",
            "severity": "Medium",
            "reason": "Projects improve practical credibility"
        })

    if "intern" not in resume_text:
        recommendations.append({
            "title": "Add Internship Experience",
            "severity": "Medium",
            "reason": "Internships increase job readiness"
        })

    return recommendations
