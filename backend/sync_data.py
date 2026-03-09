import pandas as pd
import json
import os

# 1. Load JSON and find roles regardless of nesting
def get_all_roles_from_json(data):
    roles = []
    if isinstance(data, dict):
        # If we see a dict, check if its keys are roles or if it has more branches
        for k, v in data.items():
            if isinstance(v, list): # It's a role! (role: [skill1, skill2])
                roles.append(k.lower().strip())
            else: # It's a branch (core_cs, domains, etc.)
                roles.extend(get_all_roles_from_json(v))
    return list(set(roles))

# Load your file
with open('job_skills.json', 'r') as f:
    raw_data = json.load(f)

valid_roles = get_all_roles_from_json(raw_data)

print(f"🔍 Found {len(valid_roles)} roles in JSON: {valid_roles}")

# 2. Load Dataset
df = pd.read_csv('ml/dataset.csv')
original_count = len(df)
print(f"📄 Dataset loaded with {original_count} rows.")

# 3. Clean and Match
df['Category'] = df['Category'].str.lower().str.strip()

# Check for partial matches (e.g., if JSON has 'database engineer' and CSV has 'database administrator')
df_cleaned = df[df['Category'].isin(valid_roles)]

if len(df_cleaned) > 0:
    df_cleaned.to_csv('ml/dataset.csv', index=False)
    print(f"✅ Success! Kept {len(df_cleaned)} rows.")
    print("🚀 Now run: python ml/train_model.py")
else:
    print("❌ Still 0 matches.")
    print(f"Sample roles from your CSV: {df['Category'].unique()[:5].tolist()}")
    print("TIP: Ensure your job_skills.json keys match your CSV Category names exactly!")