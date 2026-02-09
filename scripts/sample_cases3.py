from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

SPECIAL_PATTERNS = [
    re.compile(r"\d"),                         # any digit
    re.compile(r"\b\d+(st|nd|rd|th)\b", re.I),  # ordinal
    re.compile(r"\b(19\d{2}|20\d{2})\b"),      # year
    re.compile(r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b"),  # date-like
    re.compile(r"(\$|€|£)\s?\d"),              # currency
    re.compile(r"\b\d+(\.\d+)?%\b"),           # percent
    re.compile(r"\b(Dr|Mr|Mrs|Ms)\.", re.I),   # abbreviations
    re.compile(r"U\.S\.|e\.g\.|i\.e\.", re.I),
    re.compile(r"@"),                          # @ or email-ish
]

def load_jsonl(p: Path):
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def clip(s: str | None, n: int = 140) -> str:
    if not s:
        return ""
    s = s.replace("\n", " ").strip()
    return s if len(s) <= n else s[:n] + "..."

def is_special(raw: str) -> bool:
    return any(rgx.search(raw) for rgx in SPECIAL_PATTERNS)

def extract_oov_arpabet(frontend_rec: dict) -> list[str]:
    oovs = []
    for t in frontend_rec.get("tokens", []):
        if t.get("is_oov_arpabet"):
            oovs.append(t.get("text", ""))
    # unique preserve order
    seen = set()
    out = []
    for x in oovs:
        x = (x or "").strip()
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="results/.../pyttsfrontend.jsonl")
    ap.add_argument("--b", required=True, help="results/.../phonemizer_only.jsonl")
    ap.add_argument("--c", required=True, help="results/.../num2words_only.jsonl")
    ap.add_argument("--k", type=int, default=15)
    ap.add_argument("--minlen", type=int, default=20)
    ap.add_argument("--only_special", action="store_true", help="Filter to 'frontend phenomena' sentences")
    ap.add_argument("--ipa_clip", type=int, default=140)
    args = ap.parse_args()

    A = list(load_jsonl(Path(args.a)))
    B = list(load_jsonl(Path(args.b)))
    C = list(load_jsonl(Path(args.c)))
    n = min(len(A), len(B), len(C))

    picked = []
    for i in range(n):
        raw = (A[i].get("raw_text") or "").strip()
        if len(raw) < args.minlen:
            continue
        if args.only_special and not is_special(raw):
            continue
        picked.append(i)
        if len(picked) >= args.k:
            break

    for idx in picked:
        a = A[idx]
        b = B[idx]
        c = C[idx]

        raw = a.get("raw_text") or ""
        norm_a = a.get("normalized_text") or ""
        norm_c = c.get("normalized_text") or ""

        ipa_a = a.get("meta", {}).get("ipa_sentence")
        ipa_b = b.get("meta", {}).get("ipa_sentence")
        ipa_c = c.get("meta", {}).get("ipa_sentence")

        oovs = extract_oov_arpabet(a)

        print("=" * 92)
        print(f"RAW : {raw}")
        print(f"NORM (pyttsfrontend) : {norm_a}")
        print(f"NORM (num2words-only): {norm_c}")
        print(f"IPA  (pyttsfrontend) : {clip(ipa_a, args.ipa_clip)}")
        print(f"IPA  (phonemizer-only): {clip(ipa_b, args.ipa_clip)}")
        print(f"IPA  (num2words-only): {clip(ipa_c, args.ipa_clip)}")
        print(f"ARPAbet OOV tokens    : {oovs}")

if __name__ == "__main__":
    main()
