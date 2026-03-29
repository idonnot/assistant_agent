from langchain.tools import tool
from rag.schema import RagDoc
from rag.retrieval.hybrid_retriever import HybridRetriever
from config.settings import FANREN_DOC_CHUNKS_PATH

def search_fanren_knowledge(query: str) -> list[RagDoc]:
    """
    Search knowledge from the novel '凡人修仙传'.

    Use this tool when the user asks questions about:
    - characters
    - characters' relationships
    - story plots
    - events in the novel
    - world setting

    Args:
        query: user question about the novel

    Returns:
        Relevant passages from the novel knowledge base
    """
    hybrid_retriever=HybridRetriever("fanren", FANREN_DOC_CHUNKS_PATH)
    docs = hybrid_retriever.search(query)
    if not docs:
        return {"error": "No relevant information found in novel."}

    return docs
