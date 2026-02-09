from __future__ import annotations
from typing import List, Optional
import cmudict

class ArpabetG2P:
    def __init__(self):
        self._dict = cmudict.dict()

    def lookup(self, word: str) -> Optional[List[str]]:
        key = word.lower()
        if key not in self._dict:
            return None
        return list(self._dict[key][0])
