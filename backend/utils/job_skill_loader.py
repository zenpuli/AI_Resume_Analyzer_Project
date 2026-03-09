import json
import os

def get_skills_for_role(role_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "job_skills.json")
    
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            domains = data.get("domains", {})
            # This loop searches through every branch (management, networking, etc.)
            for branch_roles in domains.values():
                if role_name.lower() in branch_roles:
                    return branch_roles[role_name.lower()]
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []