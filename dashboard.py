import json
from pathlib import Path

import streamlit as st
import pandas as pd


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

SCORECARD_FILE = (
    BASE_DIR
    / "benchmark"
    / "results"
    / "final_scorecard.json"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LocalBench AI",
    page_icon="LB",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_scorecard():

    with open(
        SCORECARD_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


try:

    report = load_scorecard()

except FileNotFoundError:

    st.error(
        "final_scorecard.json not found."
    )

    st.stop()


scorecards = report[
    "scorecards"
]


df = pd.DataFrame(
    scorecards
)


# ============================================================
# HEADER
# ============================================================

st.title("LocalBench AI")

st.subheader(
    "Local LLM Performance Benchmark Dashboard"
)

st.caption(
    "Benchmark across quality, throughput, latency and GPU memory efficiency."
)


st.divider()


# ============================================================
# WINNERS
# ============================================================

winners = report[
    "winners"
]


st.header("Benchmark Winners")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Best Overall",
        winners["best_overall"]
    )


with col2:

    st.metric(
        "Best Quality",
        winners["best_quality"]
    )


with col3:

    st.metric(
        "Best Speed",
        winners["best_speed"]
    )


with col4:

    st.metric(
        "Best VRAM Efficiency",
        winners["best_resource_efficiency"]
    )


st.divider()


# ============================================================
# MODEL SELECTOR
# ============================================================

st.header("Model Comparison")


selected_models = st.multiselect(
    "Select models",
    options=list(
        df["model"]
    ),
    default=list(
        df["model"]
    )
)


if selected_models:

    filtered_df = df[
        df["model"].isin(
            selected_models
        )
    ]

else:

    filtered_df = df


# ============================================================
# SCORECARD TABLE
# ============================================================

display_df = filtered_df[
    [
        "rank",
        "model",
        "quality_percentage",
        "average_tokens_per_second",
        "average_latency_seconds",
        "average_vram_mb",
        "final_score"
    ]
].copy()


display_df.columns = [
    "Rank",
    "Model",
    "Quality (%)",
    "Tokens/sec",
    "Latency (s)",
    "VRAM (MB)",
    "Final Score"
]


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# CHARTS
# ============================================================

st.header("Performance Comparison")


chart_col1, chart_col2 = st.columns(2)


# ------------------------------------------------------------
# QUALITY
# ------------------------------------------------------------

with chart_col1:

    st.subheader(
        "Quality"
    )

    quality_chart = (
        filtered_df
        .set_index("model")[
            "quality_percentage"
        ]
    )

    st.bar_chart(
        quality_chart,
        y_label="Quality (%)"
    )


# ------------------------------------------------------------
# THROUGHPUT
# ------------------------------------------------------------

with chart_col2:

    st.subheader(
        "Throughput"
    )

    throughput_chart = (
        filtered_df
        .set_index("model")[
            "average_tokens_per_second"
        ]
    )

    st.bar_chart(
        throughput_chart,
        y_label="Tokens / Second"
    )


chart_col3, chart_col4 = st.columns(2)


# ------------------------------------------------------------
# LATENCY
# ------------------------------------------------------------

with chart_col3:

    st.subheader(
        "Latency"
    )

    latency_chart = (
        filtered_df
        .set_index("model")[
            "average_latency_seconds"
        ]
    )

    st.bar_chart(
        latency_chart,
        y_label="Seconds"
    )


# ------------------------------------------------------------
# VRAM
# ------------------------------------------------------------

with chart_col4:

    st.subheader(
        "VRAM Usage"
    )

    vram_chart = (
        filtered_df
        .set_index("model")[
            "average_vram_mb"
        ]
    )

    st.bar_chart(
        vram_chart,
        y_label="VRAM (MB)"
    )


st.divider()


# ============================================================
# OVERALL SCORE
# ============================================================

st.header(
    "Overall Score"
)


overall_chart = (
    filtered_df
    .set_index("model")[
        "final_score"
    ]
)


st.bar_chart(
    overall_chart,
    y_label="Score / 100"
)


st.divider()


# ============================================================
# SCORING METHODOLOGY
# ============================================================

st.header(
    "Scoring Methodology"
)


weights = report[
    "weights"
]


methodology_df = pd.DataFrame(
    {
        "Metric": [
            "Quality",
            "Speed",
            "Resource Efficiency"
        ],
        "Weight": [
            f"{weights['quality'] * 100:.0f}%",
            f"{weights['speed'] * 100:.0f}%",
            f"{weights['resource'] * 100:.0f}%"
        ]
    }
)


st.table(
    methodology_df
)


st.info(
    "Overall score = 50% Quality + "
    "30% Speed + 20% Resource Efficiency."
)


# ============================================================
# BENCHMARK INFO
# ============================================================

st.header(
    "Benchmark Information"
)


info_col1, info_col2, info_col3 = st.columns(3)


with info_col1:

    st.metric(
        "Models Tested",
        len(scorecards)
    )


with info_col2:

    total_requests = sum(
        item["total_requests"]
        for item in scorecards
    )

    st.metric(
        "Total Requests",
        total_requests
    )


with info_col3:

    successful_requests = sum(
        item["successful_requests"]
        for item in scorecards
    )

    st.metric(
        "Successful Requests",
        successful_requests
    )


st.caption(
    "LocalBench AI — Local LLM benchmarking "
    "for resource-constrained systems."
)