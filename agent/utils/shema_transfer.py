from ..schemas.rag_schema import RetrievedDocument

def ragdoc_to_schema(doc) -> RetrievedDocument:
    return RetrievedDocument(
        content=doc.text,
        source=doc.metadata.get("source") if doc.metadata else None,
        score=doc.score,
        metadata=doc.metadata or {}
    )