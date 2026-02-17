def analyze_skill_gap(user_skills, required_skills):
    user_set = set(skill.lower() for skill in user_skills)
    required_set = set(skill.lower() for skill in required_skills)

    matched = list(user_set & required_set)
    missing = list(required_set - user_set)

    match_percentage = round(
        (len(matched) / len(required_set)) * 100
    ) if required_set else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_percentage
    }
