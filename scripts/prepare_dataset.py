from __future__ import annotations
import argparse
import json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="wikitext")
    p.add_argument("--config", default="wikitext-2-raw-v1")
    p.add_argument("--split", default="test")
    p.add_argument("--out", default="data/textonly.jsonl")
    p.add_argument("--max", type=int, default=200)
    p.add_argument("--streaming", action="store_true")
    p.add_argument("--field", default="text", help="Which field to read as text")
    args = p.parse_args()

    from datasets import load_dataset

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)

    ds = load_dataset(args.dataset, args.config, split=args.split, streaming=args.streaming)

    n = 0
    with outp.open("w", encoding="utf-8") as f:
        for ex in ds:
            text = ex.get(args.field) or ""
            text = text.strip()
            if not text:
                continue

            if len(text) < 20:
                continue

            rec = {"id": str(n), "text": text}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
            if args.max and n >= args.max:
                break

    print(f"Wrote {n} records to {outp} (dataset={args.dataset}, streaming={args.streaming})")

if __name__ == "__main__":
    main()
