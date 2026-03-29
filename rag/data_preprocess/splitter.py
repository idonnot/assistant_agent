import re
from typing import List
from rag.schema import RagDoc


def split_by_chapter(text: str) -> List[str]:
    """
    Split novel text by chapter
    """

    chapters = re.split(r"(第\s*\d+\s*章[^\n]*)", text)

    merged = []

    for i in range(1, len(chapters), 2):
        title = chapters[i]
        content = chapters[i + 1] if i + 1 < len(chapters) else ""

        merged.append((title, content))

    return merged


def split_by_paragraph(chapter: str) -> List[str]:
    """
    Split chapter into paragraphs
    """

    # keep every non-empty line as a paragraph; some lines shorter than
    # 10 characters may still carry narrative importance
    paragraphs = [
        p.strip()
        for p in chapter.split("\n")
        if p.strip()  # drop purely blank lines only
    ]

    return paragraphs


def merge_paragraphs(
    chapter_title: str,
    paragraphs: List[str],
    chunk_size: int = 800,
    chunk_overlap: int = 200
) -> List[RagDoc]:

    chunks = []
    current_chunk = []
    current_len = 0

    for p in paragraphs:

        p_len = len(p)

        if current_len + p_len > chunk_size and current_chunk:

            chunk = "\n".join(current_chunk)
            chunks.append(
                RagDoc(
                    text=chunk,
                    metadata={
                        "chapter": chapter_title
                    }
                )
            )

            overlap_chunk = []
            overlap_len = 0

            for para in reversed(current_chunk):

                overlap_chunk.insert(0, para)
                overlap_len += len(para)

                if overlap_len >= chunk_overlap:
                    break

            current_chunk = overlap_chunk
            current_len = sum(len(x) for x in current_chunk)

        current_chunk.append(p)
        current_len += p_len

    if current_chunk:
        chunks.append(
                RagDoc(
                    text="\n".join(current_chunk),
                    metadata={
                        "chapter": chapter_title
                    }
                )
            )

    return chunks


def split_novel(text: str, chunk_size: int = 800, chunk_overlap: int = 200) -> list[dict]:
    """
    Full pipeline to split novel text into overlapping chunks.
    
    Args:
        text: full novel text
        chunk_size: target size for each chunk in characters (default 800)
        chunk_overlap: overlap between consecutive chunks (default 200)
    
    Returns:
        list of dictionaries containing text and chapter information
    """

    all_chunks = []

    chapters = split_by_chapter(text)

    for title, chapter in chapters:
        paragraphs = split_by_paragraph(chapter)

        chunks = merge_paragraphs(title, paragraphs)
        
        all_chunks.extend(chunks)

    return all_chunks
