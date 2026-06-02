import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("dataset/improved_dataset.csv")

# Features
X = data.drop("stress_level", axis=1)

# Target
y = data["stress_level"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=80,
    max_depth=4,
    min_samples_split=5,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)

print("Model Accuracy:", accuracy)

# Save trained model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")