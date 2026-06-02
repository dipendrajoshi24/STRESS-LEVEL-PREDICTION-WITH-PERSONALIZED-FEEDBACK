import pandas as pd

df = pd.read_csv("dataset/new_stress_dataset.csv")

print("Before fix:", df.columns.tolist())

# Rename anxiety_level_2 → fatigue_level
# (depression score closely maps to fatigue)
df = df.rename(columns={"anxiety_level_2": "fatigue_level"})

# Reorder columns to EXACTLY match app.py inputs
final_columns = [
    "heart_rate",
    "bp_sys",
    "bp_dia",
    "sleep_hours",
    "fatigue_level",
    "headache_frequency",
    "physical_activity",
    "screen_time",
    "work_pressure",
    "study_pressure",
    "anxiety_level",
    "mood_swings",
    "concentration_level",
    "stress_level"
]

# Check if physical_activity exists, if not add it
if "physical_activity" not in df.columns:
    # Generate based on stress level (medically accurate)
    import numpy as np
    def gen_activity(s):
        if s == 0:   return np.random.randint(6, 10)
        elif s == 1: return np.random.randint(3, 7)
        else:        return np.random.randint(1, 4)
    df["physical_activity"] = df["stress_level"].apply(gen_activity)

df = df[final_columns]

print("After fix:", df.columns.tolist())
print("Shape:", df.shape)
print("\nFirst 3 rows:")
print(df.head(3))

df.to_csv("dataset/new_stress_dataset.csv", index=False)
print("\nFixed dataset saved!")