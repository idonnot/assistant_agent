import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import FANREN_NOVEL_DIR, FANREN_DOC_CHUNKS_PATH
from rag.ingest_pipeline import load_novel
from rag.data_preprocess.splitter import split_novel
from rag.index.vector_store import get_vector_store
from rag.retrieval.vector_retriever import VectorRetriever
from rag.retrieval.hybrid_retriever import HybridRetriever
from rag.rerank.reranker import rerank


def test_load_novel():
    texts = load_novel(FANREN_NOVEL_DIR)

    print(len(texts))

    print(texts[0][:1000])


def test_split_novel():
    texts = load_novel(FANREN_NOVEL_DIR)

    chunks = split_novel(texts[0])

    print(len(chunks))

    print(chunks[0])


def test_collection_name():
    vectordb = get_vector_store("fanren")

    print(vectordb._collection.count())

def test_retrieval():
    query = "韩立什么时候进入结丹期"
    vector_retriever=VectorRetriever("fanren")
    docs = vector_retriever.search(query, k=10)
    if not docs:
        return "No relevant information found."

    reranked_docs = rerank(query, docs, topk=5)

    for d in reranked_docs:
        print(f'【{d.metadata["chapter"]}】--- {d.score}')
        print(d.text)

def test_hybrid_retrieval():
    query = "南宫婉"
    hybrid_retriever=HybridRetriever("fanren", FANREN_DOC_CHUNKS_PATH)
    docs = hybrid_retriever.search(query)
    if not docs:
        return "No relevant information found."

    for d in docs:
        print(f'【{d.metadata["chapter"]}】--- {d.score}')
        print(d.text)



if __name__ == "__main__":
    # test_split_novel()
    # test_collection_name()
    # test_retrieval()
    # test_hybrid_retrieval()
    import re

    pattern = r'第(\d+)卷'
    text = "第2240卷 真仙降世第两千两百零二章 黑枭王"
    
    # 方法1：使用re.sub
    text = re.sub(
        r"第(\d+)卷[^\n]*?第[一二三四五六七八九十百千万零两\d]+章\s*(.*)",
        lambda m: f"第{m.group(1)}章 {m.group(2)}",
        text
    )
    print(text)  # 输出：第2292章 三清雷霄符