from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class TokenOut(BaseModel):
    text: str
    lemma: Optional[str] = None
    pos: Optional[str] = None
    tag: Optional[str] = None
    is_alpha: bool = False
    is_oov_arpabet: bool = False
    arpabet: Optional[List[str]] = None
    ipa: Optional[str] = None
    entity_type: Optional[str] = None

class FrontendOut(BaseModel):
    raw_text: str
    normalized_text: str
    language: str = "en"
    tokens: List[TokenOut]
    meta: Dict[str, Any] = {}
