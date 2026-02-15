import ollama

MODEL_NAME = "qwen2.5:3b"

def invoke_conversation(context, user_input):
    system_prompt = (
        "Use the provided news snippets to answer the user's question accurately. "
        "If the answer isn't in the context, say you don't have that specific data yet. "
        "Keep your tone professional yet engaging."
        "Always emphasize that your answers are subject to errors and should be verified."
    )

    full_prompt = f"CONTEXT FROM LATEST NEWS:\n{context}\n\nUSER QUESTION: {user_input}"

    response = ollama.chat(
        model = MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt},
        ]
    )

    print(type(response))

    return response['message']['content']
