import pandas as pd
import numpy as np

# LOAD BASE DATASET
df = pd.read_csv("dataset/improved_dataset.csv")

print("Before shape:", df.shape)

# ADD STRONG NOISE
for col in df.columns:
    if col != "stress_level":
        df[col] = df[col] + np.random.normal(0, 2.0, size=len(df))

# MIX FEATURES (strong mixing)
df["anxiety"] = df["anxiety"] * np.random.uniform(0.6, 1.4, len(df))
df["fatigue_level"] = df["fatigue_level"] * np.random.uniform(0.6, 1.4, len(df))
df["sleep_hours"] = df["sleep_hours"] * np.random.uniform(0.7, 1.3, len(df))
df["screen_time"] = df["screen_time"] * np.random.uniform(0.7, 1.3, len(df))

# CLIP VALUES
df["heart_rate"] = df["heart_rate"].clip(60, 120)
df["bp_sys"] = df["bp_sys"].clip(90, 140)
df["bp_dia"] = df["bp_dia"].clip(60, 90)
df["sleep_hours"] = df["sleep_hours"].clip(3, 10)

cols_1_10 = [
    "fatigue_level", "physical_activity", "screen_time",
    "work_pressure", "study_pressure", "anxiety",
    "mood_swings", "concentration_level"
]

for col in cols_1_10:
    df[col] = df[col].clip(1, 10)

# FIX DATA QUALITY
df["headache_frequency"] = df["headache_frequency"].apply(
    lambda x: 1 if x >= 0.5 else 0
)

# Slight bias reduction
df["fatigue_level"] -= np.random.uniform(0, 1.5, len(df))
df["anxiety"] -= np.random.uniform(0, 1.5, len(df))

df["fatigue_level"] = df["fatigue_level"].clip(1, 10)
df["anxiety"] = df["anxiety"].clip(1, 10)

# ADD LABEL NOISE (STRONGER)-
flip_idx = np.random.choice(df.index, size=int(0.10 * len(df)), replace=False)

df.loc[flip_idx, "stress_level"] = np.random.choice([0, 1, 2], size=len(flip_idx))


# ROUND + SHUFFLE
df = df.round(2)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# SAVE
df.to_csv("dataset/improved_dataset.csv", index=False)

print(" Improved dataset saved!")
print("After shape:", df.shape)