from __future__ import annotations
import re
from num2words import num2words

_num_re = re.compile(r"\b\d+(\.\d+)?\b")

def basic_normalize(text: str) -> str:
    """
    MVP: expand standalone numbers using num2words.
    Keeps the rest unchanged.
    """
    def repl(m: re.Match) -> str:
        s = m.group(0)
        if "." in s:
            # simple decimal handling: "12.5" -> "twelve point five"
            left, right = s.split(".", 1)
            left_w = num2words(int(left))
            right_w = " ".join(num2words(int(ch)) for ch in right if ch.isdigit())
            return f"{left_w} point {right_w}".strip()
        return num2words(int(s))

    return _num_re.sub(repl, text)
