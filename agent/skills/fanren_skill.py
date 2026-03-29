from agent.tools.character_classifier.classifier_tool import classify_fanren_character
from agent.tools.rag_tool import search_fanren_knowledge
from langchain.tools import tool

@tool("fanren skill")
def classify_characters_and_get_fanren_knowledge(query:str) -> dict:
    """
    Use this tool to determine whether the user's question is related to characters or story content from the novel "凡人修仙传".
    If the user asks about the novel "凡人修仙传", including its characters, relationships, story events, or plot.

    The tool will:
    1. Detect whether the query mentions characters from the novel,
       including their aliases.
    2. If the query is related to the novel, retrieve relevant passages
       from the "凡人修仙传" knowledge base.

    If the query is unrelated to the novel, the tool will return an error.

    Input:
        query: the user's question.

    Output:
        Relevant passages from the "凡人修仙传" knowledge base,
        or an error message if the question is not related to the novel.
    """
    classify_res = classify_fanren_character(query)

    if "error" in classify_res:
        return classify_res
    else:
        return search_fanren_knowledge(query)
    