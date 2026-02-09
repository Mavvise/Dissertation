from __future__ import annotations
import argparse
import json
from pathlib import Path
from rich import print
from .pipeline import Frontend

def main():
    p = argparse.ArgumentParser(prog="pyttsfrontend")
    p.add_argument("text", help="Input text")
    p.add_argument("--spacy-model", default="en_core_web_sm")
    p.add_argument("--ipa-language", default="en-us")
    p.add_argument("--no-ipa", action="store_true")
    p.add_argument("--no-arpabet", action="store_true")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = p.parse_args()

    fe = Frontend(
        spacy_model=args.spacy_model,
        ipa_language=args.ipa_language,
        enable_ipa=not args.no_ipa,
        enable_arpabet=not args.no_arpabet,
    )
    out = fe.process(args.text).model_dump()

    if args.pretty:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(out, ensure_ascii=False))

def batch_main():
    p = argparse.ArgumentParser(prog="pyttsfrontend-batch")
    p.add_argument("input", help="Input .txt file, one sentence per line")
    p.add_argument("--out", required=True, help="Output .jsonl path")
    p.add_argument("--spacy-model", default="en_core_web_sm")
    p.add_argument("--ipa-language", default="en-us")
    p.add_argument("--no-ipa", action="store_true")
    p.add_argument("--no-arpabet", action="store_true")
    args = p.parse_args()

    fe = Frontend(
        spacy_model=args.spacy_model,
        ipa_language=args.ipa_language,
        enable_ipa=not args.no_ipa,
        enable_arpabet=not args.no_arpabet,
    )

    inp = Path(args.input)
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)

    with inp.open("r", encoding="utf-8") as f_in, outp.open("w", encoding="utf-8") as f_out:
        for line in f_in:
            s = line.strip()
            if not s:
                continue
            res = fe.process(s).model_dump()
            f_out.write(json.dumps(res, ensure_ascii=False) + "\n")
