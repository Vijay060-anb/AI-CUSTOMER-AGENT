from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SupportAI Evaluation Dashboard",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

EVALUATION_DIR = BASE_DIR / "data" / "evaluation"

REAL_WORLD_FILE = EVALUATION_DIR / "real_world_results.csv"
HYBRID_FILE = EVALUATION_DIR / "hybrid_results.csv"


# =========================================================
# PAGE HEADER
# =========================================================

st.title("🤖 SupportAI — Evaluation Dashboard")

st.markdown(
    """
    **AI Customer Support Agent**

    This dashboard evaluates intent classification,
    confidence, routing decisions, and hybrid AI performance.
    """
)

st.divider()


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_csv(path):
    if not path.exists():
        return None

    return pd.read_csv(path)


real_world_df = load_csv(REAL_WORLD_FILE)
hybrid_df = load_csv(HYBRID_FILE)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def find_column(df, candidates):
    """
    Find the first matching column.
    """

    if df is None:
        return None

    columns = {
        str(column).lower(): column
        for column in df.columns
    }

    for candidate in candidates:
        if candidate.lower() in columns:
            return columns[candidate.lower()]

    return None


def calculate_accuracy(
    df,
    preferred_columns=None
):
    """
    Calculate accuracy using:
    1. preferred correctness column
    2. generic correctness column
    3. expected vs predicted intent
    """

    if df is None or df.empty:
        return None

    if preferred_columns is None:
        preferred_columns = []

    # -----------------------------------------------------
    # Preferred correctness columns
    # -----------------------------------------------------

    for column_name in preferred_columns:

        if column_name not in df.columns:
            continue

        values = df[column_name]

        if values.dtype == bool:
            return float(values.mean())

        converted = (
            values.astype(str)
            .str.lower()
            .map(
                {
                    "true": 1,
                    "false": 0,
                    "1": 1,
                    "0": 0,
                    "yes": 1,
                    "no": 0,
                }
            )
        )

        if converted.notna().any():
            return float(converted.mean())

    # -----------------------------------------------------
    # Generic correctness columns
    # -----------------------------------------------------

    correct_col = find_column(
        df,
        [
            "correct",
            "is_correct",
            "accuracy",
        ],
    )

    if correct_col:

        values = df[correct_col]

        if values.dtype == bool:
            return float(values.mean())

        converted = (
            values.astype(str)
            .str.lower()
            .map(
                {
                    "true": 1,
                    "false": 0,
                    "1": 1,
                    "0": 0,
                    "yes": 1,
                    "no": 0,
                }
            )
        )

        if converted.notna().any():
            return float(converted.mean())

    # -----------------------------------------------------
    # Expected vs predicted
    # -----------------------------------------------------

    expected_col = find_column(
        df,
        [
            "expected_intent",
            "expected",
            "true_intent",
            "actual_intent",
            "ground_truth",
        ],
    )

    predicted_col = find_column(
        df,
        [
            "predicted_intent",
            "predicted",
            "final_intent",
            "hybrid_intent",
            "ml_intent",
            "intent",
        ],
    )

    if expected_col and predicted_col:

        return float(
            (
                df[expected_col].astype(str)
                ==
                df[predicted_col].astype(str)
            ).mean()
        )

    return None


def get_message_column(df):

    return find_column(
        df,
        [
            "message",
            "instruction",
            "customer_message",
            "text",
        ],
    )


def get_expected_column(df):

    return find_column(
        df,
        [
            "expected_intent",
            "expected",
            "true_intent",
            "actual_intent",
            "ground_truth",
        ],
    )


# =========================================================
# CHECK ML DATA
# =========================================================

if real_world_df is None:

    st.error(
        "Could not find the ML evaluation file:\n\n"
        f"{REAL_WORLD_FILE}"
    )

    st.stop()


# =========================================================
# 1. EVALUATION OVERVIEW
# =========================================================

st.header("1. Evaluation Overview")


ml_accuracy = calculate_accuracy(
    real_world_df
)


test_messages = len(
    real_world_df
)


# ---------------------------------------------------------
# Confidence
# ---------------------------------------------------------

confidence_col = find_column(
    real_world_df,
    [
        "confidence",
        "ml_confidence",
        "final_confidence",
    ],
)


if confidence_col:

    confidence_values = pd.to_numeric(
        real_world_df[confidence_col],
        errors="coerce",
    )

    average_confidence = (
        confidence_values.mean()
    )

else:

    average_confidence = None


# ---------------------------------------------------------
# Incorrect count
# ---------------------------------------------------------

if ml_accuracy is not None:

    incorrect_count = round(
        test_messages
        * (1 - ml_accuracy)
    )

else:

    incorrect_count = None


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Test Messages",
        test_messages,
    )


with col2:

    if ml_accuracy is not None:

        st.metric(
            "ML Accuracy",
            f"{ml_accuracy * 100:.2f}%",
        )

    else:

        st.metric(
            "ML Accuracy",
            "N/A",
        )


with col3:

    if average_confidence is not None:

        st.metric(
            "Average Confidence",
            f"{average_confidence * 100:.1f}%",
        )

    else:

        st.metric(
            "Average Confidence",
            "N/A",
        )


with col4:

    if incorrect_count is not None:

        st.metric(
            "Incorrect",
            incorrect_count,
        )

    else:

        st.metric(
            "Incorrect",
            "N/A",
        )


# =========================================================
# 2. HYBRID AI PERFORMANCE
# =========================================================

st.header("2. Hybrid AI Performance")


if (
    hybrid_df is not None
    and not hybrid_df.empty
):

    # IMPORTANT:
    # Hybrid accuracy comes specifically
    # from hybrid_correct.

    hybrid_accuracy = calculate_accuracy(
        hybrid_df,
        preferred_columns=[
            "hybrid_correct"
        ],
    )


    hybrid_messages = len(
        hybrid_df
    )


    # -----------------------------------------------------
    # Routing
    # -----------------------------------------------------

    routing_col = find_column(
        hybrid_df,
        [
            "routing_method",
            "method",
        ],
    )


    if routing_col:

        routing_values = (
            hybrid_df[routing_col]
            .astype(str)
            .str.upper()
        )


        ai_routed = int(
            routing_values.eq("AI").sum()
        )


        ml_routed = int(
            routing_values.eq("ML").sum()
        )

    else:

        ai_routed = None
        ml_routed = None


    # -----------------------------------------------------
    # Hybrid metrics
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Hybrid Test Messages",
            hybrid_messages,
        )


    with col2:

        if hybrid_accuracy is not None:

            st.metric(
                "Hybrid Accuracy",
                f"{hybrid_accuracy * 100:.2f}%",
            )

        else:

            st.metric(
                "Hybrid Accuracy",
                "N/A",
            )


    with col3:

        if ai_routed is not None:

            st.metric(
                "AI Routed",
                ai_routed,
            )

        else:

            st.metric(
                "AI Routed",
                "N/A",
            )


    with col4:

        if ml_routed is not None:

            st.metric(
                "ML Routed",
                ml_routed,
            )

        else:

            st.metric(
                "ML Routed",
                "N/A",
            )


else:

    st.warning(
        "hybrid_results.csv was not found."
    )


# =========================================================
# 3. ML VS HYBRID COMPARISON
# =========================================================

st.header("3. ML vs Hybrid Comparison")


comparison_rows = []


if ml_accuracy is not None:

    comparison_rows.append(
        {
            "System": "ML Classifier",
            "Accuracy": (
                ml_accuracy * 100
            ),
        }
    )


if (
    hybrid_df is not None
    and not hybrid_df.empty
):

    hybrid_accuracy = calculate_accuracy(
        hybrid_df,
        preferred_columns=[
            "hybrid_correct"
        ],
    )


    if hybrid_accuracy is not None:

        comparison_rows.append(
            {
                "System": "Hybrid AI",
                "Accuracy": (
                    hybrid_accuracy * 100
                ),
            }
        )


if comparison_rows:

    comparison_df = pd.DataFrame(
        comparison_rows
    )


    st.bar_chart(
        comparison_df.set_index(
            "System"
        )
    )


    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
    )


else:

    st.warning(
        "Not enough data for comparison."
    )


# =========================================================
# 4. CONFIDENCE ANALYSIS
# =========================================================

st.header("4. Confidence Analysis")


if confidence_col:

    confidence_data = pd.to_numeric(
        real_world_df[
            confidence_col
        ],
        errors="coerce",
    ).dropna()


    if not confidence_data.empty:

        confidence_percent = (
            confidence_data * 100
        )


        confidence_df = pd.DataFrame(
            {
                "Confidence (%)":
                    confidence_percent
            }
        )


        st.line_chart(
            confidence_df
        )


        # -------------------------------------------------
        # Confidence groups
        # -------------------------------------------------

        high_count = int(
            (
                confidence_data >= 0.80
            ).sum()
        )


        medium_count = int(
            (
                (
                    confidence_data >= 0.60
                )
                &
                (
                    confidence_data < 0.80
                )
            ).sum()
        )


        low_count = int(
            (
                confidence_data < 0.60
            ).sum()
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            st.metric(
                "High Confidence",
                high_count,
            )


        with c2:

            st.metric(
                "Medium Confidence",
                medium_count,
            )


        with c3:

            st.metric(
                "Low Confidence",
                low_count,
            )


else:

    st.info(
        "No confidence column was found."
    )


# =========================================================
# 5. INTENT PERFORMANCE
# =========================================================

st.header("5. Intent Performance")


expected_col = get_expected_column(
    real_world_df
)


# For the ML dataset, determine its prediction column.
ml_predicted_col = find_column(
    real_world_df,
    [
        "predicted_intent",
        "ml_intent",
        "final_intent",
        "intent",
    ],
)


if (
    expected_col
    and ml_predicted_col
):

    intent_df = (
        real_world_df.copy()
    )


    intent_df["_correct"] = (
        intent_df[
            expected_col
        ].astype(str)
        ==
        intent_df[
            ml_predicted_col
        ].astype(str)
    )


    intent_summary = (
        intent_df
        .groupby(
            expected_col
        )
        .agg(
            Test_Count=(
                "_correct",
                "count",
            ),
            Correct=(
                "_correct",
                "sum",
            ),
        )
        .reset_index()
    )


    intent_summary[
        "Accuracy (%)"
    ] = (
        intent_summary[
            "Correct"
        ]
        /
        intent_summary[
            "Test_Count"
        ]
        * 100
    )


    intent_summary = (
        intent_summary
        .sort_values(
            "Accuracy (%)"
        )
    )


    st.dataframe(
        intent_summary,
        use_container_width=True,
        hide_index=True,
    )


    st.subheader(
        "Intent Accuracy"
    )


    chart_data = (
        intent_summary[
            [
                expected_col,
                "Accuracy (%)",
            ]
        ]
        .set_index(
            expected_col
        )
    )


    st.bar_chart(
        chart_data
    )


else:

    st.info(
        "Expected and predicted intent columns "
        "were not found."
    )


# =========================================================
# 6. FAILED ML PREDICTIONS
# =========================================================

st.header("6. Failed ML Predictions")


if (
    expected_col
    and ml_predicted_col
):

    failed_ml_df = (
        real_world_df[
            real_world_df[
                expected_col
            ].astype(str)
            !=
            real_world_df[
                ml_predicted_col
            ].astype(str)
        ]
        .copy()
    )

else:

    failed_ml_df = pd.DataFrame()


if failed_ml_df.empty:

    st.success(
        "No incorrect ML predictions found. 🎉"
    )

else:

    message_col = get_message_column(
        failed_ml_df
    )


    display_columns = []


    if message_col:

        display_columns.append(
            message_col
        )


    if expected_col:

        display_columns.append(
            expected_col
        )


    if ml_predicted_col:

        display_columns.append(
            ml_predicted_col
        )


    if "confidence" in failed_ml_df.columns:

        display_columns.append(
            "confidence"
        )


    if "ml_confidence" in failed_ml_df.columns:

        display_columns.append(
            "ml_confidence"
        )


    available_columns = [
        column
        for column in display_columns
        if column in failed_ml_df.columns
    ]


    st.dataframe(
        failed_ml_df[
            available_columns
        ],
        use_container_width=True,
        hide_index=True,
    )


    st.warning(
        f"{len(failed_ml_df)} incorrect "
        "ML prediction(s) require review."
    )


# =========================================================
# 7. HYBRID IMPROVEMENTS
# =========================================================

st.header("7. Hybrid Improvements")


if (
    hybrid_df is not None
    and not hybrid_df.empty
):

    if (
        "fixed_by_hybrid"
        in hybrid_df.columns
    ):

        fixed_values = (
            hybrid_df[
                "fixed_by_hybrid"
            ]
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


        fixed_count = int(
            fixed_values.sum()
        )


        st.metric(
            "Predictions Fixed by Hybrid AI",
            fixed_count,
        )


        fixed_df = hybrid_df[
            fixed_values
        ].copy()


        if not fixed_df.empty:

            st.subheader(
                "Cases Fixed by AI"
            )


            columns_to_show = [
                "message",
                "expected_intent",
                "ml_intent",
                "hybrid_intent",
                "ml_confidence",
                "hybrid_confidence",
            ]


            available_columns = [
                column
                for column in columns_to_show
                if column in fixed_df.columns
            ]


            st.dataframe(
                fixed_df[
                    available_columns
                ],
                use_container_width=True,
                hide_index=True,
            )


        else:

            st.info(
                "No ML errors were fixed by Hybrid AI."
            )


    else:

        st.info(
            "The hybrid evaluation does not contain "
            "a fixed_by_hybrid column."
        )


# =========================================================
# 8. ROUTING ANALYSIS
# =========================================================

st.header("8. Routing Analysis")


if (
    hybrid_df is not None
    and not hybrid_df.empty
):

    method_col = find_column(
        hybrid_df,
        [
            "routing_method",
            "method",
        ],
    )


    if method_col:

        routing_counts = (
            hybrid_df[
                method_col
            ]
            .value_counts()
            .rename_axis(
                "Routing Method"
            )
            .reset_index(
                name="Messages"
            )
        )


        st.dataframe(
            routing_counts,
            use_container_width=True,
            hide_index=True,
        )


        st.bar_chart(
            routing_counts.set_index(
                "Routing Method"
            )
        )


    else:

        st.info(
            "Routing method information was not found."
        )


# =========================================================
# 9. HYBRID EVALUATION DETAILS
# =========================================================

st.header(
    "9. Hybrid Evaluation Details"
)


if (
    hybrid_df is not None
    and not hybrid_df.empty
):

    st.dataframe(
        hybrid_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "Hybrid evaluation data is unavailable."
    )


# =========================================================
# 10. ML EVALUATION DATA
# =========================================================

st.header(
    "10. ML Evaluation Data"
)


with st.expander(
    "View complete ML evaluation dataset"
):

    st.dataframe(
        real_world_df,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SupportAI Evaluation Dashboard · "
    "Python · Machine Learning · AI Routing · "
    "FastAPI · n8n"
)