import json
import ollama
from pydantic import BaseModel, ValidationError


MODEL = "qwen3:1.7b"
MAX_RETRIES = 3


class AIResponse(BaseModel):
    answer: str
    topic: str
    difficulty: str
    confidence: float


def ask_model(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def validate_response(raw_output):
    data = json.loads(raw_output)

    validated = AIResponse.model_validate(data)

    return validated


question = "Explain overfitting in machine learning."

base_prompt = f"""
Answer this question:

{question}

Return ONLY valid JSON in exactly this format:

{{
  "answer": "short explanation",
  "topic": "topic name",
  "difficulty": "beginner/intermediate/advanced",
  "confidence": 0.0
}}

Rules:
- confidence must be between 0 and 1
- difficulty must be one of: beginner, intermediate, advanced
- Do not include markdown
- Do not include any text outside JSON
"""


current_prompt = base_prompt

for attempt in range(1, MAX_RETRIES + 1):

    print(f"\nAttempt {attempt}/{MAX_RETRIES}")

    raw_output = ask_model(current_prompt)

    print("\nRAW OUTPUT:")
    print(raw_output)

    try:
        validated = validate_response(raw_output)

        print("\nVALIDATED OUTPUT:")
        print(validated.model_dump_json(indent=2))

        print("\nSTATUS: SUCCESS")

        break

    except (json.JSONDecodeError, ValidationError) as error:

        print("\nSTATUS: FAILED")

        if attempt == MAX_RETRIES:
            print("Maximum retries reached.")
            print("Final error:")
            print(error)
            break

        current_prompt = f"""
Your previous response failed validation.

Validation error:

{error}

You MUST fix the problem and return ONLY valid JSON.

Original question:

{question}

Required format:

{{
  "answer": "short explanation",
  "topic": "topic name",
  "difficulty": "beginner/intermediate/advanced",
  "confidence": 0.0
}}

Rules:
- confidence must be between 0 and 1
- difficulty must be one of: beginner, intermediate, advanced
- No markdown
- No text outside JSON
"""