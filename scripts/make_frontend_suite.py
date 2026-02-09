from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "number": re.compile(r"\d"),
    "decimal_unit": re.compile(r"\b\d+(\.\d+)?\s?(kg|km|cm|mm|m|g|lbs|lb|mph|km/h)\b", re.I),
    "currency": re.compile(r"(\$|€|£)\s?\d|(\bUSD\b|\bEUR\b|\bGBP\b)", re.I),
    "date_like": re.compile(r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b"),
    "year": re.compile(r"\b(19\d{2}|20\d{2})\b"),
    "abbr": re.compile(r"\b(Dr|Mr|Mrs|Ms)\.|U\.S\.|e\.g\.|i\.e\.", re.I),
    "email_or_at": re.compile(r"@"),
    "percent": re.compile(r"\b\d+(\.\d+)?%\b"),
    "ordinal": re.compile(r"\b\d+(st|nd|rd|th)\b", re.I),
}

def score(text: str) -> int:
    s = 0
    for _, rgx in PATTERNS.items():
        if rgx.search(text):
            s += 1
    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--minlen", type=int, default=20)
    ap.add_argument("--maxlen", type=int, default=220)
    args = ap.parse_args()

    inp = Path(args.inp)
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with inp.open("r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            text = (rec.get("text") or "").strip()
            if len(text) < args.minlen or len(text) > args.maxlen:
                continue
            sc = score(text)
            if sc == 0:
                continue
            rows.append((sc, rec))

    rows.sort(key=lambda x: x[0], reverse=True)

    picked = []
    seen = set()
    for sc, rec in rows:
        t = rec.get("text", "").strip()
        if t in seen:
            continue
        seen.add(t)
        picked.append({"id": rec.get("id"), "text": t, "score": sc})
        if len(picked) >= args.max:
            break

    with outp.open("w", encoding="utf-8") as f:
        for i, rec in enumerate(picked):
            rec2 = {"id": rec.get("id", str(i)), "text": rec["text"]}
            f.write(json.dumps(rec2, ensure_ascii=False) + "\n")

    print(f"Wrote {len(picked)} sentences to {outp}")

if __name__ == "__main__":
    main()
