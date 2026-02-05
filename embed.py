import ollama

EMBED_MODEL_NAME = "nomic-embed-text"
EMBED_VECTOR_DIM = 768
DOC_MODE = "DOC"
QUERY_MODE = "QUERY"

def get_embedding(text, mode=QUERY_MODE):
    """
    Wraps the local Ollama API to generate a real 768-dim vector.
    """
    prefix = "search_document: " if mode == "DOC" else "search_query: "

    response = ollama.embeddings(
        model=EMBED_MODEL_NAME,
        prompt=f"{prefix}{text}"
    )
    return response["embedding"]


user_input = "Who is leading the Golden Boot race in the Premier League?"
query_vector = get_embedding(user_input)
print("text embedded successfully" if len(query_vector) == EMBED_VECTOR_DIM else "text embedded failed")