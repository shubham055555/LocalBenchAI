import json
import time
import subprocess
from pathlib import Path

import ollama
import psutil


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODELS = [
    "qwen3:1.7b",
    "phi3:latest",
    "llama3:latest"
]

QUESTIONS_FILE = BASE_DIR / "questions.json"

RESULTS_DIR = BASE_DIR / "results"

RESULTS_FILE = RESULTS_DIR / "benchmark_results.json"


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_questions():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# LOAD EXISTING RESULTS
# ============================================================

def load_existing_results():

    if not RESULTS_FILE.is_file():
        return []

    try:

        with open(
            RESULTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        print(
            "Warning: Could not read existing results."
        )

        return []


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results):

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# GET RAM USAGE
# ============================================================

def get_ram_usage():

    memory = psutil.virtual_memory()

    return {
        "total_mb": round(
            memory.total / (1024 * 1024),
            2
        ),

        "used_mb": round(
            memory.used / (1024 * 1024),
            2
        ),

        "available_mb": round(
            memory.available / (1024 * 1024),
            2
        ),

        "percent": memory.percent
    }


# ============================================================
# GET NVIDIA GPU MEMORY
# ============================================================

def get_gpu_memory():

    try:

        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=memory.used,memory.total",
                "--format=csv,noheader,nounits"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return None

        line = result.stdout.strip().splitlines()[0]

        used, total = line.split(",")

        used_mb = float(used.strip())

        total_mb = float(total.strip())

        return {
            "used_mb": round(
                used_mb,
                2
            ),

            "total_mb": round(
                total_mb,
                2
            ),

            "percent": round(
                (used_mb / total_mb) * 100,
                2
            )
        }

    except (
        FileNotFoundError,
        subprocess.SubprocessError,
        ValueError,
        IndexError
    ):

        return None


# ============================================================
# ASK MODEL + COLLECT METRICS
# ============================================================

def ask_model(model, question):

    # --------------------------------------------------------
    # Memory BEFORE inference
    # --------------------------------------------------------

    ram_before = get_ram_usage()

    vram_before = get_gpu_memory()


    # --------------------------------------------------------
    # Start timer
    # --------------------------------------------------------

    start_time = time.perf_counter()


    # --------------------------------------------------------
    # Call Ollama
    # --------------------------------------------------------

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )


    # --------------------------------------------------------
    # End timer
    # --------------------------------------------------------

    end_time = time.perf_counter()


    # --------------------------------------------------------
    # Basic response
    # --------------------------------------------------------

    answer = response["message"]["content"]

    latency = end_time - start_time


    # --------------------------------------------------------
    # Ollama metrics
    # --------------------------------------------------------

    prompt_tokens = response.get(
        "prompt_eval_count",
        0
    )

    generated_tokens = response.get(
        "eval_count",
        0
    )

    prompt_duration_ns = response.get(
        "prompt_eval_duration",
        0
    )

    generation_duration_ns = response.get(
        "eval_duration",
        0
    )

    total_duration_ns = response.get(
        "total_duration",
        0
    )


    # --------------------------------------------------------
    # Convert durations
    # --------------------------------------------------------

    prompt_duration_seconds = (
        prompt_duration_ns
        / 1_000_000_000
    )

    generation_duration_seconds = (
        generation_duration_ns
        / 1_000_000_000
    )

    total_duration_seconds = (
        total_duration_ns
        / 1_000_000_000
    )


    # --------------------------------------------------------
    # Tokens per second
    # --------------------------------------------------------

    if generation_duration_seconds > 0:

        tokens_per_second = (
            generated_tokens
            / generation_duration_seconds
        )

    else:

        tokens_per_second = 0


    # --------------------------------------------------------
    # Memory AFTER inference
    # --------------------------------------------------------

    ram_after = get_ram_usage()

    vram_after = get_gpu_memory()


    # --------------------------------------------------------
    # RAM difference
    # --------------------------------------------------------

    ram_change_mb = (
        ram_after["used_mb"]
        - ram_before["used_mb"]
    )


    # --------------------------------------------------------
    # VRAM difference
    # --------------------------------------------------------

    if (
        vram_before is not None
        and vram_after is not None
    ):

        vram_change_mb = (
            vram_after["used_mb"]
            - vram_before["used_mb"]
        )

    else:

        vram_change_mb = None


    # --------------------------------------------------------
    # Return metrics
    # --------------------------------------------------------

    return {

        "answer": answer,

        "latency_seconds": round(
            latency,
            3
        ),

        "prompt_tokens": prompt_tokens,

        "generated_tokens": generated_tokens,

        "tokens_per_second": round(
            tokens_per_second,
            2
        ),

        "prompt_duration_seconds": round(
            prompt_duration_seconds,
            3
        ),

        "generation_duration_seconds": round(
            generation_duration_seconds,
            3
        ),

        "total_duration_seconds": round(
            total_duration_seconds,
            3
        ),

        "ram_before_mb": (
            ram_before["used_mb"]
        ),

        "ram_after_mb": (
            ram_after["used_mb"]
        ),

        "ram_change_mb": round(
            ram_change_mb,
            2
        ),

        "ram_percent_before": (
            ram_before["percent"]
        ),

        "ram_percent_after": (
            ram_after["percent"]
        ),

        "vram_before_mb": (
            vram_before["used_mb"]
            if vram_before
            else None
        ),

        "vram_after_mb": (
            vram_after["used_mb"]
            if vram_after
            else None
        ),

        "vram_change_mb": (
            round(
                vram_change_mb,
                2
            )
            if vram_change_mb is not None
            else None
        ),

        "vram_total_mb": (
            vram_after["total_mb"]
            if vram_after
            else None
        ),

        "vram_percent_after": (
            vram_after["percent"]
            if vram_after
            else None
        )
    }


# ============================================================
# CHECK EXISTING RESULT
# ============================================================

def result_exists(
    results,
    model,
    question_id
):

    for result in results:

        if (
            result.get("model") == model
            and result.get("question_id") == question_id
        ):

            return True

    return False


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("             LOCALBENCH AI")
    print("       PERFORMANCE BENCHMARK V2")
    print("=" * 60)


    questions = load_questions()

    results = load_existing_results()


    total_requests = (
        len(MODELS)
        * len(questions)
    )


    print(
        f"\nModels: {len(MODELS)}"
    )

    print(
        f"Questions: {len(questions)}"
    )

    print(
        f"Total requests: {total_requests}"
    )

    print(
        f"Already completed: {len(results)}"
    )

    print()


    # ========================================================
    # MODEL LOOP
    # ========================================================

    for model in MODELS:

        print("=" * 60)

        print(
            f"MODEL: {model}"
        )

        print("=" * 60)


        # ----------------------------------------------------
        # QUESTION LOOP
        # ----------------------------------------------------

        for item in questions:

            question_id = item["id"]

            question = item["question"]


            # ------------------------------------------------
            # Skip existing
            # ------------------------------------------------

            if result_exists(
                results,
                model,
                question_id
            ):

                print(
                    f"SKIPPING → "
                    f"{model} → "
                    f"Question {question_id}"
                )

                continue


            current_number = len(results) + 1


            print(
                f"\n[{current_number}/{total_requests}] "
                f"{model} → "
                f"Question {question_id}"
            )

            print(
                f"Question: {question}"
            )


            # ------------------------------------------------
            # Run model
            # ------------------------------------------------

            try:

                metrics = ask_model(
                    model,
                    question
                )


                result = {

                    "model": model,

                    "question_id": question_id,

                    "question": question,

                    "answer": metrics["answer"],

                    "latency_seconds": (
                        metrics["latency_seconds"]
                    ),

                    "prompt_tokens": (
                        metrics["prompt_tokens"]
                    ),

                    "generated_tokens": (
                        metrics["generated_tokens"]
                    ),

                    "tokens_per_second": (
                        metrics["tokens_per_second"]
                    ),

                    "prompt_duration_seconds": (
                        metrics[
                            "prompt_duration_seconds"
                        ]
                    ),

                    "generation_duration_seconds": (
                        metrics[
                            "generation_duration_seconds"
                        ]
                    ),

                    "total_duration_seconds": (
                        metrics[
                            "total_duration_seconds"
                        ]
                    ),

                    "ram_before_mb": (
                        metrics["ram_before_mb"]
                    ),

                    "ram_after_mb": (
                        metrics["ram_after_mb"]
                    ),

                    "ram_change_mb": (
                        metrics["ram_change_mb"]
                    ),

                    "ram_percent_before": (
                        metrics["ram_percent_before"]
                    ),

                    "ram_percent_after": (
                        metrics["ram_percent_after"]
                    ),

                    "vram_before_mb": (
                        metrics["vram_before_mb"]
                    ),

                    "vram_after_mb": (
                        metrics["vram_after_mb"]
                    ),

                    "vram_change_mb": (
                        metrics["vram_change_mb"]
                    ),

                    "vram_total_mb": (
                        metrics["vram_total_mb"]
                    ),

                    "vram_percent_after": (
                        metrics["vram_percent_after"]
                    ),

                    "status": "success"
                }


                # --------------------------------------------
                # Display metrics
                # --------------------------------------------

                print(
                    f"Latency: "
                    f"{metrics['latency_seconds']:.2f}s"
                )

                print(
                    f"Generated tokens: "
                    f"{metrics['generated_tokens']}"
                )

                print(
                    f"Tokens/sec: "
                    f"{metrics['tokens_per_second']:.2f}"
                )

                print(
                    f"RAM before: "
                    f"{metrics['ram_before_mb']:.0f} MB"
                )

                print(
                    f"RAM after: "
                    f"{metrics['ram_after_mb']:.0f} MB"
                )

                print(
                    f"RAM change: "
                    f"{metrics['ram_change_mb']:.0f} MB"
                )

                if metrics["vram_after_mb"] is not None:

                    print(
                        f"VRAM after: "
                        f"{metrics['vram_after_mb']:.0f} MB"
                    )

                    print(
                        f"VRAM change: "
                        f"{metrics['vram_change_mb']:.0f} MB"
                    )

                else:

                    print(
                        "VRAM: unavailable"
                    )


                print(
                    "Status: SUCCESS"
                )


            # ------------------------------------------------
            # Error handling
            # ------------------------------------------------

            except Exception as error:

                result = {

                    "model": model,

                    "question_id": question_id,

                    "question": question,

                    "answer": None,

                    "latency_seconds": None,

                    "prompt_tokens": None,

                    "generated_tokens": None,

                    "tokens_per_second": None,

                    "prompt_duration_seconds": None,

                    "generation_duration_seconds": None,

                    "total_duration_seconds": None,

                    "ram_before_mb": None,

                    "ram_after_mb": None,

                    "ram_change_mb": None,

                    "ram_percent_before": None,

                    "ram_percent_after": None,

                    "vram_before_mb": None,

                    "vram_after_mb": None,

                    "vram_change_mb": None,

                    "vram_total_mb": None,

                    "vram_percent_after": None,

                    "status": "failed",

                    "error": str(error)
                }


                print(
                    "Status: FAILED"
                )

                print(
                    f"Error: {error}"
                )


            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            results.append(result)


            # ------------------------------------------------
            # Save immediately
            # ------------------------------------------------

            save_results(results)

            print(
                "Result saved."
            )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    successful = sum(
        1
        for result in results
        if result.get("status") == "success"
    )

    failed = sum(
        1
        for result in results
        if result.get("status") == "failed"
    )


    print("\n")

    print("=" * 60)
    print("             BENCHMARK COMPLETE")
    print("=" * 60)

    print(
        f"\nTotal results: "
        f"{len(results)}"
    )

    print(
        f"Successful: "
        f"{successful}"
    )

    print(
        f"Failed: "
        f"{failed}"
    )

    print(
        "\nResults saved to:"
    )

    print(
        RESULTS_FILE
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()