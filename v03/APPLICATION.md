# PRIVTRACE application material

## Three CV bullets
- Evaluated online disclosure planning across 288 held-out synthetic quorum workflows. Using current reviewer eligibility raised safe completions from 85 to 106 against a fixed-order quorum baseline, with a reversal under mailbox handoff.
- Tested delayed grants, missing recipient history, inverted lineage and unreliable verification. Current checks reduced exposed jobs from 212/288 to zero under mixed faults; incorrect attestations produced 51 exposed jobs.
- Compared three detectors on 195 determinate natural-language recipient contexts and preserved 22,848 paired workflow runs with replayable traces and independently implemented scoring.

## Significance
The decision to share information depends on who already knows what and who may need to act next. PRIVTRACE makes those dependencies observable and measures the cost of withholding information alongside the cost of disclosure. Its strongest case is a conditional finding that can be inspected and challenged.

## Proposed cover-letter paragraph
PRIVTRACE shaped my interest in privacy as a problem of coordination. In a synthetic workflow, an individually permissible message could prevent a later collaborator from receiving the evidence needed to finish a task. Using current reviewer eligibility improved safe completion from 85 to 106 of 288 held-out jobs, yet that advantage reversed when a handoff changed the recipient mailbox. I would like to investigate how privacy systems represent changing context, how much trust their decisions place in provenance, and how to evaluate disclosures that emerge across messages. Those questions are what draw me to doctoral research on privacy at Göttingen.

## Five-minute interview outline
| Time | Message | Evidence to show |
|---|---|---|
| 0:00–0:45 | Explain two harmless fragments and one identifying intersection using the four-site map. | Coastal leaves Alder or Cedar. Outside the southern district leaves Alder. |
| 0:45–1:30 | Explain why a safe gate alone can still lose utility. | v0.1 completion 115 versus 74; a later receipt could not be delivered safely. |
| 1:30–2:30 | Explain online observation boundaries and the new quorum task. | Known eligible pool, hidden later assignment, identical observation-prefix tests. |
| 2:30–3:35 | Show one positive result beside its counterexample. | 106 versus 85 overall; 22 versus 33 under handoff. |
| 3:35–4:30 | Explain the verifier boundary and semantic misses. | Zero exposed under honest mixed verification; 51 when positive evidence can be wrong. |
| 4:30–5:00 | Explain what remains uncertain. | Internal synthetic benchmarks, no human semantic ratings or generative-agent study. |

## Likely questions
**How do you know the online policy did not read future requests?** The schedule consumes a small immutable opening view. The later assignments are outside it. Mutating future fields preserves earlier decisions in regression tests. An isolated interpreter also reconstructed actions from recorded views alone.

**Does the policy simply block everything?** No. Under clean metadata it completed 106 tasks safely; it failed to complete 56 other jobs for which a safe schedule existed. Under mixed metadata verification reduced exposure dramatically but yielded one fewer safe completion than the unchecked method.

**What exactly do you mean by semantic evaluation?** Each synthetic statement has an authored set of possible sites. The labeled task is whether this recipient's previously possible sites collapse to one. We compared detectors against that construct and left ambiguous references unresolved. This gives no measured human agreement.

**What is the strongest counterexample?** In test-347-14 an early vote went to a mailbox later used for certification after a handoff. Its two messages would identify the site, so certification was blocked. A simpler fixed order completed it safely.

**Were these real LLM agents?** The measured workflow agents were scripted. A character n-gram classifier was trained and tested for semantic interpretation. A local generative pilot harness exists; it was not run with model weights.

**What was your personal contribution?** Describe only implementation, review and reproduction work you personally performed. The project was implemented with AI assistance. Distinguish your design decisions and interpretation from generated code and automatic verification.
