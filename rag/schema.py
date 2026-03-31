from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class RagDoc:
    text: str
    metadata: Dict
    score: Optional[float] = None
