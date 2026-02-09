from __future__ import annotations
import spacy

def load_nlp(model: str = "en_core_web_sm"):
    return spacy.load(model)
