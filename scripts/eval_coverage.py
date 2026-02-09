from __future__ import annotations
import argparse
import json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("jsonl", help="Output jsonl from pyttsfrontend-batch")
    args = p.parse_args()

    total_alpha = 0
    dict_hit = 0
    oov = 0

    ipa_available_count = 0
    n = 0

    with Path(args.jsonl).open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            n += 1
            meta = obj.get("meta", {})
            if meta.get("ipa_backend_available"):
                ipa_available_count += 1

            for tok in obj["tokens"]:
                if tok.get("is_alpha"):
                    total_alpha += 1
                    if tok.get("arpabet"):
                        dict_hit += 1
                    elif tok.get("is_oov_arpabet"):
                        oov += 1

    print(f"Sentences: {n}")
    print(f"IPA backend available (sent-level): {ipa_available_count}/{n}")
    print(f"Alpha tokens: {total_alpha}")
    if total_alpha > 0:
        print(f"ARPAbet dict hit rate: {dict_hit/total_alpha:.3f}")
        print(f"ARPAbet OOV rate: {oov/total_alpha:.3f}")

if __name__ == "__main__":
    main()
