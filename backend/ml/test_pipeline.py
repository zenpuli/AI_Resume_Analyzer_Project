from analyze_resume import analyze_resume
import json

resume_text = """
Skills:
Android Development, Kotlin, Java,
XML, Android Studio,
REST APIs, Firebase,
Room Database, MVVM Architecture,
Git, UI/UX Design, Debugging
"""

print("\n===== FULL RESUME ANALYSIS =====\n")

result = analyze_resume(resume_text)

# -----------------------------
# Scores Panel
# -----------------------------
print("=== SCORES ===")
scores = result["scores"]
print(f"Overall Score    : {scores['overall']}/100")
print(f"Skills Score     : {scores['skills']}/100")
print(f"Experience Score : {scores['experience']}/100")
print(f"Education Score  : {scores['education']}/100")
print(f"Formatting Score : {scores['formatting']}/100")

# -----------------------------
# Predicted Job Roles Panel
# -----------------------------
print("\n=== PREDICTED JOB ROLES ===")
for i, role in enumerate(result["predicted_roles"], start=1):
    print(
        f"#{i} {role['role']} | "
        f"{role['match']}% Match | "
        f"Salary: {role['salary']} | "
        f"Demand: {role['demand']}"
    )

# -----------------------------
# Skills Analysis Panel
# -----------------------------
print("\n=== SKILLS ANALYSIS ===")
for role, data in result["skills_analysis"].items():
    print(f"\nRole: {role}")

    if data.get("status") == "no_skill_mapping":
        print("⚠ No predefined skill mapping")
        continue

    print(f"Matched Skills : {data['matched_skills']}")
    print(f"Missing Skills : {data['missing_skills']}")
    print(f"Match %        : {data['match_percentage']}")

# -----------------------------
# Recommendations Panel
# -----------------------------
print("\n=== IMPROVEMENT RECOMMENDATIONS ===")
for rec in result["recommendations"]:
    print(
        f"- {rec['title']} "
        f"[{rec['severity']}] → {rec['reason']}"
    )
