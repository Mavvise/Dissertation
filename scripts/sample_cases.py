from __future__ import annotations
import argparse
import json
from pathlib import Path

def load_jsonl(p: Path):
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def clip(s: str | None, n: int = 120) -> str:
    if not s:
        return ""
    s = s.replace("\n", " ").strip()
    return s if len(s) <= n else s[:n] + "..."

def extract_oov_arpabet(frontend_rec: dict) -> list[str]:
    oovs = []
    for t in frontend_rec.get("tokens", []):
        if t.get("is_oov_arpabet"):
            oovs.append(t.get("text", ""))
    # unique preserve order
    seen = set()
    out = []
    for x in oovs:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="pyttsfrontend outputs jsonl")
    ap.add_argument("--b", required=True, help="baseline outputs jsonl")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--minlen", type=int, default=20)
    ap.add_argument("--only_special", action="store_true",
                    help="Only keep sentences containing digits or typical frontend phenomena.")
    args = ap.parse_args()

    A = list(load_jsonl(Path(args.a)))
    B = list(load_jsonl(Path(args.b)))
    n = min(len(A), len(B))

    picked = []
    for i in range(n):
        raw = (A[i].get("raw_text") or "").strip()
        if len(raw) < args.minlen:
            continue
        if args.only_special:
            if not (any(ch.isdigit() for ch in raw) or "$" in raw or "%" in raw or "-" in raw or "/" in raw
                    or "Dr." in raw or "Mr." in raw or "Mrs." in raw or "U.S." in raw or "e.g." in raw):
                continue
        picked.append(i)
        if len(picked) >= args.k:
            break

    for idx in picked:
        a = A[idx]
        b = B[idx]
        raw = a.get("raw_text")
        norm = a.get("normalized_text")
        ipa_a = a.get("meta", {}).get("ipa_sentence")
        ipa_b = b.get("meta", {}).get("ipa_sentence")
        oovs = extract_oov_arpabet(a)

        print("=" * 88)
        print(f"RAW : {raw}")
        print(f"NORM: {norm}")
        print(f"IPA (pyttsfrontend): {clip(ipa_a, 120)}")
        print(f"IPA (baseline)     : {clip(ipa_b, 120)}")
        print(f"ARPAbet OOV tokens : {oovs}")

if __name__ == "__main__":
    main()
