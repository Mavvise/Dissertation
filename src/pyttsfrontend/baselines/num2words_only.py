from __future__ import annotations
import re
from typing import Optional

from pyttsfrontend.phonemes.ipa import try_phonemize

_num_re = re.compile(r"\b\d+(\.\d+)?\b")

def _num_to_words(token: str) -> str:
    try:
        from num2words import num2words
    except Exception:
        return token

    # try int first
    if token.isdigit():
        try:
            return num2words(int(token))
        except Exception:
            return token

    # decimal like 12.5
    try:
        val = float(token)
        # simple strategy: "twelve point five"
        whole = int(val)
        frac = str(token).split(".")[1]
        whole_words = num2words(whole)
        frac_words = " ".join(num2words(int(ch)) for ch in frac if ch.isdigit())
        return f"{whole_words} point {frac_words}".strip()
    except Exception:
        return token

def simple_num_normalize(text: str) -> str:
    def repl(m):
        return _num_to_words(m.group(0))
    return _num_re.sub(repl, text)

class Num2WordsOnlyBaseline:
    """
    Baseline: only number-to-words normalization + sentence-level IPA via eSpeak-NG.
    No spaCy, no CMUdict.
    """
    def __init__(self, ipa_language: str = "en-us"):
        self.ipa_language = ipa_language

    def process(self, raw_text: str) -> dict:
        norm = simple_num_normalize(raw_text)
        ipa = try_phonemize(norm, language=self.ipa_language)
        return {
            "raw_text": raw_text,
            "normalized_text": norm,
            "language": "en",
            "tokens": [],
            "meta": {
                "baseline": "num2words_only",
                "ipa_backend_available": ipa is not None,
                "ipa_sentence": ipa,
            },
        }
