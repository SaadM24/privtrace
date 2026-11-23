# PRIVTRACE v0.3 reproduction
Use the private owner archive for executable code and complete evidence. Unzip it, open a shell inside PRIVTRACE-v0.3, and run these commands there. Numerical packages were tested on 64-bit CPython 3.12.14 under Linux. The package requires Python 3.11 or later; use 3.12 for the pinned numerical stack. No external account, model or network is needed after installing dependencies.

    python v03/verify_manifest.py
    python -m venv .venv
    # Linux/macOS: source .venv/bin/activate
    # Windows PowerShell: .\.venv\Scripts\Activate.ps1
    python -m pip install -r v03/requirements.txt
    python -m pip install --no-build-isolation --no-deps -e .
    python -m unittest discover -s tests -v
    python -m unittest discover -s v03/tests -v
    python v03/run.py --out replay
    python v03/semantics.py --out replay
    python v03/verify_study.py --out replay
    python v03/feasibility.py --out replay
    python v03/analyze.py --out replay
    python v03/compare.py v03/results/main replay
    python v03/views.py

The runner requires a fresh destination. Keep prior output intact on retry by choosing another directory. compare.py normalizes line endings and gzip headers; the reference clean replay also checked raw decompressed bytes on Linux. Timings and PDF metadata may differ. views.py operates on sealed primary traces and uses a separate Python interpreter. Source controls and generation are in src/privtrace03; the frozen v0.2 cue function and development counts are in src/privtrace02 and data/table.json. Git history through the final source commit is in history-v03.bundle. Clone it locally with git clone history-v03.bundle source-history. Large archival evidence is distributed in the owner ZIP. Earlier v0.2 reproduction commands belong to that archived release.

Reference results, tests, SHA-256 preservation checks and clean replay hashes are in v03/results/. The fresh virtual environment used preinstalled numerical wheels via system-site-packages. This tests reproducibility on this host, not a second OS. Only Linux was exercised. The file-lifetime regression is intended for Windows runners too. For publication or an external claim, repeat on a separately managed machine.

To rebuild presentation materials in a scratch copy:

    python v03/render.py --out regenerated-papers
    python v03/review_packet.py

The review generator writes an owner-only scoring key under v03/results. Give human annotators the instructions and blank cards only.

## Optional local language-model pilot
A matching locally licensed chat GGUF and compatible llama-cpp-python binding are required. No checkpoint, chat runtime or inference server was available in the project environment. Hosted model services were unused. With an independently obtained model, run:

    python v03/pilot.py --model /path/to/chat-model.gguf --n 12 --out pilot-private.jsonl

The harness calls actual local generation once per case, records settings, prompt, model hash and response, and pairs two gates on that same reply. Arbitrary language outside the strict grammar remains unresolved. The acknowledgement marker is a limited task proxy. Blind human readers should rate unrestricted replies before reporting semantic exposure, and invalid or unresolved cases must remain in the accounting. Unit tests cover scoring fixtures only. This command was not executed with weights.
