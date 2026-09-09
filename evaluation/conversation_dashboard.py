from pathlib import Path
import json

import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SupportAI Conversation Analytics",
    page_icon="📊",
    layout="wide",
)


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE = (
    BASE_DIR
    / "data"
    / "logs"
    / "agent_interactions.jsonl"
)


# =========================================================
# PAGE HEADER
# =========================================================

st.title(
    "📊 SupportAI — Conversation Analytics"
)

st.markdown(
    """
    **Production-style AI Agent Observability**

    Monitor customer conversations, routing decisions,
    AI fallback usage, confidence, workflow results,
    and human-agent escalations.
    """
)

st.divider()


# =========================================================
# LOAD JSONL
# =========================================================

def load_logs():

    if not LOG_FILE.exists():
        return pd.DataFrame()

    records = []

    with LOG_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:

                record = json.loads(line)

                records.append(record)

            except json.JSONDecodeError:

                continue

    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)


df = load_logs()


# =========================================================
# NO DATA
# =========================================================

if df.empty:

    st.warning(
        "No customer interactions have been logged yet."
    )

    st.info(
        "Send a customer message through SupportAI "
        "and refresh this dashboard."
    )

    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

if "timestamp" in df.columns:

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
    )


for column in [
    "final_confidence",
    "ml_confidence",
    "ai_confidence",
]:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )


# =========================================================
# NORMALIZE BOOLEAN VALUES
# =========================================================

def boolean_series(
    series
):

    return (
        series
        .astype(str)
        .str.lower()
        .isin(
            [
                "true",
                "1",
                "yes",
            ]
        )
    )


if "ai_used" in df.columns:

    ai_used_series = boolean_series(
        df["ai_used"]
    )

else:

    ai_used_series = pd.Series(
        False,
        index=df.index,
    )


if "success" in df.columns:

    success_series = boolean_series(
        df["success"]
    )

else:

    success_series = pd.Series(
        False,
        index=df.index,
    )


# =========================================================
# 1. CONVERSATION OVERVIEW
# =========================================================

st.header(
    "1. Conversation Overview"
)


total_conversations = len(df)


# ---------------------------------------------------------
# Routing
# ---------------------------------------------------------

if "routing_method" in df.columns:

    routing_values = (
        df["routing_method"]
        .astype(str)
        .str.upper()
    )

    ml_count = int(
        routing_values.eq("ML").sum()
    )

    ai_routing_count = int(
        routing_values.eq("AI").sum()
    )

else:

    ml_count = 0
    ai_routing_count = 0


# ---------------------------------------------------------
# AI fallback
# ---------------------------------------------------------

ai_count = int(
    ai_used_series.sum()
)


# ---------------------------------------------------------
# Human escalation
# ---------------------------------------------------------

if "final_intent" in df.columns:

    escalation_count = int(
        df["final_intent"]
        .astype(str)
        .eq(
            "contact_human_agent"
        )
        .sum()
    )

else:

    escalation_count = 0


# ---------------------------------------------------------
# Average confidence
# ---------------------------------------------------------

if "final_confidence" in df.columns:

    confidence_values = (
        df["final_confidence"]
        .dropna()
    )

    if not confidence_values.empty:

        avg_confidence = (
            confidence_values.mean()
        )

    else:

        avg_confidence = None

else:

    avg_confidence = None


# =========================================================
# METRIC CARDS
# =========================================================

c1, c2, c3, c4, c5 = st.columns(
    5
)


with c1:

    st.metric(
        "Conversations",
        total_conversations,
    )


with c2:

    st.metric(
        "AI Fallback",
        ai_count,
    )


with c3:

    st.metric(
        "ML Routed",
        ml_count,
    )


with c4:

    st.metric(
        "Human Escalations",
        escalation_count,
    )


with c5:

    if avg_confidence is not None:

        st.metric(
            "Avg Confidence",
            f"{avg_confidence * 100:.1f}%",
        )

    else:

        st.metric(
            "Avg Confidence",
            "N/A",
        )


# =========================================================
# 2. ROUTING ANALYSIS
# =========================================================

st.header(
    "2. Routing Analysis"
)


if total_conversations > 0:

    ai_fallback_rate = (
        ai_count
        / total_conversations
        * 100
    )

    ml_routing_rate = (
        ml_count
        / total_conversations
        * 100
    )

else:

    ai_fallback_rate = 0
    ml_routing_rate = 0


c1, c2 = st.columns(2)


with c1:

    st.metric(
        "AI Fallback Rate",
        f"{ai_fallback_rate:.1f}%",
    )


with c2:

    st.metric(
        "ML Routing Rate",
        f"{ml_routing_rate:.1f}%",
    )


routing_chart = pd.DataFrame(
    {
        "Routing Method": [
            "ML",
            "AI",
        ],
        "Conversations": [
            ml_count,
            ai_routing_count,
        ],
    }
)


st.bar_chart(
    routing_chart.set_index(
        "Routing Method"
    )
)


# =========================================================
# 3. INTENT DISTRIBUTION
# =========================================================

st.header(
    "3. Intent Distribution"
)


if "final_intent" in df.columns:

    intent_counts = (
        df["final_intent"]
        .astype(str)
        .value_counts()
        .rename_axis(
            "Intent"
        )
        .reset_index(
            name="Conversations"
        )
    )


    st.dataframe(
        intent_counts,
        use_container_width=True,
        hide_index=True,
    )


    st.bar_chart(
        intent_counts.set_index(
            "Intent"
        )
    )

else:

    st.info(
        "Intent information is not available."
    )


# =========================================================
# 4. CONFIDENCE ANALYSIS
# =========================================================

st.header(
    "4. Confidence Analysis"
)


if "final_confidence" in df.columns:

    confidence_data = (
        df[
            [
                "final_confidence"
            ]
        ]
        .dropna()
        .copy()
    )


    if not confidence_data.empty:

        confidence_data[
            "Confidence (%)"
        ] = (
            confidence_data[
                "final_confidence"
            ]
            * 100
        )


        st.line_chart(
            confidence_data[
                [
                    "Confidence (%)"
                ]
            ]
        )


        high_count = int(
            (
                df["final_confidence"]
                >= 0.80
            ).sum()
        )


        medium_count = int(
            (
                (
                    df["final_confidence"]
                    >= 0.60
                )
                &
                (
                    df["final_confidence"]
                    < 0.80
                )
            ).sum()
        )


        low_count = int(
            (
                df["final_confidence"]
                < 0.60
            ).sum()
        )


        c1, c2, c3 = st.columns(
            3
        )


        with c1:

            st.metric(
                "High ≥ 80%",
                high_count,
            )


        with c2:

            st.metric(
                "Medium 60–79%",
                medium_count,
            )


        with c3:

            st.metric(
                "Low < 60%",
                low_count,
            )


else:

    st.info(
        "Confidence information is not available."
    )


# =========================================================
# 5. HUMAN-AGENT ESCALATIONS
# =========================================================

st.header(
    "5. Human-Agent Escalations"
)


if "final_intent" in df.columns:

    escalation_df = df[
        df["final_intent"]
        .astype(str)
        .eq(
            "contact_human_agent"
        )
    ].copy()


    if escalation_df.empty:

        st.success(
            "No human-agent escalations recorded."
        )

    else:

        st.metric(
            "Total Escalations",
            len(escalation_df),
        )


        columns_to_show = [
            "timestamp",
            "customer_name",
            "order_id",
            "message",
            "final_intent",
            "final_confidence",
            "routing_method",
        ]


        available_columns = [
            column
            for column in columns_to_show
            if column in escalation_df.columns
        ]


        st.dataframe(
            escalation_df[
                available_columns
            ],
            use_container_width=True,
            hide_index=True,
        )


else:

    st.info(
        "Escalation information is not available."
    )


# =========================================================
# 6. WORKFLOW SUCCESS
# =========================================================

st.header(
    "6. Workflow Success"
)


successful = int(
    success_series.sum()
)

failed = int(
    (~success_series).sum()
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Successful",
        successful,
    )


with c2:

    st.metric(
        "Failed",
        failed,
    )


with c3:

    if total_conversations > 0:

        success_rate = (
            successful
            / total_conversations
            * 100
        )

        st.metric(
            "Success Rate",
            f"{success_rate:.1f}%",
        )

    else:

        st.metric(
            "Success Rate",
            "N/A",
        )


workflow_chart = pd.DataFrame(
    {
        "Status": [
            "Successful",
            "Failed",
        ],
        "Conversations": [
            successful,
            failed,
        ],
    }
)


st.bar_chart(
    workflow_chart.set_index(
        "Status"
    )
)


# =========================================================
# 7. RECENT CUSTOMER CONVERSATIONS
# =========================================================

st.header(
    "7. Recent Customer Conversations"
)


recent_df = df.copy()


if "timestamp" in recent_df.columns:

    recent_df = (
        recent_df
        .sort_values(
            "timestamp",
            ascending=False,
        )
        .head(20)
    )

else:

    recent_df = (
        recent_df
        .tail(20)
    )


columns_to_show = [
    "timestamp",
    "customer_name",
    "order_id",
    "message",
    "final_intent",
    "final_confidence",
    "routing_method",
    "ai_used",
    "success",
]


available_columns = [
    column
    for column in columns_to_show
    if column in recent_df.columns
]


st.dataframe(
    recent_df[
        available_columns
    ],
    use_container_width=True,
    hide_index=True,
)


# =========================================================
# 8. AI FALLBACK CONVERSATIONS
# =========================================================

st.header(
    "8. Conversations Handled by AI Fallback"
)


if ai_count > 0:

    ai_conversations = df[
        ai_used_series
    ].copy()


    columns_to_show = [
        "timestamp",
        "message",
        "ml_intent",
        "ml_confidence",
        "ai_intent",
        "ai_confidence",
        "final_intent",
        "final_confidence",
    ]


    available_columns = [
        column
        for column in columns_to_show
        if column in ai_conversations.columns
    ]


    st.dataframe(
        ai_conversations[
            available_columns
        ],
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No AI fallback conversations recorded."
    )


# =========================================================
# 9. RAW INTERACTION LOGS
# =========================================================

st.header(
    "9. Raw Interaction Logs"
)


with st.expander(
    "View complete JSONL data"
):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# REFRESH INFORMATION
# =========================================================

st.divider()

st.caption(
    f"Live log source: {LOG_FILE}"
)

st.caption(
    "Refresh the browser to reload the latest "
    "customer interactions."
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SupportAI Conversation Analytics · "
    "AI Agent Observability · "
    "Python · FastAPI · ML · n8n"
)