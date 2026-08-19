import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find the CSV file
data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in the 'data' folder.")

csv_file = csv_files[0]

# Load dataset
df = pd.read_csv(csv_file)

# Basic information
print("=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print(f"File: {csv_file.name}")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Column names
print("\n" + "=" * 50)
print("COLUMN NAMES")
print("=" * 50)

print(df.columns.tolist())

# First 5 rows
print("\n" + "=" * 50)
print("FIRST 5 ROWS")
print("=" * 50)

print(df.head())

# Data types
print("\n" + "=" * 50)
print("DATA TYPES")
print("=" * 50)

print(df.dtypes)

# Missing values
print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print(df.isnull().sum())

# Duplicate rows
print("\n" + "=" * 50)
print("DUPLICATE ROWS")
print("=" * 50)

print(f"Number of duplicate rows: {df.duplicated().sum()}")

# Random samples
print("\n" + "=" * 50)
print("RANDOM EMAIL SAMPLES")
print("=" * 50)

print(df.sample(5, random_state=42))

# Class distribution
print("\n" + "=" * 50)
print("CLASS DISTRIBUTION")
print("=" * 50)

print(df['label'].value_counts())

# Class percentages
print("\n" + "=" * 50)
print("CLASS PERCENTAGES")
print("=" * 50)

print(df['label'].value_counts(normalize=True) * 100)

# Visualize class distribution
class_counts = df['label'].value_counts()

class_counts.index = class_counts.index.map({
    0: 'Not Spam',
    1: 'Spam'
})

plt.figure(figsize=(6, 4))

class_counts.plot(kind="bar")

plt.title("Spam vs Not Spam Emails")
plt.xlabel("Email Type")
plt.ylabel("Number of Emails")

plt.xticks(rotation=0)
plt.tight_layout()

plt.show()

