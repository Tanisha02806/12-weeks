import pandas as pd


# Load dataset
df = pd.read_csv("dataset/hr.csv")


# Display first 5 rows
print("\n--- FIRST 5 ROWS ---")
print(df.head())


# Display dataset shape
print("\n--- DATASET SHAPE ---")
print(df.shape)


# Display column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())


# Display data types
print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- ATTRITION DISTRIBUTION ---")
print(df["Attrition"].value_counts())


print("\n--- ATTRITION PERCENTAGE ---")
print(df["Attrition"].value_counts(normalize=True) * 100)

print("\n--- NUMERICAL STATISTICS ---")
print(df.describe())

print("\n--- CATEGORICAL COLUMNS ---")

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

print(categorical_columns.tolist())