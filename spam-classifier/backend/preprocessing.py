import pandas as pd
import re

from pathlib import Path

# Find the CSV file
data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found inside the data folder.")

csv_files = csv_files[0]

#Load dataset
df = pd.read_csv(csv_files)

#Display sample emails
print("=" * 60)
print("RAM EMAIL TEXT")
print("=" * 60)

for i, text in enumerate(df["text"].head(5)):
    print(f"\nEmail {i + 1}:")
    print(text)
    
def clean_text(text):
    #Handle missing values
    if pd.isna(text):
        return ""
    
    #Convert to string
    text = str(text)
    
    #Convert to lowercase
    text = text.lower()
    
    #Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    
    #Remove leading/trailing whitespace
    text = text.strip()
    
    return text

#Apply cleaning
df["clean_text"] = df["text"].apply(clean_text)

print("\n" + "=" * 60)
print("ORIGINAL VS CLEANED")
print("=" * 60)

for i in range(5):
    print(f"\nEmail {i + 1}")
    
    print("Original:")
    print(df.loc[i, "text"])
    
    print("\nCleaned:")
    print(df.loc[i, "clean_text"])