import pandas as pd
import numpy as np

# LOAD BOTH DATASETS

med = pd.read_csv("data/SaYoPillow.csv")
psy = pd.read_csv("data/StressLevelDataset.csv")

print("Medical columns:", med.columns.tolist())
print("Psychological columns:", psy.columns.tolist())

# CLEAN MEDICAL DATA

# We only need heart rate (hr) and stress level (sl)
med = med[["hr", "sl"]].copy()
med.columns = ["heart_rate", "stress_level"]
med = med.dropna()

# 0,1 → Low(0)   2 → Medium(1)   3,4 → High(2)
def convert_stress(val):
    if val <= 1:
        return 0
    elif val == 2:
        return 1
    else:
        return 2

med["stress_level"] = med["stress_level"].apply(convert_stress)

print("\nMedical after conversion:")
print(med["stress_level"].value_counts())

# CLEAN PSYCHOLOGICAL DATA

psy_cols = [
    "anxiety_level",
    "sleep_quality",
    "fatigue_level", 
    "headache",
    "physical_activity",
    "study_load",
    "future_career_concerns",
    "social_support",         
    "peer_pressure",           
    "depression",              
    "stress_level"
]

#  Only keep columns that actually exist
existing = [c for c in psy_cols if c in psy.columns]
print("\nUsing psychological columns:", existing)

psy = psy[existing].copy()
psy = psy.dropna()

print("\nPsychological stress distribution:")
print(psy["stress_level"].value_counts())


def add_medical_cols(df):
    rows = []
    for _, row in df.iterrows():
        s = row["stress_level"]
        if s == 0:   # Low stress
            bp_sys  = np.random.randint(90, 120)
            bp_dia  = np.random.randint(60, 80)
            screen  = np.random.randint(1, 5)
        elif s == 1: # Medium stress
            bp_sys  = np.random.randint(115, 140)
            bp_dia  = np.random.randint(75, 90)
            screen  = np.random.randint(4, 7)
        else:        # High stress
            bp_sys  = np.random.randint(135, 170)
            bp_dia  = np.random.randint(85, 105)
            screen  = np.random.randint(6, 10)

        rows.append({
            "bp_sys":       bp_sys,
            "bp_dia":       bp_dia,
            "screen_time":  screen
        })
    extra = pd.DataFrame(rows)
    return pd.concat([df.reset_index(drop=True),
                      extra.reset_index(drop=True)], axis=1)

# MERGE BY STRESS LEVEL

def merge_by_stress(med_df, psy_df, stress_val, n_rows):

    m = med_df[med_df["stress_level"] == stress_val].sample(
        n=n_rows, replace=True, random_state=42
    ).reset_index(drop=True)

    p = psy_df[psy_df["stress_level"] == stress_val].sample(
        n=n_rows, replace=True, random_state=42
    ).reset_index(drop=True)

    # Remove stress_level from both — add once at end
    m = m.drop("stress_level", axis=1)
    p = p.drop("stress_level", axis=1)

    combined = pd.concat([m, p], axis=1)
    combined["stress_level"] = stress_val
    return combined

low    = merge_by_stress(med, psy, 0, 2500)
medium = merge_by_stress(med, psy, 1, 2500)
high   = merge_by_stress(med, psy, 2, 2500)

final = pd.concat([low, medium, high], ignore_index=True)

# ADD MISSING COLUMNS

final = add_medical_cols(final)

# Shuffle rows
final = final.sample(frac=1, random_state=42).reset_index(drop=True)

# RENAME TO MATCH YOUR FOR

final = final.rename(columns={
    "sleep_quality":          "sleep_hours",
    "headache":               "headache_frequency",
    "physical_activity":      "physical_activity",
    "study_load":             "study_pressure",
    "future_career_concerns": "work_pressure",
    "social_support":         "mood_swings",
    "peer_pressure":          "concentration_level",
    "depression":             "anxiety_level_2"
})

# VERIFY FINAL DATASET

print("\n=== FINAL DATASET ===")
print("Shape:", final.shape)
print("Columns:", final.columns.tolist())
print("\nStress distribution:")
print(final["stress_level"].value_counts())
print("\nMissing values:")
print(final.isnull().sum())
print("\nFirst 3 rows:")
print(final.head(3))

# SAVE

final.to_csv("dataset/new_stress_dataset.csv", index=False)
print("\nDone! Saved to dataset/new_stress_dataset.csv")