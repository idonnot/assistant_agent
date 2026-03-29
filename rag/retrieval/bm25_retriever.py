from rank_bm25 import BM25Okapi
from rag.schema import RagDoc

class BM25Retriever:

    def __init__(self, documents: list[RagDoc]):

        self.documents = documents

        tokenized_docs = [
            doc.text.split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(tokenized_docs)

    def search(self, query, k=10):

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for doc, score in ranked[:k]:
            results.append(
                RagDoc(
                    text=doc.text,
                    metadata=doc.metadata,
                    score=float(score)
                )
            )

        return results
    