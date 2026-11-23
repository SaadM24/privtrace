# PRIVTRACE — Privacy-aware information sharing in multi-agent workflows

**Research software and reproducible synthetic experiments · final v0.3 release (November 2026)**

PRIVTRACE studies when an individually permissible disclosure can cause a later collaboration task to become impossible without exposing protected information. It evaluates recipient history, data provenance, revocation, online disclosure planning, unreliable verification and indirect information disclosure in controlled multi-agent workflows.

> **Scope:** All measured workflow agents were **scripted** and all task data are **synthetic**. This repository does **not** establish real-world privacy guarantees, externally validated generalisation, or performance on generative LLM agents. The optional local LLM pilot is **implemented but not executed** in the final research release.

## Key measured findings

| Experiment | Measured outcome | Boundary / counterexample |
|---|---|---|
| v0.1 — history + lineage | Exposed workflows dropped from 132/144 to 0/144 | Exact task completion dropped from 115/144 to 74/144 |
| v0.2 — cue-aware online planner | Safe completion improved from 158/384 to 206/384 dispatch jobs | On a designed museum shift, it fell from 134/384 to 110/384 |
| v0.3 — current eligibility planning | 106/288 safe completions vs 85/288 for a fixed-order quorum | Later mailbox handoff reversed the result: 22 vs 33 of 96 jobs |
| v0.3 — evidence verification | Measured exposure under combined metadata faults: 212/288 to 0/288 | Incorrect positive attestations yielded 51/288 exposures; safe completion dropped from 65 to 64 with verification |
| v0.3 — indirect language disclosure | Literal matching missed 72/108 identifying contexts; a compositional dictionary missed 30/108 | These are internally authored controlled-language contexts, not human-validated semantic judgments |

The v0.3 experiment contains **22,848 paired policy-condition runs** across 408 synthetic jobs (including 288 held-out jobs) and **162,848 logged events**. Do not treat the 56 policies/conditions per job as independent samples. Main findings were checked with a separately implemented scorer and reproduced in a fresh environment within the project; **no external replication** is claimed.

## Research documents

- [Two-page Göttingen selection committee summary](v03/papers/PRIVTRACE_v03_Research_Summary.pdf)
- [Six-page final technical report](v03/papers/PRIVTRACE_v03_Technical_Report.pdf)
- [Research methodology](v03/METHODOLOGY.md)
- [Protocol and evaluation controls](v03/docs/PROTOCOL.md)
- [Prior-work audit and limitations](v03/docs/AUDIT.md)
- [Reproduction instructions](REPRODUCE.md)

## Repository map

| Path | Purpose |
|---|---|
| `src/privtrace02/`, `src/privtrace03/` | Online policies, simulation, test-world construction and evaluation |
| `v03/run.py`, `v03/semantics.py` | Generate synthetic scenarios, paired runs and controlled-language measurements |
| `v03/verify_study.py`, `v03/views.py` | Independent score reconstruction and observation-only decision replay |
| `v03/analyze.py`, `v03/compare.py` | Analysis and comparison with preserved measured outputs |
| `v03/results/main/` | Published synthetic fixtures, traces, paired scores, analysis and plots |
| `tests/`, `v03/tests/` | Automated regression and methodological tests |
| `v03/papers/` | Study summaries for scientific review |

## Quick start

Python **3.11+** is required; the recorded environment used Python **3.12** on Linux. Refer to [REPRODUCE.md](REPRODUCE.md) for complete instructions.

```bash
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

## Research transparency and limitations

The datasets, controlled utterances and ground-truth policies were created internally. The observed zero exposures are conditional on the explicitly tested rules and trustworthy successful evidence, **not** an assurance of secure deployment. Cases involving human social inference, collusion, real asynchronous systems, external benchmarks and actual generative-agent behaviour remain unvalidated.

This repository is a **sanitised publication copy** with fresh public history. It excludes the original private release archives, private Git bundles and coordinator answer files. These private materials remain in the author's owner archive. The published synthetic results are suitable for reproducibility but must not be given as answer-free material to blinded human reviewers.

Development and implementation used AI assistance; the evidence should be evaluated on its experimental methods and reproducibility, not on any claim of unaided authorship. The research release has not been peer-reviewed.

**License:** No open-source license has been selected for this GitHub snapshot; public visibility does not itself grant redistribution or modification rights.
