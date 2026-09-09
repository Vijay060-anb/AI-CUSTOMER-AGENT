import csv
import os

from agent.smart_router import classify_message
from agent.hybrid_router import hybrid_classify


# ============================================================
# FILE CONFIGURATION
# ============================================================

INPUT_FILE = "data/evaluation/real_world_test.csv"
OUTPUT_FILE = "data/evaluation/hybrid_results.csv"


# ============================================================
# LOAD TEST DATA
# ============================================================

def load_test_data():
    """
    Load the real-world customer support evaluation dataset.
    """

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Evaluation file not found: {INPUT_FILE}"
        )

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        data = list(reader)

    return data


# ============================================================
# EVALUATION
# ============================================================

def evaluate():

    data = load_test_data()

    ml_correct = 0
    hybrid_correct = 0
    fixed_count = 0

    results = []

    print("=" * 70)
    print("HYBRID AI CUSTOMER SUPPORT EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # PROCESS EVERY TEST MESSAGE
    # --------------------------------------------------------

    for index, row in enumerate(data, start=1):

        message = row["message"]
        expected = row["expected_intent"]

        print()
        print(
            f"Processing {index}/{len(data)}: "
            f"{message}"
        )

        # ====================================================
        # ML-ONLY CLASSIFICATION
        # ====================================================

        ml_result = classify_message(message)

        ml_intent = ml_result["intent"]

        ml_confidence = ml_result["confidence"]

        ml_is_correct = (
            ml_intent == expected
        )

        if ml_is_correct:
            ml_correct += 1

        # ====================================================
        # HYBRID CLASSIFICATION
        # ====================================================

        hybrid_result = hybrid_classify(message)

        hybrid_intent = hybrid_result["final_intent"]

        hybrid_confidence = (
            hybrid_result["final_confidence"]
        )

        hybrid_method = (
            hybrid_result["routing_method"]
        )

        ai_used = (
            hybrid_result["ai_used"]
        )

        hybrid_is_correct = (
            hybrid_intent == expected
        )

        if hybrid_is_correct:
            hybrid_correct += 1

        # ====================================================
        # CHECK WHETHER HYBRID FIXED ML ERROR
        # ====================================================

        fixed_by_hybrid = (
            not ml_is_correct
            and hybrid_is_correct
        )

        if fixed_by_hybrid:
            fixed_count += 1

        # ====================================================
        # SAVE RESULT
        # ====================================================

        results.append(
            {
                "message": message,

                "expected_intent": expected,

                "ml_intent": ml_intent,

                "ml_confidence": round(
                    ml_confidence,
                    4
                ),

                "ml_correct": ml_is_correct,

                "hybrid_intent": hybrid_intent,

                "hybrid_confidence": round(
                    hybrid_confidence,
                    4
                ),

                "routing_method": hybrid_method,

                "ai_used": ai_used,

                "hybrid_correct": hybrid_is_correct,

                "fixed_by_hybrid": fixed_by_hybrid,
            }
        )

        # ----------------------------------------------------
        # SHOW RESULT
        # ----------------------------------------------------

        print(
            f"Expected : {expected}"
        )

        print(
            f"ML       : {ml_intent} "
            f"({ml_confidence:.2%})"
        )

        print(
            f"Hybrid   : {hybrid_intent} "
            f"({hybrid_confidence:.2%})"
        )

        print(
            f"Routing  : {hybrid_method}"
        )

        print(
            f"AI Used  : {ai_used}"
        )

        if fixed_by_hybrid:

            print(
                "RESULT   : FIXED BY AI"
            )

        elif hybrid_is_correct:

            print(
                "RESULT   : CORRECT"
            )

        else:

            print(
                "RESULT   : INCORRECT"
            )

    # ========================================================
    # CALCULATE ACCURACY
    # ========================================================

    total = len(data)

    if total == 0:
        print("No evaluation data found.")
        return

    ml_accuracy = (
        ml_correct / total
    ) * 100

    hybrid_accuracy = (
        hybrid_correct / total
    ) * 100

    improvement = (
        hybrid_accuracy
        - ml_accuracy
    )

    # ========================================================
    # SAVE RESULTS TO CSV
    # ========================================================

    output_directory = os.path.dirname(
        OUTPUT_FILE
    )

    if output_directory:

        os.makedirs(
            output_directory,
            exist_ok=True
        )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = list(
            results[0].keys()
        )

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(results)

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print()
    print("=" * 70)
    print("FINAL EVALUATION RESULTS")
    print("=" * 70)

    print()
    print("ML-ONLY")
    print("-" * 40)

    print(
        f"Correct:  "
        f"{ml_correct}/{total}"
    )

    print(
        f"Accuracy: "
        f"{ml_accuracy:.2f}%"
    )

    print()
    print("HYBRID ML + AI")
    print("-" * 40)

    print(
        f"Correct:  "
        f"{hybrid_correct}/{total}"
    )

    print(
        f"Accuracy: "
        f"{hybrid_accuracy:.2f}%"
    )

    print()
    print("HYBRID IMPROVEMENT")
    print("-" * 40)

    print(
        f"Messages fixed by AI: "
        f"{fixed_count}"
    )

    print(
        f"Accuracy improvement: "
        f"{improvement:+.2f} "
        f"percentage points"
    )

    # ========================================================
    # SHOW FIXED CASES
    # ========================================================

    print()
    print("CASES FIXED BY AI")
    print("-" * 40)

    fixed_cases = [
        result
        for result in results
        if result["fixed_by_hybrid"]
    ]

    if fixed_cases:

        for result in fixed_cases:

            print()
            print(
                f"Customer: "
                f"{result['message']}"
            )

            print(
                f"Expected: "
                f"{result['expected_intent']}"
            )

            print(
                f"ML:      "
                f"{result['ml_intent']}"
            )

            print(
                f"Hybrid:  "
                f"{result['hybrid_intent']}"
            )

    else:

        print(
            "No ML errors were fixed by the hybrid router."
        )

    # ========================================================
    # SHOW REMAINING ERRORS
    # ========================================================

    print()
    print("REMAINING HYBRID ERRORS")
    print("-" * 40)

    remaining_errors = [
        result
        for result in results
        if not result["hybrid_correct"]
    ]

    if remaining_errors:

        for result in remaining_errors:

            print()
            print(
                f"Customer: "
                f"{result['message']}"
            )

            print(
                f"Expected: "
                f"{result['expected_intent']}"
            )

            print(
                f"Hybrid:  "
                f"{result['hybrid_intent']}"
            )

    else:

        print(
            "No hybrid classification errors."
        )

    # ========================================================
    # OUTPUT FILE
    # ========================================================

    print()
    print("=" * 70)

    print(
        f"Results saved to:"
    )

    print(
        f"{OUTPUT_FILE}"
    )

    print("=" * 70)


# ============================================================
# RUN EVALUATION
# ============================================================

if __name__ == "__main__":

    evaluate()