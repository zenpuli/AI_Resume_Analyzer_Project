# role_normalizer.py

INVALID_ROLES = {
    "job seeker", "student", "fresher",
    "unemployed", "na", "none",
    "irving", "owner", "president", "volunteer"
}

ROLE_MAPPINGS = {
    # ---------------- Python ----------------
    "sr. python developer": "python developer",
    "senior python developer": "python developer",
    "sr python developer": "python developer",

    # ---------------- Java ----------------
    "sr. java developer": "java developer",
    "senior java developer": "java developer",
    "java/j2ee developer": "java developer",
    "sr. java/j2ee developer": "java developer",

    # ---------------- Full Stack ----------------
    "java full stack developer": "full stack java developer",
    "sr. java full stack developer": "full stack java developer",
    "sr. full stack java developer": "full stack java developer",

    # ---------------- Frontend ----------------
    "front end developer": "frontend developer",
    "front-end developer": "frontend developer",
    "front end web developer": "frontend developer",
    "front-end web developer": "frontend developer",
    "senior front end developer": "frontend developer",
    "sr. front end developer": "frontend developer",
    "ui developer": "frontend developer",

    # ---------------- Database ----------------
    "junior database administrator": "database administrator",
    "senior database administrator": "database administrator",
    "sr. database administrator": "database administrator",
    "oracle database administrator": "database administrator",
    "sql database administrator": "database administrator",
    "sql server database administrator": "database administrator",

    # ---------------- Network ----------------
    "network administrator": "network engineer",
    "senior network engineer": "network engineer",

    # ---------------- Security ----------------
    "information security analyst": "security analyst",
    "network security analyst": "security analyst",
    "it security analyst": "security analyst",

    # ---------------- Project Management ----------------
    "it project manager": "project manager",
    "senior project manager": "project manager",
    "technical project manager": "project manager",
}


def normalize_role(role: str):
    role = role.lower().strip()

    if role in INVALID_ROLES:
        return None

    return ROLE_MAPPINGS.get(role, role)
