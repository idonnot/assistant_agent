from sentence_transformers import CrossEncoder

from rag.schema import RagDoc
from config.settings import RERANK_MODEL

reranker = CrossEncoder(RERANK_MODEL)

def rerank(query: str, docs: list[RagDoc], topk: int = 5) -> list[RagDoc]:

    pairs = [
        [query, doc.text]
        for doc in docs
    ]

    scores = reranker.predict(pairs)

    scored = []

    for doc, score in zip(docs, scores):
        doc.score = float(score)

        scored.append(doc)

    scored.sort(
        key=lambda x: x.score,
        reverse=True
    )

    return scored[:topk]