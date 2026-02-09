# pyTTSFrontend — Dissertation Code Repository

This repository contains the full experimental codebase accompanying the MSc dissertation:

**Revisiting Text Frontends in Modern Text-to-Speech Systems:  
A Modular Python Implementation and Comparative Study**

---

## Overview

This project investigates the role of **text frontends** in modern Text-to-Speech (TTS) systems.
Rather than focusing on acoustic modeling, it isolates and evaluates **frontend text processing pipelines**, including:

- Text normalization
- Linguistic preprocessing
- Pronunciation generation
- Dictionary coverage and OOV analysis

The core contribution is **pyTTSFrontend**, a modular and extensible Python-based frontend designed for
**transparency, reproducibility, and research-oriented evaluation**.

---

## Repository Structure

```
.
├── data/
│   └── wikitext_textonly.jsonl        # Text-only evaluation dataset
│
├── results/
│   ├── main/
│   ├── suite30/
│   ├── results_suite/
│   └── results_suite3/
│
├── scripts/
│   ├── prepare_dataset.py             # Dataset preparation
│   ├── run_benchmark.py               # Run pyTTSFrontend pipeline
│   ├── run_compare.py                 # Two-way comparison
│   ├── run_compare3.py                # Three-way comparison
│   ├── compare_stats.py               # Quantitative stats (2 systems)
│   ├── compare_stats3.py              # Quantitative stats (3 systems)
│   ├── sample_cases.py                # Qualitative examples (2 systems)
│   ├── sample_cases3.py               # Qualitative examples (3 systems)
│   ├── eval_coverage.py               # Dictionary & IPA coverage
│   └── debug_espeak.py                # IPA backend diagnostics
│
├── src/pyttsfrontend/
│   ├── pipeline.py                    # Main frontend pipeline
│   ├── cli.py                         # Command-line interface
│   ├── schema.py                      # Output schema
│   ├── components/
│   │   ├── normalizer.py              # Text normalization
│   │   └── spacy_nlp.py               # Linguistic analysis
│   ├── phonemes/
│   │   ├── arpabet.py                 # ARPAbet utilities
│   │   └── ipa.py                     # IPA generation (eSpeak backend)
│   └── baselines/
│       ├── phonemizer_only.py         # Baseline: phonemizer-only
│       └── num2words_only.py          # Baseline: num2words-only
│
├── requirements.lock.txt
├── python_version.txt
└── README.md
```

---

## Installation

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate   # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.lock.txt
pip install -e .
```

### 3. Install eSpeak-NG (IPA backend)

On Windows (recommended):

```bash
winget install eSpeak-NG.eSpeak-NG
```

Ensure `espeak` or `espeak-ng` is available in `PATH`.

---

## Reproducing Experiments

### Prepare dataset

```bash
python scripts/prepare_dataset.py --max 200 --streaming --out data/wikitext_textonly.jsonl
```

### Run frontend pipeline

```bash
python scripts/run_benchmark.py --in data/wikitext_textonly.jsonl --out results/main/frontend_outputs.jsonl
```

### Run baselines and comparisons

```bash
python scripts/run_compare3.py --in data/wikitext_textonly.jsonl --outdir results/results_suite3
```

### Quantitative evaluation

```bash
python scripts/compare_stats3.py \
  --a results/results_suite3/pyttsfrontend.jsonl \
  --b results/results_suite3/phonemizer_only.jsonl \
  --c results/results_suite3/num2words_only.jsonl
```

### Qualitative case studies

```bash
python scripts/sample_cases3.py \
  --a results/results_suite3/pyttsfrontend.jsonl \
  --b results/results_suite3/phonemizer_only.jsonl \
  --c results/results_suite3/num2words_only.jsonl \
  -k 15 --only_special
```

---

## Notes

- All evaluations are conducted at the **text and phonetic representation level**.
- The modular design allows easy integration of additional components such as
  CMUdict variants, pysle, or neural G2P models.

---

## License

This repository is provided for academic and research purposes.


