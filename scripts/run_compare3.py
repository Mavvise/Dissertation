from __future__ import annotations
import argparse
import json
from pathlib import Path

from pyttsfrontend import Frontend
from pyttsfrontend.baselines.phonemizer_only import PhonemizerOnlyBaseline
from pyttsfrontend.baselines.num2words_only import Num2WordsOnlyBaseline

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--max", type=int, default=0)
    args = p.parse_args()

    inp = Path(args.inp)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    fe = Frontend(enable_ipa=True, enable_arpabet=True)
    base1 = PhonemizerOnlyBaseline()
    base2 = Num2WordsOnlyBaseline()

    out_a = outdir / "pyttsfrontend.jsonl"
    out_b = outdir / "phonemizer_only.jsonl"
    out_c = outdir / "num2words_only.jsonl"

    n = 0
    with inp.open("r", encoding="utf-8") as f_in, \
         out_a.open("w", encoding="utf-8") as f_a, \
         out_b.open("w", encoding="utf-8") as f_b, \
         out_c.open("w", encoding="utf-8") as f_c:

        for line in f_in:
            rec = json.loads(line)
            text = rec["text"]

            a = fe.process(text).model_dump()
            a["meta"]["dataset_id"] = rec.get("id")
            f_a.write(json.dumps(a, ensure_ascii=False) + "\n")

            b = base1.process(text)
            b["meta"]["dataset_id"] = rec.get("id")
            f_b.write(json.dumps(b, ensure_ascii=False) + "\n")

            c = base2.process(text)
            c["meta"]["dataset_id"] = rec.get("id")
            f_c.write(json.dumps(c, ensure_ascii=False) + "\n")

            n += 1
            if args.max and n >= args.max:
                break

    print(f"Wrote {n} triples to {outdir}")
    print(out_a)
    print(out_b)
    print(out_c)

if __name__ == "__main__":
    main()
