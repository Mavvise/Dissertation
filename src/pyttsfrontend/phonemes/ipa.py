from __future__ import annotations
from typing import Optional
import subprocess
import shutil

def _find_espeak_cmd() -> Optional[str]:
    # Prefer espeak-ng; fallback to espeak (your wrapper points to NG anyway)
    for cmd in ["espeak-ng", "espeak"]:
        p = shutil.which(cmd)
        if p:
            return p
    return None

def try_phonemize(text: str, language: str = "en-us") -> Optional[str]:
    """
    IPA via eSpeak/eSpeak-NG CLI.
    This avoids phonemizer's Windows auto-detection issues.
    Returns None on failure.
    """
    cmd = _find_espeak_cmd()
    if not cmd:
        return None

    # Map language to espeak voice codes (minimal set for MVP)
    # en-us -> en-us, en -> en, etc.
    voice = language.lower()

    # eSpeak output:
    # -x : phoneme output (eSpeak phonemes, not IPA)
    # --ipa : IPA output (supported by eSpeak NG)
    # -q : quiet
    # -v : voice
    #
    # We use --ipa=3 for more IPA detail (you can tune later).
    args = [cmd, "-q", "-v", voice, "--ipa=3", text]

    try:
        res = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode != 0:
            return None

        out = (res.stdout or "").strip()
        # Some builds may print to stderr; use stdout first, fallback to stderr.
        if not out:
            out = (res.stderr or "").strip()

        out = out.strip()
        return out if out else None
    except Exception:
        return None
