# PRIVTRACE
## When can sharing less help a team finish its work?
Final research summary · University of Göttingen application · November 2026

### Question
A message can be appropriate for its recipient now, yet prevent a later exchange that the team needs. A second message can also identify a protected fact without naming it. PRIVTRACE studies these mechanisms in synthetic collaborative workflows with changing permissions, named recipients and inspectable decision histories.

### Three experiments
In v0.1, tracking history and lineage reduced exposed workflows from 132/144 to zero but lowered completion from 115 to 74. In v0.2, a planner using only a visible booking cue improved safe completion from 158/384 to 206/384 in dispatch; on a museum transfer task it fell from 134 to 110. Both outcomes raised a question for the final study: could the visible structure of the work guide the early choice more reliably?

In v0.3, a team needs one or two early signatures and later certificates from reviewers whose assignments have not yet been revealed. Early and late documents disclose different attributes of a fictional site. A public mailbox receiving both may identify the site. The new planner preferentially assigns early work outside the pool currently eligible for later certification.

| Clean held-out result | Safe completions / 288 |
|---|---:|
| Greedy disclosure | 13 |
| Fixed-order minimum quorum | 85 |
| Earlier cue adapted to new task | 84 |
| Current eligibility | 106 |

The gain over fixed-order quorum was 7.3 percentage points (adjusted paired interval +3.5 to +12.5). A later mailbox handoff reversed the comparison in that subgroup: 22 versus 33 safe completions in 96 jobs.

<!-- page -->

## What happens when the evidence is wrong?
Under combined local metadata faults, checking current evidence reduced exposed jobs from 212/288 to zero. Safe completions fell from 65 to 64 because the gate sometimes had to decline useful work when it could not verify the evidence. When the verifier could return incorrect positive evidence, exposure reappeared in 51/288 jobs. Protection depended on evidence quality as well as the enforcement rule.

### Words can change what a recipient knows
A recipient who knows that a site is coastal can identify it from a second message establishing that it lies outside the southern district. A literal detector missed 72 of 108 identifying contexts in a controlled language test. A dictionary that accounted for composition and some negation missed 30. An independently implemented character-based classifier also made errors and abstained. Ambiguous references were retained for human review.

### Evidence available to reviewers
The final evaluation paired eight policies and seven metadata conditions across 408 synthetic jobs, including 288 held-out jobs. A second scoring implementation checked all 22,848 runs and 162,848 events. The scientific results reproduced in a fresh Python environment. The source, measured outcomes, analysis, provenance and reproduction instructions are preserved in the private research archive.

The evidence supports a conditional conclusion. Planning with current recipient information can preserve future collaboration, but its value diminishes when assignments move, semantic judgments fail or verification becomes unreliable. All workflows were scripted and internally authored. There were no real personal records, generative-model trials, human semantic ratings or external replications.
