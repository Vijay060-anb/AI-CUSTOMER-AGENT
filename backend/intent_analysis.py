from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "train.csv"
)


print("\n========================================")
print("CUSTOMER SUPPORT INTENT ANALYSIS")
print("========================================\n")


if not TRAIN_FILE.exists():
    raise FileNotFoundError(
        f"Training dataset not found:\n{TRAIN_FILE}\n\n"
        "Run prepare_dataset.py first."
    )


df = pd.read_csv(TRAIN_FILE)


print(f"Training records: {len(df):,}")
print(f"Unique categories: {df['category'].nunique()}")
print(f"Unique intents: {df['intent'].nunique()}")


print("\n========================================")
print("CATEGORY → INTENT MAP")
print("========================================\n")


for category in sorted(df["category"].unique()):

    category_df = df[df["category"] == category]

    print(f"\n{category}")
    print("-" * 50)

    intents = (
        category_df["intent"]
        .value_counts()
        .sort_index()
    )

    for intent, count in intents.items():
        print(f"  {intent:<35} {count:,}")


print("\n========================================")
print("INTENT EXAMPLES")
print("========================================\n")


for intent in sorted(df["intent"].unique()):

    examples = (
        df[df["intent"] == intent]
        ["instruction"]
        .head(3)
        .tolist()
    )

    print(f"\n[{intent}]")

    for number, example in enumerate(examples, start=1):
        print(f"  {number}. {example}")


print("\n========================================")
print("ANALYSIS COMPLETE")
print("========================================\n")