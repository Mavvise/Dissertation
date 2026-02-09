from __future__ import annotations
import argparse
import json
from pathlib import Path

from pyttsfrontend import Frontend

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--no-ipa", action="store_true")
    p.add_argument("--no-arpabet", action="store_true")
    args = p.parse_args()

    fe = Frontend(enable_ipa=not args.no_ipa, enable_arpabet=not args.no_arpabet)

    inp = Path(args.inp)
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)

    n = 0
    with inp.open("r", encoding="utf-8") as f_in, outp.open("w", encoding="utf-8") as f_out:
        for line in f_in:
            rec = json.loads(line)
            text = rec["text"]
            out = fe.process(text).model_dump()
            out["meta"]["dataset_id"] = rec.get("id")
            out["meta"]["audio_path"] = rec.get("audio_path")
            f_out.write(json.dumps(out, ensure_ascii=False) + "\n")
            n += 1

    print(f"Wrote {n} frontend outputs to {outp}")

if __name__ == "__main__":
    main()
