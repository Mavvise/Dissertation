from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

DIGIT_RE = re.compile(r"\d")

def load_jsonl(p: Path):
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def ipa_available(x: dict) -> bool:
    return bool(x.get("meta", {}).get("ipa_sentence"))

def alpha_token_count(x: dict) -> int:
    toks = x.get("tokens", [])
    return sum(1 for t in toks if t.get("is_alpha"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="pyttsfrontend.jsonl")
    ap.add_argument("--b", required=True, help="phonemizer_only.jsonl")
    ap.add_argument("--c", required=True, help="num2words_only.jsonl")
    args = ap.parse_args()

    A = list(load_jsonl(Path(args.a)))
    B = list(load_jsonl(Path(args.b)))
    C = list(load_jsonl(Path(args.c)))
    n = min(len(A), len(B), len(C))

    a_ipa = sum(ipa_available(x) for x in A[:n])
    b_ipa = sum(ipa_available(x) for x in B[:n])
    c_ipa = sum(ipa_available(x) for x in C[:n])

    avg_alpha = (sum(alpha_token_count(x) for x in A[:n]) / n) if n else 0.0

    # ARPAbet coverage for pyttsfrontend
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

    # Normalization impact on digit-containing sentences
    digit_sent = 0
    changed_py = 0
    changed_num2 = 0
    changed_both = 0

    for i in range(n):
        raw = (A[i].get("raw_text") or "").strip()
        if not DIGIT_RE.search(raw):
            continue
        digit_sent += 1

        norm_a = (A[i].get("normalized_text") or "").strip()
        norm_c = (C[i].get("normalized_text") or "").strip()

        py_changed = (norm_a != raw) and (norm_a != "")
        c_changed = (norm_c != raw) and (norm_c != "")

        if py_changed:
            changed_py += 1
        if c_changed:
            changed_num2 += 1
        if py_changed and c_changed:
            changed_both += 1

    print(f"=== Three-way Comparison Summary (N={n}) ===")
    print(f"IPA available (pyttsfrontend)    : {a_ipa}/{n} = {a_ipa/n:.3f}")
    print(f"IPA available (phonemizer-only)  : {b_ipa}/{n} = {b_ipa/n:.3f}")
    print(f"IPA available (num2words-only)   : {c_ipa}/{n} = {c_ipa/n:.3f}")
    print(f"Avg alpha tokens per sentence (pyttsfrontend): {avg_alpha:.2f}")

    if total_alpha:
        print(f"ARPAbet dict hit rate (pyttsfrontend): {dict_hit/total_alpha:.3f}")
        print(f"ARPAbet OOV rate (pyttsfrontend)     : {oov/total_alpha:.3f}")

    print("--- Normalization impact (digit-containing sentences) ---")
    if digit_sent == 0:
        print("Digit sentences: 0 (no analysis)")
    else:
        print(f"Digit sentences: {digit_sent}/{n} = {digit_sent/n:.3f}")
        print(f"Changed normalized_text (pyttsfrontend): {changed_py}/{digit_sent} = {changed_py/digit_sent:.3f}")
        print(f"Changed normalized_text (num2words-only): {changed_num2}/{digit_sent} = {changed_num2/digit_sent:.3f}")
        print(f"Both changed: {changed_both}/{digit_sent} = {changed_both/digit_sent:.3f}")

if __name__ == "__main__":
    main()
