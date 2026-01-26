ROLE_META = {
    "android developer": {"salary": "$80k-$120k", "demand": "High"},
    "full stack developer": {"salary": "$100k-$150k", "demand": "High"},
    "software engineer": {"salary": "$90k-$140k", "demand": "High"},
}

def enrich_roles(predictions, skills_report):
    enriched = []

    for p in predictions:
        role = p["role"]
        skill_match = skills_report.get(role, {}).get("match_percentage", 50)

        match = round(p["confidence"] * 0.6 + skill_match * 0.4)

        meta = ROLE_META.get(role, {})
        enriched.append({
            "role": role,
            "match": match,
            "salary": meta.get("salary", "N/A"),
            "demand": meta.get("demand", "Medium")
        })

    return enriched
