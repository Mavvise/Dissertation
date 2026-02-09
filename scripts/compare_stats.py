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
    ap.add_argument("--a", required=True, help="pyttsfrontend.jsonl")
    ap.add_argument("--b", required=True, help="phonemizer_only.jsonl")
    args = ap.parse_args()

    A = list(load_jsonl(Path(args.a)))
    B = list(load_jsonl(Path(args.b)))

    n = min(len(A), len(B))

    def ipa_available(x):
        return bool(x.get("meta", {}).get("ipa_sentence"))

    def avg_len(x):
        toks = x.get("tokens", [])
        # 只统计字母 token，近似衡量“有意义 token 数”
        return sum(1 for t in toks if t.get("is_alpha"))

    a_ipa = sum(ipa_available(x) for x in A[:n])
    b_ipa = sum(ipa_available(x) for x in B[:n])

    a_avg_tokens = sum(avg_len(x) for x in A[:n]) / n if n else 0.0

    # ARPAbet coverage
    total_alpha = 0
    dict_hit = 0
    oov = 0
    for x in A[:n]:
        for t in x.get("tokens", []):
            if t.get("is_alpha"):
                total_alpha += 1
                if t.get("arpabet"):
                    dict_hit += 1
                elif t.get("is_oov_arpabet"):
                    oov += 1

    print("=== Comparison Summary (N=%d) ===" % n)
    print(f"IPA available (pyttsfrontend): {a_ipa}/{n} = {a_ipa/n:.3f}")
    print(f"IPA available (phonemizer-only): {b_ipa}/{n} = {b_ipa/n:.3f}")
    print(f"Avg alpha tokens per sentence (pyttsfrontend): {a_avg_tokens:.2f}")

    if total_alpha:
        print(f"ARPAbet dict hit rate (pyttsfrontend): {dict_hit/total_alpha:.3f}")
        print(f"ARPAbet OOV rate (pyttsfrontend): {oov/total_alpha:.3f}")

if __name__ == "__main__":
    main()
