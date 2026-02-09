from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

def fixed_size_chunking(text, chunk_size=500, chunk_overlap=100):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text)
    print(f"text split into {len(chunks)} chunks")

    return chunks