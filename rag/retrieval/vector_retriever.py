from rag.schema import RagDoc
from rag.index.vector_store import get_vector_store

class VectorRetriever:

    def __init__(self, collection_name:str):

        self.vectordb = get_vector_store(collection_name)

    def search(self, query: str, k: int = 40) -> list[RagDoc]:
        docs = self.vectordb.similarity_search(
            query,
            k=k
        )

        results = []

        for d in docs:
            results.append(
                RagDoc(
                    text=d.page_content,
                    metadata={"chapter": d.metadata.get("chapter", "Unknown")},
                    score=0
                )
            )

        return results