# PRIVTRACE v0.2
## When should an agent withhold information it may legally share?
Private research summary · University of Göttingen application · November 2026

### The research question
An agent has one early chance to deliver fragment A. Later a client may need fragment B. Each is individually permitted, but together they reveal a protected attribute. Can the agent decide before seeing the request and still complete useful work? An earlier PRIVTRACE experiment relied on knowing the future receipt requirement. This study removes that information from the planner's interface.

### What was built and tested
A CPU-only framework pairs each workflow across online policies and an offline upper bound. The planner sees the current request, a public booking cue, the recipient's history and the evidence available at that instant. It never sees the future ticket. The experiment covers separate development, validation and evaluation seeds, plus a separately designed transfer family. Tests give the planner identical histories followed by different futures and check that its earlier decisions remain identical.

### Results with reliable current information
| Method | Dispatch safe completions | Museum safe completions |
|---|---:|---:|
| Greedy history-and-lineage control | 158 / 384 | 134 / 384 |
| Conservative online control | 156 / 384 | 147 / 384 |
| Cue-aware online planner | 206 / 384 | 110 / 384 |
| Foresighted safe upper bound | 234 / 384 | 191 / 384 |

On held-out dispatch jobs, the online planner improved safe completion by 12.5 percentage points against greedy disclosure. The adjusted paired interval was +8.3 to +15.9 points. The same rule lost to both simple controls on museum jobs, where booking urgency predicted a different requirement. The evidence supports a conditional benefit.

<!-- page -->

## What changed when privacy metadata became unreliable?
A document can inherit restricted status from its source. A delayed grant update or a wrong ancestry label can cause a gateway to release it improperly. The checked planner requests current verification when processing a document and blocks delivery if evidence is unavailable.

| Degraded dispatch jobs | Unchecked planner | Checked planner |
|---|---:|---:|
| Jobs with an unauthorized exposure | 125 / 384 | 0 / 384 |
| Jobs completed exactly | 225 / 384 | 194 / 384 |
| Jobs completed exactly and safely | 143 / 384 | 194 / 384 |

Verification improved safe completion while rejecting some legitimate work. In one traced job, the staff document was routine and necessary, but its status could not be verified at the decision time. The model assumes accurate evidence when verification succeeds; zero observed violations is conditional on that assumption.

### Can the planner adapt?
A separate prospective follow-up allowed the planner to learn only from jobs that had already closed. In fresh streams, it recovered 22 safe completions over a frozen planner during a shift, then lost 19 when the original pattern returned. This shows both the value and the cost of using recent feedback.

### What a reviewer can verify
The private archive preserves the v0.1 release, v0.2 implementation, prospectively locked protocols and complete decision traces. A second implementation rescored all 15,872 primary runs. The 7,680 follow-up runs also passed replay checks, and both sets of scientific outputs reproduced byte for byte. All 15 v0.2 automated tests passed.

These results concern scripted agents, synthetic records, explicit privacy rules and a defined two-fragment inference. The transfer family was designed within the project. External replication, natural-language leakage evaluation and an LLM-agent trial remain open.
