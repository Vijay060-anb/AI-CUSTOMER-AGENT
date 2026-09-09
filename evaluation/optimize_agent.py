from pathlib import Path

import pandas as pd


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

EVALUATION_DIR = BASE_DIR / "data" / "evaluation"

HYBRID_FILE = (
    EVALUATION_DIR / "hybrid_results.csv"
)

OUTPUT_FILE = (
    EVALUATION_DIR / "optimization_report.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

if not HYBRID_FILE.exists():

    raise FileNotFoundError(
        f"Evaluation file not found: {HYBRID_FILE}"
    )


df = pd.read_csv(
    HYBRID_FILE
)


print("=" * 70)
print("SUPPORTAI AGENT OPTIMIZATION ANALYSIS")
print("=" * 70)


print(
    f"\nLoaded {len(df)} evaluation messages."
)


# =========================================================
# BASIC VALIDATION
# =========================================================

required_columns = [
    "message",
    "expected_intent",
    "ml_intent",
    "ml_confidence",
    "hybrid_intent",
    "hybrid_confidence",
    "routing_method",
    "ai_used",
    "hybrid_correct",
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    raise ValueError(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )


# =========================================================
# NORMALIZE DATA
# =========================================================

df["ml_confidence"] = pd.to_numeric(
    df["ml_confidence"],
    errors="coerce",
)


df["hybrid_confidence"] = pd.to_numeric(
    df["hybrid_confidence"],
    errors="coerce",
)


df["ai_used"] = (
    df["ai_used"]
    .astype(str)
    .str.lower()
    .map(
        {
            "true": True,
            "false": False,
            "1": True,
            "0": False,
        }
    )
    .fillna(False)
)


df["hybrid_correct"] = (
    df["hybrid_correct"]
    .astype(str)
    .str.lower()
    .map(
        {
            "true": True,
            "false": False,
            "1": True,
            "0": False,
        }
    )
    .fillna(False)
)


# =========================================================
# 1. ML PERFORMANCE
# =========================================================

ml_correct = (
    df["expected_intent"]
    == df["ml_intent"]
)


ml_accuracy = (
    ml_correct.mean()
)


print("\n1. ML PERFORMANCE")
print("-" * 70)

print(
    f"ML Accuracy: "
    f"{ml_accuracy * 100:.2f}%"
)

print(
    f"ML Correct: "
    f"{ml_correct.sum()} / {len(df)}"
)

print(
    f"ML Incorrect: "
    f"{(~ml_correct).sum()}"
)


# =========================================================
# 2. HYBRID PERFORMANCE
# =========================================================

hybrid_accuracy = (
    df["hybrid_correct"].mean()
)


print("\n2. HYBRID AI PERFORMANCE")
print("-" * 70)

print(
    f"Hybrid Accuracy: "
    f"{hybrid_accuracy * 100:.2f}%"
)

print(
    f"Hybrid Correct: "
    f"{df['hybrid_correct'].sum()} / {len(df)}"
)

print(
    f"Hybrid Incorrect: "
    f"{(~df['hybrid_correct']).sum()}"
)


# =========================================================
# 3. IMPROVEMENT
# =========================================================

accuracy_improvement = (
    hybrid_accuracy
    - ml_accuracy
)


print("\n3. ACCURACY IMPROVEMENT")
print("-" * 70)

print(
    f"Absolute Improvement: "
    f"{accuracy_improvement * 100:.2f} percentage points"
)


if ml_accuracy > 0:

    relative_improvement = (
        accuracy_improvement
        / ml_accuracy
        * 100
    )

    print(
        f"Relative Improvement: "
        f"{relative_improvement:.2f}%"
    )


# =========================================================
# 4. AI ROUTING ANALYSIS
# =========================================================

ai_routed = (
    df["routing_method"]
    .astype(str)
    .str.upper()
    .eq("AI")
)


ml_routed = (
    df["routing_method"]
    .astype(str)
    .str.upper()
    .eq("ML")
)


print("\n4. ROUTING ANALYSIS")
print("-" * 70)

print(
    f"ML Routed: "
    f"{ml_routed.sum()}"
)

print(
    f"AI Routed: "
    f"{ai_routed.sum()}"
)

print(
    f"AI Routing Rate: "
    f"{ai_routed.mean() * 100:.2f}%"
)


# =========================================================
# 5. LOW-CONFIDENCE ML CASES
# =========================================================

low_confidence = (
    df[
        df["ml_confidence"] < 0.60
    ]
    .copy()
)


medium_confidence = (
    df[
        (
            df["ml_confidence"] >= 0.60
        )
        &
        (
            df["ml_confidence"] < 0.80
        )
    ]
    .copy()
)


high_confidence = (
    df[
        df["ml_confidence"] >= 0.80
    ]
    .copy()
)


print("\n5. CONFIDENCE ANALYSIS")
print("-" * 70)

print(
    f"High Confidence (>=80%): "
    f"{len(high_confidence)}"
)

print(
    f"Medium Confidence (60-79%): "
    f"{len(medium_confidence)}"
)

print(
    f"Low Confidence (<60%): "
    f"{len(low_confidence)}"
)


# =========================================================
# 6. ML FAILURES
# =========================================================

ml_failures = df[
    ~ml_correct
].copy()


print("\n6. ML FAILURE ANALYSIS")
print("-" * 70)

print(
    f"Total ML failures: "
    f"{len(ml_failures)}"
)


if not ml_failures.empty:

    print(
        "\nCommon ML failure patterns:"
    )

    failure_patterns = (
        ml_failures
        .groupby(
            [
                "expected_intent",
                "ml_intent",
            ]
        )
        .size()
        .reset_index(
            name="count"
        )
        .sort_values(
            "count",
            ascending=False,
        )
    )


    print(
        failure_patterns.to_string(
            index=False
        )
    )


# =========================================================
# 7. HYBRID FIXES
# =========================================================

if "fixed_by_hybrid" in df.columns:

    fixed_values = (
        df["fixed_by_hybrid"]
        .astype(str)
        .str.lower()
        .map(
            {
                "true": True,
                "false": False,
                "1": True,
                "0": False,
            }
        )
        .fillna(False)
    )

else:

    fixed_values = (
        (~ml_correct)
        &
        df["hybrid_correct"]
    )


fixed_count = int(
    fixed_values.sum()
)


print("\n7. HYBRID FIXES")
print("-" * 70)

print(
    f"ML errors fixed by Hybrid AI: "
    f"{fixed_count}"
)


if len(ml_failures) > 0:

    fix_rate = (
        fixed_count
        / len(ml_failures)
        * 100
    )

    print(
        f"ML failure recovery rate: "
        f"{fix_rate:.2f}%"
    )


# =========================================================
# 8. REMAINING HYBRID FAILURES
# =========================================================

remaining_failures = df[
    ~df["hybrid_correct"]
].copy()


print("\n8. REMAINING HYBRID FAILURES")
print("-" * 70)

print(
    f"Remaining failures: "
    f"{len(remaining_failures)}"
)


if not remaining_failures.empty:

    remaining_patterns = (
        remaining_failures
        .groupby(
            [
                "expected_intent",
                "hybrid_intent",
            ]
        )
        .size()
        .reset_index(
            name="count"
        )
        .sort_values(
            "count",
            ascending=False,
        )
    )


    print(
        remaining_patterns.to_string(
            index=False
        )
    )


# =========================================================
# 9. INTENT-LEVEL ANALYSIS
# =========================================================

print("\n9. INTENT-LEVEL PERFORMANCE")
print("-" * 70)


intent_analysis = (
    df
    .groupby("expected_intent")
    .agg(
        test_messages=(
            "expected_intent",
            "count",
        ),
        ml_correct=(
            "ml_intent",
            lambda x: (
                x.values
                ==
                df.loc[
                    x.index,
                    "expected_intent",
                ].values
            ).sum(),
        ),
        hybrid_correct=(
            "hybrid_correct",
            "sum",
        ),
    )
    .reset_index()
)


intent_analysis[
    "ml_accuracy"
] = (
    intent_analysis["ml_correct"]
    /
    intent_analysis["test_messages"]
)


intent_analysis[
    "hybrid_accuracy"
] = (
    intent_analysis["hybrid_correct"]
    /
    intent_analysis["test_messages"]
)


intent_analysis[
    "improvement"
] = (
    intent_analysis["hybrid_accuracy"]
    -
    intent_analysis["ml_accuracy"]
)


intent_analysis = (
    intent_analysis
    .sort_values(
        "improvement",
        ascending=False,
    )
)


print(
    intent_analysis.to_string(
        index=False
    )
)


# =========================================================
# 10. GENERATE OPTIMIZATION RECOMMENDATIONS
# =========================================================

print("\n10. OPTIMIZATION RECOMMENDATIONS")
print("-" * 70)


recommendations = []


# ---------------------------------------------------------
# Recommendation 1
# ---------------------------------------------------------

if len(low_confidence) > 0:

    recommendations.append(
        {
            "priority": "HIGH",
            "area": "Confidence Routing",
            "recommendation": (
                "Continue routing low-confidence "
                "ML predictions to the AI reasoning layer."
            ),
        }
    )


# ---------------------------------------------------------
# Recommendation 2
# ---------------------------------------------------------

if len(ml_failures) > 0:

    recommendations.append(
        {
            "priority": "HIGH",
            "area": "Intent Classification",
            "recommendation": (
                "Add more real-world examples for "
                "the intents involved in ML failures."
            ),
        }
    )


# ---------------------------------------------------------
# Recommendation 3
# ---------------------------------------------------------

if fixed_count > 0:

    recommendations.append(
        {
            "priority": "HIGH",
            "area": "Hybrid Routing",
            "recommendation": (
                "Keep the hybrid ML + AI architecture "
                "because the AI layer successfully "
                "recovers some ML classification errors."
            ),
        }
    )


# ---------------------------------------------------------
# Recommendation 4
# ---------------------------------------------------------

if len(remaining_failures) > 0:

    recommendations.append(
        {
            "priority": "MEDIUM",
            "area": "AI Reasoning",
            "recommendation": (
                "Review remaining hybrid failures "
                "and improve the AI prompt with explicit "
                "intent distinctions."
            ),
        }
    )


# ---------------------------------------------------------
# Recommendation 5
# ---------------------------------------------------------

recommendations.append(
    {
        "priority": "MEDIUM",
        "area": "Evaluation",
        "recommendation": (
            "Expand the real-world evaluation set "
            "with ambiguous, short, and conversational "
            "customer messages."
        ),
    }
)


# ---------------------------------------------------------
# Recommendation 6
# ---------------------------------------------------------

recommendations.append(
    {
        "priority": "LOW",
        "area": "Monitoring",
        "recommendation": (
            "Track intent accuracy, confidence, "
            "AI fallback rate, and failure patterns "
            "after deployment."
        ),
    }
)


recommendations_df = pd.DataFrame(
    recommendations
)


print(
    recommendations_df.to_string(
        index=False
    )
)


# =========================================================
# 11. SAVE OPTIMIZATION REPORT
# =========================================================

recommendations_df.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("\n" + "=" * 70)

print(
    "Optimization report saved to:"
)

print(
    OUTPUT_FILE
)

print("=" * 70)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\nFINAL SUMMARY")
print("-" * 70)

print(
    f"ML Accuracy: "
    f"{ml_accuracy * 100:.2f}%"
)

print(
    f"Hybrid Accuracy: "
    f"{hybrid_accuracy * 100:.2f}%"
)

print(
    f"Accuracy Improvement: "
    f"{accuracy_improvement * 100:.2f} percentage points"
)

print(
    f"AI Routed: "
    f"{ai_routed.sum()}"
)

print(
    f"ML Routed: "
    f"{ml_routed.sum()}"
)

print(
    f"ML Errors Fixed by Hybrid: "
    f"{fixed_count}"
)

print(
    f"Remaining Hybrid Errors: "
    f"{len(remaining_failures)}"
)

print("\nOptimization analysis complete. ✅")