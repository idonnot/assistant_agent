from langchain_chroma import Chroma
from rag.index.embedding import get_embedding_model
from config.settings import CHROMA_DIR


def get_vector_store(collection_name: str) -> Chroma:

    embedding = get_embedding_model()

    vectordb = Chroma(
        collection_name=collection_name,
        persist_directory=CHROMA_DIR,
        embedding_function=embedding
    )

    return vectordb