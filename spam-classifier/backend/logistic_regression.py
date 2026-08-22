import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Find the CSV file
data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found inside the data folder.")

csv_file = csv_files[0]

# Load dataset
df = pd.read_csv(csv_file)

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

# TF-IDF
vectorizer = TfidfVectorizer()

x_train_tfidf = vectorizer.fit_transform(x_train)
x_test_tfidf = vectorizer.transform(x_test)

# Create Logistic Regression model
model = LogisticRegression(
    max_iter=1000
)

# Train the model
model.fit(x_train_tfidf, y_train)

print("=" * 60)
print("LOGISTIC REGRESSION TRAINING")
print("=" * 60)

print("Model training completed!")

# Make predictions
y_pred = model.predict(x_test_tfidf)

print("\nFirst 10 predictions:")
print(y_pred[:10])

print("\nFirst 10 actual labels:")
print(y_test.iloc[:10].values)

print("\n" + "=" * 60)
print("PREDICTION COMPARISON")
print("=" * 60)

for i in range(10):
    actual = y_test.iloc[i]
    predicted = y_pred[i]
    
    print(
        f"Email {i + 1}:"
        f"Actual = {actual}, "
        f"Predicted = {predicted}"
    )
    
# Prediction probabilities
probabilities = model.predict_proba(x_test_tfidf)

print("\n" + "=" * 60)
print("PREDICTION PROBABILITIES")
print("=" * 60)

for i in range(10):
    not_spam_probability = probabilities[i][0]
    spam_probability = probabilities[i][1]
    
    print(
        f"Email {i + 1}: "
        f"Not Spam = {not_spam_probability:.4f}, "
        f"Spam = {spam_probability:.4f}"
    )