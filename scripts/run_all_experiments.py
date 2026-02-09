from __future__ import annotations
import subprocess
from pathlib import Path
import sys

def run(cmd: list[str]):
    print("\n> " + " ".join(cmd))
    r = subprocess.run(cmd, check=False)
    if r.returncode != 0:
        raise SystemExit(r.returncode)

def main():
    root = Path(__file__).resolve().parents[1]
    data_in = root / "data" / "wikitext_textonly.jsonl"
    suite_in = root / "data" / "frontend_suite_30.jsonl"

    results_main = root / "results" / "main"
    results_suite = root / "results" / "suite30"
    tables = root / "results" / "tables"

    results_main.mkdir(parents=True, exist_ok=True)
    results_suite.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)

    # (A) prepare suite (if not exists)
    if not suite_in.exists():
        run([sys.executable, str(root / "scripts" / "make_frontend_suite.py"),
             "--in", str(data_in),
             "--out", str(suite_in),
             "--max", "30"])

    # (B) main benchmark outputs (pyttsfrontend only)
    run([sys.executable, str(root / "scripts" / "run_benchmark.py"),
         "--in", str(data_in),
         "--out", str(results_main / "frontend_outputs.jsonl")])

    run([sys.executable, str(root / "scripts" / "eval_coverage.py"),
         str(results_main / "frontend_outputs.jsonl")])

    # (C) 2-way compare on main N=200
    run([sys.executable, str(root / "scripts" / "run_compare.py"),
         "--in", str(data_in),
         "--outdir", str(results_main),
         "--max", "200"])

    run([sys.executable, str(root / "scripts" / "compare_stats.py"),
         "--a", str(results_main / "pyttsfrontend.jsonl"),
         "--b", str(results_main / "phonemizer_only.jsonl")])

    # (D) 3-way compare on suite N=30
    run([sys.executable, str(root / "scripts" / "run_compare3.py"),
         "--in", str(suite_in),
         "--outdir", str(results_suite),
         "--max", "30"])

    run([sys.executable, str(root / "scripts" / "compare_stats3.py"),
         "--a", str(results_suite / "pyttsfrontend.jsonl"),
         "--b", str(results_suite / "phonemizer_only.jsonl"),
         "--c", str(results_suite / "num2words_only.jsonl")])

    # (E) sample cases outputs (store as text files for dissertation)
    sample2 = tables / "sample_cases_2way.txt"
    sample3 = tables / "sample_cases_3way.txt"

    with sample2.open("w", encoding="utf-8") as f:
        subprocess.run([sys.executable, str(root / "scripts" / "sample_cases.py"),
                        "--a", str(results_main / "pyttsfrontend.jsonl"),
                        "--b", str(results_main / "phonemizer_only.jsonl"),
                        "--k", "10", "--only_special"],
                       stdout=f, check=False)

    with sample3.open("w", encoding="utf-8") as f:
        subprocess.run([sys.executable, str(root / "scripts" / "sample_cases3.py"),
                        "--a", str(results_suite / "pyttsfrontend.jsonl"),
                        "--b", str(results_suite / "phonemizer_only.jsonl"),
                        "--c", str(results_suite / "num2words_only.jsonl"),
                        "--k", "15", "--only_special"],
                       stdout=f, check=False)

    print("\nAll experiments finished.")
    print("Tables:", tables)

if __name__ == "__main__":
    main()
