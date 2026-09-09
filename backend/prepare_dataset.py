from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

TRAIN_FILE = PROCESSED_DIR / "train.csv"
VALIDATION_FILE = PROCESSED_DIR / "validation.csv"
TEST_FILE = PROCESSED_DIR / "test.csv"


# ============================================================
# SETTINGS
# ============================================================

RANDOM_STATE = 42

TRAIN_SIZE = 0.80
VALIDATION_SIZE = 0.10
TEST_SIZE = 0.10


# ============================================================
# LOAD
# ============================================================

print("\n========================================")
print("PREPARING BITEXT DATASET")
print("========================================\n")

print(f"Reading:\n{RAW_FILE}\n")

if not RAW_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{RAW_FILE}"
    )

df = pd.read_csv(RAW_FILE)

print(f"Original rows: {len(df):,}")
print(f"Original columns: {len(df.columns)}")


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = [
    "flags",
    "instruction",
    "category",
    "intent",
    "response",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# CLEAN TEXT
# ============================================================

text_columns = [
    "flags",
    "instruction",
    "category",
    "intent",
    "response",
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )


# ============================================================
# REMOVE EXACT DUPLICATES
# ============================================================

before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = before_duplicates - len(df)

print(f"\nDuplicates removed: {duplicates_removed:,}")


# ============================================================
# REMOVE INVALID EMPTY TEXT
# ============================================================

before_empty = len(df)

df = df[
    (df["instruction"].str.len() > 0)
    & (df["response"].str.len() > 0)
    & (df["intent"].str.len() > 0)
    & (df["category"].str.len() > 0)
].copy()

empty_removed = before_empty - len(df)

print(f"Invalid/empty rows removed: {empty_removed:,}")


# ============================================================
# RESET INDEX
# ============================================================

df = df.reset_index(drop=True)


# ============================================================
# SPLIT: 80 / 10 / 10
# ============================================================

print("\nCreating stratified train/validation/test split...")


# First:
# 80% train
# 20% temporary

train_df, temp_df = train_test_split(
    df,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=df["intent"],
)


# Split temporary 50/50:
# 10% validation
# 10% test

validation_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=RANDOM_STATE,
    stratify=temp_df["intent"],
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# SAVE
# ============================================================

train_df.to_csv(
    TRAIN_FILE,
    index=False,
)

validation_df.to_csv(
    VALIDATION_FILE,
    index=False,
)

test_df.to_csv(
    TEST_FILE,
    index=False,
)


# ============================================================
# RESULTS
# ============================================================

print("\n========================================")
print("DATASET PREPARATION COMPLETE")
print("========================================\n")

print(f"Total rows      : {len(df):,}")
print(f"Training rows   : {len(train_df):,}")
print(f"Validation rows : {len(validation_df):,}")
print(f"Testing rows    : {len(test_df):,}")


print("\n========================================")
print("INTENT COUNTS")
print("========================================\n")

print(
    df["intent"]
    .value_counts()
    .sort_index()
    .to_string()
)


print("\n========================================")
print("OUTPUT FILES")
print("========================================\n")

print(f"TRAIN:")
print(TRAIN_FILE)

print(f"\nVALIDATION:")
print(VALIDATION_FILE)

print(f"\nTEST:")
print(TEST_FILE)

print("\n========================================")
print("DONE")
print("========================================\n")