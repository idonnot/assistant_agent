from langchain.tools import tool
from typing import List

from ..schemas.rag_schema import RAGResponse
from ..schemas.tool_schema import ToolResponse
from ..utils.shema_transfer import ragdoc_to_schema
from rag.retrieval.hybrid_retriever import HybridRetriever
from config.settings import FANREN_DOC_CHUNKS_PATH


def search_fanren_knowledge(query: str) -> str:
    """
    Search knowledge from the novel '凡人修仙传'.

    Use this tool when the user asks questions about:
    - characters
    - characters' relationships
    - story plots
    - events in the novel
    - world setting
    """

    hybrid_retriever = HybridRetriever("fanren", FANREN_DOC_CHUNKS_PATH)

    docs = hybrid_retriever.search(query)

    if not docs:
        return ToolResponse(
            status="error",
            message="No relevant information found in novel.",
            data=None
        ).model_dump_json()

    schema_docs = [ragdoc_to_schema(d) for d in docs]

    rag_response = RAGResponse(
        query=query,
        documents=schema_docs,
        answer=None  
    )

    return ToolResponse(
        status="success",
        message=None,
        data=rag_response.model_dump()
    ).model_dump_json()