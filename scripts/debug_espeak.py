import os
import shutil
from pathlib import Path

print("=== PATH contains espeak? ===")
print("shutil.which('espeak')    =", shutil.which("espeak"))
print("shutil.which('espeak-ng') =", shutil.which("espeak-ng"))

print("\n=== Common locations ===")
cands = [
    r"C:\Program Files\eSpeak NG\espeak-ng.exe",
    r"C:\Program Files\eSpeak NG\espeak.exe",
    r"C:\Program Files\eSpeak NG\espeak-ng-data",
    r"C:\Program Files\eSpeak NG\espeak-ng-data\phondata",
]
for p in cands:
    print(p, "=>", Path(p).exists())

print("\n=== Try running executables ===")
for exe in ["espeak-ng", "espeak"]:
    try:
        out = os.popen(f'"{exe}" --version').read().strip()
        print(exe, "--version =>", out[:120])
    except Exception as e:
        print(exe, "failed:", repr(e))

print("\n=== phonemizer version ===")
try:
    import phonemizer
    print("phonemizer", phonemizer.__version__)
except Exception as e:
    print("phonemizer import failed:", repr(e))

print("\n=== Try EspeakBackend (direct) ===")
try:
    from phonemizer.backend import EspeakBackend
    print("EspeakBackend imported OK:", EspeakBackend)
except Exception as e:
    print("EspeakBackend import failed:", repr(e))

print("\n=== Try phonemizer.phonemize (espeak backend) ===")
try:
    from phonemizer import phonemize
    print(phonemize("Hello world", language="en-us", backend="espeak", strip=True))
except Exception as e:
    print("phonemize failed:", type(e).__name__, str(e))

print("\n=== Try EspeakBackend with explicit paths ===")
try:
    from phonemizer.backend import EspeakBackend
    text = "Hello world"
    espeak_ng = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
    data_path = r"C:\Program Files\eSpeak NG\espeak-ng-data"
    # Try common keyword names used in different phonemizer versions
    tried = []
    for kwargs in [
        dict(language="en-us", espeak_path=espeak_ng, data_path=data_path),
        dict(language="en-us", espeak_path=espeak_ng, espeak_data_path=data_path),
        dict(language="en-us", path=espeak_ng, data_path=data_path),
        dict(language="en-us", path=espeak_ng, espeak_data_path=data_path),
    ]:
        tried.append(kwargs)
        try:
            backend = EspeakBackend(**kwargs)
            res = backend.phonemize([text], strip=True)[0]
            print("SUCCESS with kwargs:", kwargs)
            print("RESULT:", res)
            break
        except Exception as e:
            print("FAIL with kwargs:", kwargs, "=>", type(e).__name__, str(e))
except Exception as e:
    print("Explicit backend attempts failed:", type(e).__name__, str(e))
