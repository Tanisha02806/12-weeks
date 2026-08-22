import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Find the CSV file
data_folder = Path("data")
csv_file = list(data_folder.glob("*.csv"))

if not csv_file:
    raise FileNotFoundError("No CSV file found inside the data folder.")

csv_file = csv_file[0]

# Load the dataset
df = pd.read_csv(csv_file)

# Handle missing text
df["text"] = df["text"].fillna("")

# Separate input and target
x = df["text"]
y = df["label"]

# Train/Test Split
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# learn vocabulary from training data
x_train_tfidf = vectorizer.fit_transform(x_train)

# Transform test data
x_test_tfidf = vectorizer.transform(x_test)

# Display Information
print("=" * 60)
print("TF-IDF INFORMATION")
print("=" * 60)

print(f"Training emails: {len(x_train)}")
print(f"Testing emails: {len(x_test)}")

print(f"\nTraining TF-IDF shape: {x_train_tfidf.shape}")
print(f"\nTesting TF-IDF shape: {x_test_tfidf.shape}")

print(f"\nVocabulary size: {len(vectorizer.vocabulary_)}")

# Inspect a small part of the TF-IDF matrix
print("\n" + "=" * 60)
print("TF-IDF SAMPLE")
print("=" * 60)

print(x_train_tfidf[:3, :10].toarray())