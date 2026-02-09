from __future__ import annotations
import argparse
import json
from pathlib import Path

def load_jsonl(p: Path):
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="input", required=True)
    ap.add_argument("--out", dest="output", required=True)
    args = ap.parse_args()

    inp = Path(args.input)
    out = Path(args.output)

    out.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for rec in load_jsonl(inp):
        rows.append({
            "raw_text": rec.get("raw_text", ""),
            "normalized_text": rec.get("normalized_text", ""),
            "ipa_sentence": rec.get("meta", {}).get("ipa_sentence", ""),
            "ipa_backend_available": rec.get("meta", {}).get("ipa_backend_available", False),
        })

    # very simple CSV
    import csv
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["raw_text","normalized_text","ipa_sentence","ipa_backend_available"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Wrote {len(rows)} rows to {out}")

if __name__ == "__main__":
    main()
