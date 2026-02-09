import ollama

EMBED_MODEL_NAME = "nomic-embed-text"
EMBED_VECTOR_DIM = 768

def embed(text, mode="QUERY"):
    """
    Wraps the local Ollama API to generate a real 768-dim vector.
    """
    prefix = "search_document: " if mode == "DOC" else "search_query: "

    response = ollama.embeddings(
        model=EMBED_MODEL_NAME,
        prompt=f"{prefix}{text}"
    )
    return response["embedding"]