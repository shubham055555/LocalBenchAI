import json
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RESULTS_FILE = (
    BASE_DIR
    / "results"
    / "benchmark_results.json"
)

RUBRIC_FILE = (
    BASE_DIR
    / "evaluation_rubric.json"
)

OUTPUT_FILE = (
    BASE_DIR
    / "results"
    / "quality_results.json"
)


# ============================================================
# LOAD JSON
# ============================================================

def load_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    return (
        text
        .lower()
        .replace(",", " ")
        .replace(".", " ")
        .replace(":", " ")
        .replace(";", " ")
        .replace("-", " ")
    )


# ============================================================
# CHECK CONCEPT
# ============================================================

def concept_present(answer, concept):

    answer_normalized = normalize_text(answer)

    concept_normalized = normalize_text(concept)

    # Direct phrase match
    if concept_normalized in answer_normalized:
        return True

    # Word-based fallback
    concept_words = concept_normalized.split()

    if not concept_words:
        return False

    matched_words = sum(
        1
        for word in concept_words
        if word in answer_normalized
    )

    match_ratio = (
        matched_words
        / len(concept_words)
    )

    return match_ratio >= 0.5


# ============================================================
# EVALUATE ANSWER
# ============================================================

def evaluate_answer(
    answer,
    expected_concepts
):

    if not answer:

        return {
            "score": 0,
            "matched_concepts": [],
            "missing_concepts": expected_concepts
        }


    matched = []

    missing = []


    for concept in expected_concepts:

        if concept_present(
            answer,
            concept
        ):

            matched.append(concept)

        else:

            missing.append(concept)


    total_concepts = len(
        expected_concepts
    )

    matched_count = len(matched)


    if total_concepts == 0:

        score = 0

    else:

        score = (
            matched_count
            / total_concepts
        ) * 5


    return {
        "score": round(score, 2),
        "matched_concepts": matched,
        "missing_concepts": missing
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("                 LOCALBENCH AI")
    print("                 QUALITY EVALUATOR")
    print("=" * 70)


    # --------------------------------------------------------
    # Load files
    # --------------------------------------------------------

    results = load_json(
        RESULTS_FILE
    )

    rubric = load_json(
        RUBRIC_FILE
    )


    # --------------------------------------------------------
    # Create rubric lookup
    # --------------------------------------------------------

    rubric_lookup = {
        item["question_id"]: item
        for item in rubric
    }


    quality_results = []


    # --------------------------------------------------------
    # Evaluate every model answer
    # --------------------------------------------------------

    for result in results:

        question_id = result[
            "question_id"
        ]

        model = result[
            "model"
        ]

        answer = result.get(
            "answer"
        )


        rubric_item = rubric_lookup.get(
            question_id
        )


        if rubric_item is None:

            print(
                f"WARNING: No rubric for "
                f"Question {question_id}"
            )

            continue


        evaluation = evaluate_answer(
            answer,
            rubric_item[
                "expected_concepts"
            ]
        )


        quality_result = {

            "model": model,

            "question_id": question_id,

            "question": result[
                "question"
            ],

            "answer": answer,

            "quality_score": evaluation[
                "score"
            ],

            "max_score": 5,

            "matched_concepts": evaluation[
                "matched_concepts"
            ],

            "missing_concepts": evaluation[
                "missing_concepts"
            ]
        }


        quality_results.append(
            quality_result
        )


        print(
            f"\nModel: {model}"
        )

        print(
            f"Question: {question_id}"
        )

        print(
            f"Quality: "
            f"{evaluation['score']}/5"
        )


    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            quality_results,
            file,
            indent=2,
            ensure_ascii=False
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n")

    print("=" * 70)
    print("                    QUALITY SUMMARY")
    print("=" * 70)


    models = sorted(
        set(
            item["model"]
            for item in quality_results
        )
    )


    for model in models:

        model_results = [
            item
            for item in quality_results
            if item["model"] == model
        ]


        if model_results:

            average_score = (
                sum(
                    item["quality_score"]
                    for item in model_results
                )
                / len(model_results)
            )

        else:

            average_score = 0


        percentage = (
            average_score
            / 5
            * 100
        )


        print(
            f"{model:<20}"
            f" {average_score:.2f}/5"
            f"  ({percentage:.1f}%)"
        )


    print("\n")

    print(
        "Quality results saved to:"
    )

    print(
        OUTPUT_FILE
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()