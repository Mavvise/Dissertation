from __future__ import annotations
from typing import Optional, List
from .schema import FrontendOut, TokenOut
from .components.normalizer import basic_normalize
from .components.spacy_nlp import load_nlp
from .phonemes.arpabet import ArpabetG2P
from .phonemes.ipa import try_phonemize

class Frontend:
    def __init__(
        self,
        spacy_model: str = "en_core_web_sm",
        ipa_language: str = "en-us",
        enable_ipa: bool = True,
        enable_arpabet: bool = True,
    ):
        self.nlp = load_nlp(spacy_model)
        self.ipa_language = ipa_language
        self.enable_ipa = enable_ipa
        self.enable_arpabet = enable_arpabet
        self.arpabet = ArpabetG2P() if enable_arpabet else None

    def process(self, raw_text: str) -> FrontendOut:
        norm = basic_normalize(raw_text)
        doc = self.nlp(norm)

        # sentence-level IPA (best-effort)
        ipa_sentence: Optional[str] = None
        if self.enable_ipa:
            ipa_sentence = try_phonemize(norm, language=self.ipa_language)

        tokens: List[TokenOut] = []
        for t in doc:
            if t.is_space:
                continue

            tok = TokenOut(
                text=t.text,
                lemma=t.lemma_ if t.lemma_ else None,
                pos=t.pos_ if t.pos_ else None,
                tag=t.tag_ if t.tag_ else None,
                is_alpha=bool(t.is_alpha),
                entity_type=t.ent_type_ if t.ent_type_ else None,
            )

            # ARPAbet per token (dictionary lookup)
            if self.enable_arpabet and tok.is_alpha and self.arpabet is not None:
                pr = self.arpabet.lookup(tok.text)
                if pr is None:
                    tok.is_oov_arpabet = True
                else:
                    tok.arpabet = pr

            tokens.append(tok)

        # MVP: attach sentence IPA to meta; token-level IPA alignment can be improved later
        out = FrontendOut(
            raw_text=raw_text,
            normalized_text=norm,
            tokens=tokens,
            meta={
                "spacy_model": self.nlp.meta.get("name", "unknown"),
                "ipa_backend_available": ipa_sentence is not None,
                "ipa_sentence": ipa_sentence,
            },
        )
        return out
