from __future__ import annotations
from pyttsfrontend.phonemes.ipa import try_phonemize

class PhonemizerOnlyBaseline:
    def __init__(self, ipa_language: str = "en-us"):
        self.ipa_language = ipa_language

    def process(self, raw_text: str) -> dict:
        ipa = try_phonemize(raw_text, language=self.ipa_language)
        return {
            "raw_text": raw_text,
            "normalized_text": raw_text,
            "language": "en",
            "tokens": [],
            "meta": {
                "baseline": "phonemizer_only",
                "ipa_backend_available": ipa is not None,
                "ipa_sentence": ipa,
            },
        }
