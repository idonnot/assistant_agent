from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import VECTOR_DB_MODEL

def get_embedding_model():
    """
    Load embedding model for RAG
    """

    embedding = HuggingFaceEmbeddings(
        model_name=VECTOR_DB_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    return embedding