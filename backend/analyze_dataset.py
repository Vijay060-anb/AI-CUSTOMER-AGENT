from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
)


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

print("\n========================================")
print("AI CUSTOMER SUPPORT DATASET ANALYSIS")
print("========================================\n")

print(f"Loading dataset from:\n{RAW_DATA}\n")

if not RAW_DATA.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{RAW_DATA}"
    )

df = pd.read_csv(RAW_DATA)


# ---------------------------------------------------------
# Basic information
# ---------------------------------------------------------

print("Dataset loaded successfully.\n")

print("Shape:")
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]:,}\n")

print("Columns:")
for column in df.columns:
    print(f" - {column}")


# ---------------------------------------------------------
# Missing values
# ---------------------------------------------------------

print("\n========================================")
print("MISSING VALUES")
print("========================================\n")

missing = df.isnull().sum()

for column, count in missing.items():
    print(f"{column}: {count}")


# ---------------------------------------------------------
# Duplicate rows
# ---------------------------------------------------------

print("\n========================================")
print("DUPLICATES")
print("========================================\n")

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates:,}")


# ---------------------------------------------------------
# Categories
# ---------------------------------------------------------

print("\n========================================")
print("CATEGORIES")
print("========================================\n")

categories = df["category"].value_counts()

print(categories.to_string())


# ---------------------------------------------------------
# Intents
# ---------------------------------------------------------

print("\n========================================")
print("INTENTS")
print("========================================\n")

intents = df["intent"].value_counts()

print(f"Number of unique intents: {df['intent'].nunique()}\n")

print(intents.to_string())


# ---------------------------------------------------------
# Example records
# ---------------------------------------------------------

print("\n========================================")
print("SAMPLE RECORDS")
print("========================================\n")

for index, row in df.head(5).iterrows():

    print(f"Record {index + 1}")
    print("-" * 60)

    print(f"Category : {row['category']}")
    print(f"Intent   : {row['intent']}")
    print(f"Question : {row['instruction']}")
    print(f"Response : {row['response'][:300]}...")

    print()


# ---------------------------------------------------------
# Text statistics
# ---------------------------------------------------------

df["instruction_length"] = (
    df["instruction"]
    .fillna("")
    .astype(str)
    .str.len()
)

df["response_length"] = (
    df["response"]
    .fillna("")
    .astype(str)
    .str.len()
)


print("========================================")
print("TEXT STATISTICS")
print("========================================\n")

print(
    df[
        ["instruction_length", "response_length"]
    ].describe()
)


print("\n========================================")
print("ANALYSIS COMPLETE")
print("========================================\n")