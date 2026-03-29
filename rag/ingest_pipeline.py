import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
from rag.data_preprocess.data_cleaner import clean_novel_text
from rag.data_preprocess.splitter import split_novel
from rag.index.vector_store import get_vector_store
import pickle


def load_novel(folder_path):

    texts = []

    for file in os.listdir(folder_path):

        if file.endswith(".txt"):

            path = Path(folder_path) / file

            with open(path, "r", encoding="utf-8") as f:

                text = f.read()
                texts.append(text)

    return texts

def build_vector_db(novel_dir: str, doc_chunks_path: str):
    vectordb = get_vector_store("fanren")

    all_chunks = []

    texts = load_novel(novel_dir)

    for text in texts:
        clean_text = clean_novel_text(text)

        chunks = split_novel(clean_text)

        all_chunks.extend(chunks)

    print("Total chunks:", len(all_chunks))
    with open(doc_chunks_path, "wb") as f:
        pickle.dump(all_chunks, f)

    BATCH_SIZE = 1000

    for i in range(0, len(all_chunks), BATCH_SIZE):

        batch = all_chunks[i:i+BATCH_SIZE]

        texts = [item.text for item in batch]
        metadatas = [
            {"chapter": item.metadata["chapter"]}
            for item in batch
        ]

        vectordb.add_texts(
            texts=texts,
            metadatas=metadatas
        )

        print(f"Inserted {i+len(batch)} / {len(all_chunks)}")

    print("RAG database built successfully!")


if __name__ == "__main__":
    from config.settings import FANREN_NOVEL_DIR, FANREN_DOC_CHUNKS_PATH
    build_vector_db(FANREN_NOVEL_DIR, FANREN_DOC_CHUNKS_PATH)

