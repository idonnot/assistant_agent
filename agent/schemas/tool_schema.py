from pydantic import BaseModel
from typing import List, Optional

# Input schema
class QueryInput(BaseModel):
    query: str

class WeatherQuery(BaseModel):
    city: str
    
class NovelQuery(BaseModel):
    query: str
    character: Optional[str] = None

# response schema
class ToolResponse(BaseModel):
    status: str   # success / error
    message: Optional[str] = None
    data: Optional[dict] = None