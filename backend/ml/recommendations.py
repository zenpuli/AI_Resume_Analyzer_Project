def generate_recommendations(skills_report):
    recs = []

    for role, data in skills_report.items():
        if "missing_skills" not in data:
            continue

        for skill in data["missing_skills"]:
            recs.append({
                "title": f"Learn {skill.title()}",
                "severity": "High" if skill in [
                    "system design",
                    "docker",
                    "kubernetes",
                    "machine learning"
                ] else "Medium",
                "reason": f"Required for {role} roles"
            })

    # Remove duplicates
    unique = {rec["title"]: rec for rec in recs}
    return list(unique.values())[:6]
