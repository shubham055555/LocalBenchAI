import json
from pathlib import Path
from statistics import mean


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PERFORMANCE_FILE = (
    BASE_DIR
    / "results"
    / "benchmark_results.json"
)

QUALITY_FILE = (
    BASE_DIR
    / "results"
    / "quality_results.json"
)

REPORT_FILE = (
    BASE_DIR
    / "results"
    / "final_scorecard.json"
)


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# AVERAGE HELPER
# ============================================================

def average(values):

    values = [
        value
        for value in values
        if value is not None
    ]

    if not values:
        return 0

    return mean(values)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("                    LOCALBENCH AI")
    print("                    FINAL SCORECARD")
    print("=" * 80)


    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    performance_results = load_json(
        PERFORMANCE_FILE
    )

    quality_results = load_json(
        QUALITY_FILE
    )


    # --------------------------------------------------------
    # Models
    # --------------------------------------------------------

    models = sorted(
        set(
            item["model"]
            for item in performance_results
        )
    )


    scorecards = []


    # ========================================================
    # MODEL ANALYSIS
    # ========================================================

    for model in models:

        model_performance = [
            item
            for item in performance_results
            if item["model"] == model
        ]

        model_quality = [
            item
            for item in quality_results
            if item["model"] == model
        ]


        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        successful = [
            item
            for item in model_performance
            if item.get("status") == "success"
        ]

        total_requests = len(
            model_performance
        )

        success_rate = (
            len(successful)
            / total_requests
            * 100
            if total_requests > 0
            else 0
        )


        # ----------------------------------------------------
        # Latency
        # ----------------------------------------------------

        latencies = [
            item["latency_seconds"]
            for item in successful
            if item.get("latency_seconds") is not None
        ]

        avg_latency = average(
            latencies
        )


        # ----------------------------------------------------
        # Tokens / second
        # ----------------------------------------------------

        token_rates = [
            item["tokens_per_second"]
            for item in successful
            if item.get("tokens_per_second") is not None
        ]

        avg_tokens_per_second = average(
            token_rates
        )


        # ----------------------------------------------------
        # Generated tokens
        # ----------------------------------------------------

        generated_tokens = [
            item["generated_tokens"]
            for item in successful
            if item.get("generated_tokens") is not None
        ]

        avg_generated_tokens = average(
            generated_tokens
        )


        # ----------------------------------------------------
        # VRAM
        # ----------------------------------------------------

        vram_values = [
            item["vram_after_mb"]
            for item in successful
            if item.get("vram_after_mb") is not None
        ]

        avg_vram = average(
            vram_values
        )


        # ----------------------------------------------------
        # RAM
        # ----------------------------------------------------

        ram_values = [
            item["ram_after_mb"]
            for item in successful
            if item.get("ram_after_mb") is not None
        ]

        avg_ram = average(
            ram_values
        )


        # ----------------------------------------------------
        # Quality
        # ----------------------------------------------------

        quality_scores = [
            item["quality_score"]
            for item in model_quality
            if item.get("quality_score") is not None
        ]

        avg_quality = average(
            quality_scores
        )


        quality_percentage = (
            avg_quality
            / 5
            * 100
        )


        # ----------------------------------------------------
        # Store raw metrics
        # ----------------------------------------------------

        scorecards.append({

            "model": model,

            "total_requests": total_requests,

            "successful_requests": len(
                successful
            ),

            "success_rate": round(
                success_rate,
                2
            ),

            "average_latency_seconds": round(
                avg_latency,
                2
            ),

            "average_tokens_per_second": round(
                avg_tokens_per_second,
                2
            ),

            "average_generated_tokens": round(
                avg_generated_tokens,
                2
            ),

            "average_vram_mb": round(
                avg_vram,
                2
            ),

            "average_ram_mb": round(
                avg_ram,
                2
            ),

            "average_quality_score": round(
                avg_quality,
                2
            ),

            "quality_percentage": round(
                quality_percentage,
                2
            )
        })


    # ========================================================
    # NORMALIZATION
    # ========================================================

    # --------------------------------------------------------
    # Quality
    # --------------------------------------------------------

    for item in scorecards:

        item["quality_component"] = round(
            item["quality_percentage"],
            2
        )


    # --------------------------------------------------------
    # Speed
    #
    # Higher tokens/sec = better
    # --------------------------------------------------------

    max_tokens_per_second = max(
        item["average_tokens_per_second"]
        for item in scorecards
    )


    for item in scorecards:

        if max_tokens_per_second > 0:

            speed_score = (
                item["average_tokens_per_second"]
                / max_tokens_per_second
                * 100
            )

        else:

            speed_score = 0


        item["speed_component"] = round(
            speed_score,
            2
        )


    # --------------------------------------------------------
    # Resource efficiency
    #
    # Lower VRAM = better
    # --------------------------------------------------------

    valid_vram = [
        item["average_vram_mb"]
        for item in scorecards
        if item["average_vram_mb"] > 0
    ]


    if valid_vram:

        min_vram = min(
            valid_vram
        )

        max_vram = max(
            valid_vram
        )

    else:

        min_vram = 0
        max_vram = 0


    for item in scorecards:

        vram = item[
            "average_vram_mb"
        ]


        if max_vram == min_vram:

            resource_score = 100

        elif vram > 0:

            resource_score = (
                (
                    max_vram - vram
                )
                /
                (
                    max_vram - min_vram
                )
                * 100
            )

        else:

            resource_score = 0


        item["resource_component"] = round(
            resource_score,
            2
        )


    # ========================================================
    # FINAL WEIGHTED SCORE
    # ========================================================

    for item in scorecards:

        quality = item[
            "quality_component"
        ]

        speed = item[
            "speed_component"
        ]

        resource = item[
            "resource_component"
        ]


        final_score = (
            quality * 0.50
            +
            speed * 0.30
            +
            resource * 0.20
        )


        item["final_score"] = round(
            final_score,
            2
        )


    # ========================================================
    # RANKING
    # ========================================================

    scorecards.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )


    for rank, item in enumerate(
        scorecards,
        start=1
    ):

        item["rank"] = rank


    # ========================================================
    # WINNERS
    # ========================================================

    best_quality = max(
        scorecards,
        key=lambda x:
        x["quality_percentage"]
    )

    best_speed = max(
        scorecards,
        key=lambda x:
        x["average_tokens_per_second"]
    )

    best_latency = min(
        scorecards,
        key=lambda x:
        x["average_latency_seconds"]
    )

    best_resource = min(
        scorecards,
        key=lambda x:
        x["average_vram_mb"]
    )

    best_overall = scorecards[0]


    # ========================================================
    # PRINT SCORECARD
    # ========================================================

    print()

    print(
        f"{'MODEL':<20}"
        f"{'QUALITY':<12}"
        f"{'TOK/S':<12}"
        f"{'VRAM MB':<12}"
        f"{'LATENCY':<12}"
        f"{'FINAL':<10}"
    )

    print("-" * 80)


    for item in scorecards:

        print(
            f"{item['model']:<20}"
            f"{item['quality_percentage']:<12.1f}"
            f"{item['average_tokens_per_second']:<12.2f}"
            f"{item['average_vram_mb']:<12.0f}"
            f"{item['average_latency_seconds']:<12.2f}"
            f"{item['final_score']:<10.2f}"
        )


    # ========================================================
    # WINNERS
    # ========================================================

    print("\n")
    print("=" * 80)
    print("                       WINNERS")
    print("=" * 80)

    print(
        f"\nBest Quality:"
        f" {best_quality['model']}"
        f" ({best_quality['quality_percentage']:.1f}%)"
    )

    print(
        f"Best Token Throughput:"
        f" {best_speed['model']}"
        f" ({best_speed['average_tokens_per_second']:.2f} tok/s)"
    )

    print(
        f"Best Latency:"
        f" {best_latency['model']}"
        f" ({best_latency['average_latency_seconds']:.2f}s)"
    )

    print(
        f"Best VRAM Efficiency:"
        f" {best_resource['model']}"
        f" ({best_resource['average_vram_mb']:.0f} MB)"
    )

    print(
        f"\nBEST OVERALL:"
        f" {best_overall['model']}"
        f" ({best_overall['final_score']:.2f}/100)"
    )


    # ========================================================
    # WEIGHTS
    # ========================================================

    print("\n")
    print("=" * 80)
    print("                    SCORING WEIGHTS")
    print("=" * 80)

    print(
        "\nQuality:    50%"
    )

    print(
        "Speed:      30%"
    )

    print(
        "Resources:  20%"
    )


    # ========================================================
    # SAVE FINAL REPORT
    # ========================================================

    report = {

        "benchmark": "LocalBench AI",

        "version": "1.0",

        "weights": {
            "quality": 0.50,
            "speed": 0.30,
            "resource": 0.20
        },

        "scorecards": scorecards,

        "winners": {

            "best_quality": best_quality[
                "model"
            ],

            "best_speed": best_speed[
                "model"
            ],

            "best_latency": best_latency[
                "model"
            ],

            "best_resource_efficiency": (
                best_resource["model"]
            ),

            "best_overall": best_overall[
                "model"
            ]
        }
    }


    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )


    print("\n")

    print(
        "Final scorecard saved to:"
    )

    print(
        REPORT_FILE
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()