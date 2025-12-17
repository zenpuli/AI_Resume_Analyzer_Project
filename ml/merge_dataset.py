# merge_dataset.py
import pandas as pd

# -------------------------
# Step 1: Load CSV files
# -------------------------
people = pd.read_csv("01_people.csv")
abilities = pd.read_csv("02_abilities.csv")
education = pd.read_csv("03_education.csv")
experience = pd.read_csv("04_experience.csv")
person_skills = pd.read_csv("05_person_skills.csv")

# -------------------------
# Step 2: Preprocess and combine text per person
# -------------------------

# Combine abilities
abilities_grouped = abilities.groupby('person_id')['ability'].apply(lambda x: ' '.join(x.astype(str))).reset_index()

# Combine education fields
education_grouped = education.groupby('person_id').apply(lambda df: ' '.join(df.fillna('').astype(str).values.flatten())).reset_index(name='education_text')

# Combine experience fields
experience_grouped = experience.groupby('person_id').apply(lambda df: ' '.join(df.fillna('').astype(str).values.flatten())).reset_index(name='experience_text')

# Combine skills
skills_grouped = person_skills.groupby('person_id')['skill'].apply(lambda x: ' '.join(x.astype(str))).reset_index()

# -------------------------
# Step 3: Merge all into one DataFrame
# -------------------------
merged = people[['person_id', 'name']].merge(abilities_grouped, on='person_id', how='left') \
                                      .merge(education_grouped, on='person_id', how='left') \
                                      .merge(experience_grouped, on='person_id', how='left') \
                                      .merge(skills_grouped, on='person_id', how='left')

# -------------------------
# Step 4: Create 'Resume' and 'Category' columns
# -------------------------
merged['Resume'] = merged[['ability', 'education_text', 'experience_text', 'skill']].fillna('').agg(' '.join, axis=1)
merged['Category'] = merged['name']

# -------------------------
# Step 5: Save final dataset
# -------------------------
merged[['Resume', 'Category']].to_csv('dataset.csv', index=False)
print("dataset.csv created successfully!")
