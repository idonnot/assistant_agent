from agent.services.character_classifier.basic_character_classifier import BasicCharacterClassifier
from langchain.tools import tool

def classify_fanren_character(query: str) -> dict:
    """
    Use this tool to determine whether the user's question is related to characters or story content from the novel "凡人修仙传".

    The tool checks whether the query mentions characters from the novel, such as:

    - 韩立
    - 南宫婉
    - 紫灵
    - 元瑶
    - 银月
    - 墨大夫
    - 向之礼
    - 凌玉灵
    - 极阴老祖
    - etc.

    It also recognizes character aliases, such as:
    - 韩跑跑
    - 韩老魔
    - 南宫仙子
    - 紫灵仙子

    Return characters if the question is about characters, relationships, events, or story knowledge in the novel.

    Return error if the question is unrelated to the novel.
    """
    classifier = BasicCharacterClassifier()
    is_fanren, details = classifier.classify(query)

    if is_fanren:
        characters = classifier.get_character_from_query(query)
        return {
            "character": characters
        }
    else:
        return {"error":"User's query doesn't relate to any characters of the novel of '凡人修仙传'"}