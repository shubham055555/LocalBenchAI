import json
from pathlib import Path

import matplotlib.pyplot as plt


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RESULTS_DIR = BASE_DIR / "results"

SCORECARD_FILE = (
    RESULTS_DIR / "final_scorecard.json"
)

CHARTS_DIR = (
    RESULTS_DIR / "charts"
)


# ============================================================
# LOAD SCORECARD
# ============================================================

def load_scorecard():

    with open(
        SCORECARD_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# SAVE BAR CHART
# ============================================================

def create_bar_chart(
    models,
    values,
    title,
    ylabel,
    filename
):

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        models,
        values
    )

    plt.title(title)

    plt.ylabel(ylabel)

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    output_path = (
        CHARTS_DIR / filename
    )

    plt.savefig(
        output_path,
        dpi=200
    )

    plt.close()

    print(
        f"Created: {output_path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("                  LOCALBENCH AI")
    print("                  BENCHMARK CHARTS")
    print("=" * 70)


    # --------------------------------------------------------
    # Create directory
    # --------------------------------------------------------

    CHARTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    report = load_scorecard()

    scorecards = report[
        "scorecards"
    ]


    models = [
        item["model"]
        for item in scorecards
    ]


    # ========================================================
    # 1. QUALITY
    # ========================================================

    quality = [
        item[
            "quality_percentage"
        ]
        for item in scorecards
    ]


    create_bar_chart(
        models,
        quality,
        "Model Quality Comparison",
        "Quality (%)",
        "quality_comparison.png"
    )


    # ========================================================
    # 2. TOKENS / SECOND
    # ========================================================

    tokens_per_second = [
        item[
            "average_tokens_per_second"
        ]
        for item in scorecards
    ]


    create_bar_chart(
        models,
        tokens_per_second,
        "Model Throughput Comparison",
        "Tokens / Second",
        "throughput_comparison.png"
    )


    # ========================================================
    # 3. LATENCY
    # ========================================================

    latency = [
        item[
            "average_latency_seconds"
        ]
        for item in scorecards
    ]


    create_bar_chart(
        models,
        latency,
        "Model Latency Comparison",
        "Latency (seconds)",
        "latency_comparison.png"
    )


    # ========================================================
    # 4. VRAM
    # ========================================================

    vram = [
        item[
            "average_vram_mb"
        ]
        for item in scorecards
    ]


    create_bar_chart(
        models,
        vram,
        "GPU Memory Usage Comparison",
        "VRAM (MB)",
        "vram_comparison.png"
    )


    # ========================================================
    # 5. FINAL SCORE
    # ========================================================

    final_scores = [
        item[
            "final_score"
        ]
        for item in scorecards
    ]


    create_bar_chart(
        models,
        final_scores,
        "Overall Model Score",
        "Final Score (/100)",
        "overall_score.png"
    )


    # ========================================================
    # COMPLETE
    # ========================================================

    print()

    print("=" * 70)

    print(
        "All charts generated successfully."
    )

    print()

    print(
        f"Charts directory:\n"
        f"{CHARTS_DIR}"
    )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()