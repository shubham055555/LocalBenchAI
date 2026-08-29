import json
from pathlib import Path
from statistics import mean


BASE_DIR = Path(__file__).resolve().parent

RESULTS_FILE = (
    BASE_DIR
    / "results"
    / "benchmark_results.json"
)


def load_results():

    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def analyze_model(results, model):

    model_results = [
        result
        for result in results
        if result["model"] == model
    ]

    successful = [
        result
        for result in model_results
        if result["status"] == "success"
    ]

    failed = [
        result
        for result in model_results
        if result["status"] == "failed"
    ]

    latencies = [
        result["latency_seconds"]
        for result in successful
        if result["latency_seconds"] is not None
    ]

    if latencies:

        average_latency = mean(latencies)
        minimum_latency = min(latencies)
        maximum_latency = max(latencies)

    else:

        average_latency = None
        minimum_latency = None
        maximum_latency = None

    total = len(model_results)

    success_rate = (
        len(successful) / total * 100
        if total > 0
        else 0
    )

    return {
        "model": model,
        "total": total,
        "successful": len(successful),
        "failed": len(failed),
        "success_rate": success_rate,
        "average_latency": average_latency,
        "minimum_latency": minimum_latency,
        "maximum_latency": maximum_latency
    }


def main():

    results = load_results()

    models = sorted(
        set(
            result["model"]
            for result in results
        )
    )

    print("=" * 80)
    print("                  LOCALBENCH AI")
    print("                  BENCHMARK REPORT")
    print("=" * 80)

    print()

    reports = []

    for model in models:

        report = analyze_model(
            results,
            model
        )

        reports.append(report)

    print(
        f"{'MODEL':<20}"
        f"{'SUCCESS':<10}"
        f"{'RATE':<10}"
        f"{'AVG(s)':<12}"
        f"{'MIN(s)':<12}"
        f"{'MAX(s)':<12}"
    )

    print("-" * 80)

    for report in reports:

        print(
            f"{report['model']:<20}"
            f"{report['successful']:<10}"
            f"{report['success_rate']:<10.1f}"
            f"{report['average_latency']:<12.2f}"
            f"{report['minimum_latency']:<12.2f}"
            f"{report['maximum_latency']:<12.2f}"
        )

    print()

    fastest = min(
        reports,
        key=lambda x: x["average_latency"]
        if x["average_latency"] is not None
        else float("inf")
    )

    print(
        f"Fastest model: "
        f"{fastest['model']}"
    )

    print(
        f"Average latency: "
        f"{fastest['average_latency']:.2f}s"
    )


if __name__ == "__main__":
    main()