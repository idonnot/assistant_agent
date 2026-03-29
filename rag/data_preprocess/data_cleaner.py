import re

def clean_novel_text(text: str) -> str:
    """
    Clean fanren novel txt for RAG
    """

    # delete copyright information
    text = re.sub(r"《凡人修仙传》", '', text)
    text = re.sub(r"作者：.*", '', text)
    text = re.sub(r"来源：.*", '', text)
    text = re.sub(r"网址：.*", '', text)

    # delete repeated chapter titles
    text = re.sub(r"(第\d+章[^\n]+)\n\s*\1", r"\1", text)       # identical titles
    text = re.sub(r"[ \t　]*第[一二三四五六七八九十百千万]+章[^\n]*", "", text)
    text = re.sub(
        r"第(\d+)卷[^\n]*?第[一二三四五六七八九十百千万零两\d]+章\s*(.*)",
        lambda m: f"第{m.group(1)}章 {m.group(2)}",
        text
    )

    # delete chapter completion indicators
    text = re.sub(r"(本章完)", '', text)
    # match "新" + any chars (lazy) + "书吧→"
    text = re.sub(r"新.*?书吧→", '', text)

    # delete broken urls
    patterns = [
        r'^\s*（请记住.*?更新.*?）',
        r'^\s*【记住.*?】',
        r'^\s*.*全手打无错站.*',
        r'^\s*本书首发.*',
        r'更多精彩小说，请访问：.*',
        r'【写到这里我希望读者记一下我们域名.*',
    ]
    for p in patterns:
        text = re.sub(p, '\n', text, flags=re.MULTILINE)

    text = re.sub(r'[^\u4e00-\u9fa5。]{5,}[a-zA-Z0-9]*[^\u4e00-\u9fa5]*', '', text)
    text = re.sub(r'(\(\))', '', text)
    text = text.strip()

    # delete full-width indentation
    text = text.replace("　　", '')

    # delete excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text
