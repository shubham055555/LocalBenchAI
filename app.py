import ollama


MODEL = "qwen3:1.7b"


print("=" * 40)
print("        LOCALBENCH AI")
print("=" * 40)
print(f"Model: {MODEL}")
print("Type 'exit' to quit.")
print()


while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question.strip():
        continue

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response["message"]["content"]

    print("\nAI:", answer)
    print()