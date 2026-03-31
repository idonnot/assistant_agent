from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RetrievedDocument(BaseModel):
    content: str = Field(..., description="文本内容")
    source: Optional[str] = Field(None, description="来源，比如文件名或URL")
    score: Optional[float] = Field(None, description="相似度或rerank分数")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class RAGResponse(BaseModel):
    query: str
    documents: List[RetrievedDocument]
    answer: Optional[str] = None