import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Find the CSV file
data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found inside the data folder.")

csv_files = csv_files[0]

# Load dataset
df = pd.read_csv(csv_files)

# Separate input and target
x = df["text"]
y = df["label"]

# Split into training and testing data
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Display results
print("=" * 50)
print("TRAIN / TEST SPLIT")
print("=" * 50)

print(f"Total emails: {len(df)}")
print(f"Training emails: {len(x_train)}")
print(f"Testing emails: {len(x_test)}")

print("\nTraining class distribution:")
print(y_train.value_counts(normalize=True) * 100)

print("\nTesting class distribution:")
print(y_test.value_counts(normalize=True) * 100)