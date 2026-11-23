# Reproduce PRIVTRACE v0.3 from the GitHub publication snapshot

This repository is the sanitised public-facing snapshot, not the complete owner archive. It includes the full v0.3 executable source, synthetic fixtures, frozen reference results, traces and tests. Historical owner-only archives, raw Git bundles and blinded-review answer keys are deliberately excluded.

**Environment:** Python 3.11+; the recorded scientific environment used CPython 3.12 on Linux. Windows execution was not validated during the original release. The reference environment is documented in `v03/results/environment.json`.

```bash
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
```

Run from the repository root. `replay` must not already exist. A new output name is recommended for repeat executions. `compare.py` compares 10 scientific artifacts, normalising line endings and gzip headers; timings and PDF metadata may vary. `v03/views.py` checks the retained reference event traces against policies in an isolated interpreter using whitelisted current observations.

To regenerate research-paper renderings in a separate directory:

```bash
python v03/render.py --out regenerated-papers
```

The optional `v03/pilot.py` requires a separately obtained, properly licensed chat GGUF and compatible `llama-cpp-python` binding. This pilot did **not** execute as part of the v0.3 scientific evidence; do not cite it as an empirical result. `v03/review_packet.py` can recreate a private coordinator answer key—never commit the generated `v03/results/coordinator.jsonl` or distribute it to annotators.

The original v0.1 and v0.2 owner archives were preserved and verified in the private owner release. They are intentionally not included in this public snapshot; their historical checksum-preservation claims cannot be re-verified using this sanitised package alone.
