import pickle
from rag.rerank.reranker import rerank
from rag.retrieval.vector_retriever import VectorRetriever
from rag.retrieval.bm25_retriever import BM25Retriever

class HybridRetriever:

    def __init__(self, collection_name:str, doc_chunks_path:str):

        self.vector = VectorRetriever(collection_name)

        with open(doc_chunks_path, "rb") as f:
            documents = pickle.load(f)
        self.bm25 = BM25Retriever(documents)

    def search(self, query: str, retrieve_top_k: int = 30, rerank_top_k: int = 5):

        vector_docs = self.vector.search(query, retrieve_top_k)

        bm25_docs = self.bm25.search(query, retrieve_top_k)

        docs = vector_docs + bm25_docs

        docs = rerank(query, docs, rerank_top_k)

        return docs