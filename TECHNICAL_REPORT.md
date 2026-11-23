# PRIVTRACE v0.2
## Online disclosure planning under uncertain future requests
Private technical report · 23 November 2026

### Abstract
An agent can make a permissible disclosure now and thereby lose the ability to meet a later request safely. We studied that decision using synthetic workflows in which an early transmission expires before the final job ticket opens. An online planner learned from past jobs which public dispatch cues predicted the need for an early or late receipt. On 384 held-out jobs with accurate metadata, it completed 206 safely, against 158 for greedy disclosure and 156 for conservative disclosure. A foresighted safe comparator completed 234. When metadata degraded, current evidence checks eliminated 125 observed exposure cases relative to unchecked planning, while denying some legitimate work. On 384 transfer jobs with a changed cue–demand relationship, the learned rule lost its advantage. An exploratory estimator using only closed tickets partially recovered during the shift, then lagged when the environment changed back. These are measurements of a specified synthetic decision problem, with complete traces and independently implemented replay.

### Research question
When should an agent use a short-lived opportunity to send fragment A, knowing that the recipient might later need fragment B, and that observing both reveals a protected attribute? The answer should depend only on the actual observation prefix. A strategy that consults the next request tests a different question.

### Relation to v0.1
The previous release found 132/144 exposed workflows under contextual local controls and zero under history-and-lineage controls. Completion fell from 115 to 74. The later scheduling intervention supplied the future receipt requirement directly. In v0.2 we retained the original adjudicator, isolated the planner, introduced an early opportunity that sometimes matters for task success, and made future requests uncertain. The attached historical archive passed all 72 checksums and all 12 tests. A fresh execution reproduced its 3,456 original scientific rows and traces. Historical outcomes are preserved separately.

### Evidence and scope
The primary protocol, generator and estimated model were frozen before evaluating the reserved blocks. Evidence includes 992 jobs, eight methods, two metadata regimes and 15,872 primary runs. A separately specified follow-up contributed 960 new jobs and 7,680 runs. There were no human participants, language-model inferences or paid calls.

<!-- page -->

## 1. Information model and experimental design
A dispatch job has an observable cue indicating an early or late booking. Its final ticket can require A, B, both or neither. A is available early only. B is delivered on request. The target and secondary public observer have separate histories. An observer with both matching slips can reconstruct the planted binary cohort by XOR. Some tasks require a document at a staff endpoint. The document can have restricted or routine ancestry. A true restricted document cannot be sent to a public endpoint; withdrawal also ends staff permission. Exact completion and safety are separate endpoints.

### Information at the decision boundary
The online function receives the tick, public cue, current offer and recipient, the recipient's delivered slip types, observed grant version, declared ancestry and current verification response if requested. No identifier, seed, future demand, upcoming notification time or gold value appears in the view. Verified methods can query a modeled authority about the present document and grant. All methods see the same underlying jobs, routes and candidate payloads. The oracle executes through a separate privileged branch. Future schedules exist inside the trusted driver. The test suite checks the interface and paired histories; it does not establish language-level sandboxing against malicious code.

### Development and transfer
Development used 128 jobs across four seeds. Validation used 96 jobs across three further seeds; no tuning followed. Test used 384 jobs over twelve further seeds. A separate museum-loan generator supplied 384 transfer jobs over twelve other seeds. Each museum block uses a finite booking and substitution manifest. Urgent loans are often reassigned to a courier, reversing the development association. This is an authored distribution shift, not external validation. Domain terminology, event times, prevalence of staff requirements, and metadata availability also differ.

### Delays and corrupted evidence
Jobs follow direct, relay or branched transport paths followed by recipient-side mediation. Router hops carry opaque payloads. Candidate messages may be in flight when a grant expires. In the degraded condition, each job has a notification lag, an honest, absent or inverted ancestry claim, and an availability flag for the independent verifier. The authoritative clock and true root exist only in the driver and evaluator. A checked control fails closed on unavailable proof. It can therefore refuse a legitimate document. The experiment models logical asynchronous arrivals and an atomic gateway decision; it does not benchmark network concurrency or actual verification latency.

<!-- page -->

## 2. Algorithms and prespecified analysis
The original contextual-local and full controls reuse the archived v0.1 authorization function. Full uses recipient history and declared ancestor restrictions. Local checks only the currently visible raw type and context; a document labeled as a digest does not inherit protection in this control. Both greedily propose all eligible transfers. Reserve uses full enforcement and withholds optional A at an empty target. An existing A is harmless to repeat in this threat model. An existing B causes the full gate to reject A.

### Online threshold rule
At an empty target, releasing A now enables an A-only task and prevents a B-only task. Reserving capacity does the reverse. Both-required and neither-required tickets cancel out of this local difference. Estimate the sign of P(A only | cue) minus P(B only | cue) using additive smoothing on completed development jobs. Send when the sign is positive, otherwise reserve. For early cues the smoothed counts were 38 to 5; for late cues, 17 to 39. The pooled estimator saw 54 to 43 and behaved like greedy disclosure. Correlation with staff feasibility or future grant changes could make the optimal threshold different. We do not assume this rule is globally optimal.

### Risk-aware checks and the oracle
Checked utility keeps the same online threshold and verifies the present ancestry and grant for each auxiliary document. Checked greedy isolates verification from planning. The offline oracle enumerates subsets of future candidate transfers, maximizing exact task completion subject to all gold privacy rules, then minimizing deliveries among successful subsets. On impossible jobs it sends nothing. An independent closed-form feasibility check verifies every ceiling. Unsafe completion can exceed that ceiling. This comparator is never callable through the online planner.

### Paired analysis
All controls face each job under each metadata regime. H1 and H2 compare online utility with full and reserve on clean in-family exact completion. H3 compares checked and unchecked utility on degraded in-family exposure. Each estimate is a paired risk difference. We resample the twelve independent test seed blocks 10,000 times with replacement. Two-sided 98.33% percentile intervals adjust for the three prespecified contrasts. These intervals quantify reweighting of these generator blocks. They do not quantify transfer uncertainty to human populations. Local protocol commits e32d4a2 and 3e9b899 record these decisions and the implementation. There was no external registration.

### Why perfect online utility is impossible here
Consider equal visible prefixes with an empty client history, no staff requirement and no restrictions on either fragment alone. One future asks for A and another asks for B. Sending A loses the B-only future under safe enforcement; withholding A loses the A-only future. Even a randomized policy cannot always match a foresighted planner across this pair. Prediction improves expected outcomes only while its cue remains informative.

<!-- page -->

## 3. Primary results
Each cell below is a count out of 384 dispatch test jobs. Safe completion requires an exact outcome and no unauthorized exposure anywhere in the run.

| Method | Clean safe | Degraded exact | Degraded safe | Degraded exposed |
|---|---:|---:|---:|---:|
| Contextual local | 52 | 384 | 52 | 332 |
| Greedy full | 158 | 170 | 115 | 125 |
| Conservative reserve | 156 | 174 | 110 | 125 |
| Utility-aware | 206 | 225 | 143 | 125 |
| Checked utility | 206 | 194 | 194 | 0 |
| No cue | 158 | 170 | 115 | 125 |
| Checked greedy | 158 | 147 | 147 | 0 |
| Safe offline oracle | 234 | 234 | 234 | 0 |

### Prespecified contrasts
H1 met its criterion. Online utility gained 60 and lost 12 jobs against full, for a net 48/384 or +12.50 percentage points (adjusted interval +8.33 to +15.89). H2 also met its criterion: 66 gained and 16 lost against reserve, +13.02 points (+9.11 to +17.71). H3 met its criterion: checked utility changed degraded exposure by −32.55 points (−39.06 to −26.82), from 125 to zero. Zero is an observation under this gate and verifier model. It does not establish security of deployed agents.

### Interpreting the denominators
Among 197 withdrawn dispatch jobs, unchecked utility had 70 with a post-withdrawal violation; checked utility had zero. Neither reconstructed a protected cohort on the degraded dispatch set because both retained per-recipient history. Contextual local allowed reconstruction in 345 of 768 public observer-workflows, all matching the synthetic truth. Local completed all 384 tasks, but only 52 safely. The safe oracle's 234 successes imply 150 tasks were infeasible under true permissions and initial holdings. With reliable metadata, 28 additional feasible jobs separated online utility from the oracle.

### Where the policy helps or costs a job
In dispatch-79-4 the late cue led utility to withhold optional A. The client later needed B and received it safely. Full had already sent A. In dispatch-83-5 the same cue preceded an A-only ticket and the online planner missed the opportunity. In dispatch-79-13 the auxiliary document was actually routine, staff required it, and current verification was unavailable. Checked utility blocked it and lost the job. Overall checked utility made 215 locally permissible denials in degraded dispatch. In 23 of its safely incomplete runs, changing one denial while fixing later deliveries would have enabled safe completion. These are retrospective, fixed-trace diagnostics.

<!-- page -->

## 4. Distribution shift, ablations and costs
On clean museum jobs, frozen utility completed 110/384 safely versus 134 for full, 147 for reserve and 191 for the oracle. Under degraded evidence, checked utility completed 89 safely and checked greedy completed 110. Unchecked utility completed 148 exactly but only 65 safely, exposing information in 217 jobs. The cross-domain result reverses the main planning comparison. It cautions against interpreting the dispatch estimates as a generally preferable policy.

### Disentangling scheduling and verification
On degraded dispatch, checked greedy yielded 147 safe completions. Holding verification fixed and enabling cue-aware scheduling increased this to 194. Holding scheduling fixed and adding verification increased safe completion from 143 to 194, while reducing exact completion from 225 to 194. Even when degraded ancestry labels happened to be honest, unchecked utility exposed information in 24/210 jobs; the corresponding values were 59/95 for inverted claims and 42/79 for unknown claims. Honest labels alone cannot identify an expired grant when the local clock view is stale.

### Learning from closed jobs
After seeing the transfer reversal we froze an exploratory protocol, then generated ten entirely new streams of 96 jobs each. Booking behavior changes twice within a stream. The estimator uses the last 16 closed tickets and a weak development prior. It receives no domain label or change notification. A separate verifier reconstructed its table before each prediction using only earlier tickets. In each period, 320 jobs faced each method and regime.

| Period | Clean frozen | Clean adaptive | Degraded frozen | Degraded adaptive |
|---|---:|---:|---:|---:|
| Initial dispatch | 184 | 184 | 167 | 167 |
| Museum transfer | 88 | 110 | 79 | 97 |
| Return to dispatch | 161 | 142 | 143 | 128 |

Numbers are safe completions. All four methods in this extension used current-evidence checking. The adaptive estimator recovered 22 completions in the clean shift period and lost 19 after the return shift. Clean greedy and reserve each reached 111 during transfer, one above adaptive. Across all three clean periods the adaptive gain over frozen was only three jobs out of 960. This is a diagnostic of adaptation lag, not evidence to deploy the rolling window universally. The approach assumes every final ticket becomes available after job closure, including failed jobs.

### Computational costs
The reference execution timed each method end to end, including view construction and trace capture, excluding scoring and storage. Across both regimes and all splits, median simulated job time was roughly 31 µs for utility and checked utility and 39 µs for the oracle. Separate allocation probes on 248 jobs per method measured median Python peaks near 4.8 KB for online methods. These are traced allocations, not process RSS. results/decision_cost.csv isolates repeated current-view decisions. The verification service is simulated; its real network or cryptographic overhead is unmeasured. Tokens and paid requests were zero.

<!-- page -->

## 5. Validation, limitations and evidence
Independent scoring code imported no planner, broker, generator or policy evaluator. It reconstructed violations and task outcomes from the delivered values, actual recipient paths and authoritative fixtures. It checked all 87,712 primary event records, matched every violation event ID and verified every oracle ceiling using a separate feasibility formula. It separately checked all 7,680 supplementary outcomes and the chronological construction of all rolling estimates. A separate isolated-interpreter replay reconstructed all 62,314 primary online actions and reason codes from the whitelisted current view and development counts alone. A clean replay reproduced both experiments' score tables and decompressed traces byte for byte. Timings were excluded. Fifteen v0.2 tests passed, including divergent-future prefix checks, counterfactual histories and grants, unavailable verification, XOR controls and feedback-window isolation.

### Threats to validity
The primary and transfer families were written within the same project. The transfer generator is independently specified from the dispatch sampler, with a deliberately changed relationship between cue and ticket. It is not an externally authored or independently human-validated benchmark. Tasks and labels share domain assumptions even where scoring code is independent. Duplicate abstract states across distinct seeds are expected. Cases use a small finite action alphabet, typed origins and two noncolluding public observers. Routes do not model an observer that gains access at an intermediate hop. Task payloads are synthetic tokens; a forbidden ancestry transfer does not demonstrate recovery of a real document or semantic fact. A true asynchronous race, a compromised verifier or a second hidden recipient identity would require a different experiment.

The oracle is exact for these finite tasks. It has no claim on real-world maxima. The causal comparison between planners holds within a synthetic job; comparisons between domains jointly vary several attributes. A prospective externally authored task family with additional independent information rather than reversed cues would be a stronger generalization test. An actual model-driven pilot was not run: no local generative chat checkpoint and inference binding were available within the project environment. Scripted simulation is the only measured backend. Independent human replication and language-level disclosure evaluation remain open.

### Position relative to prior work
Context-relative disclosure norms are established by Nissenbaum (2004). Myers and Liskov (1998) formalize per-principal information-flow controls. W3C PROV-DM supplies concepts for representing derivations. TG-CI/MAPLE-Bench already addresses recipient state and downstream graph scope; CI-RELAY already mediates agent relays. Prior work measures compositional leakage and the effect of stale memory. Online decision rules and prophet comparators are also established. The contribution here is a controlled empirical comparison under uncertain demand and imperfect current evidence, with an explicit impossibility pair, a reversed transfer result and a fully replayable evaluation. Primary-source links and the methodological audit are in docs/AUDIT.md.

### Evidence for a selection committee
The defensible application claim is that conditional online planning improved safe completion on the in-family test while a designed transfer shift reversed that benefit. Verification improved measured privacy under modeled metadata faults and could also deny useful work. No experiment in this release establishes external validity, clinical applicability or a guarantee of zero disclosure. The accompanying archive includes the locked protocols, source, datasets, machine-readable outcomes, full decision histories, statistical analysis and independent reproduction instructions.

<!-- page -->

## Primary sources and reproducibility record
Nissenbaum, H. (2004). Privacy as Contextual Integrity. Washington Law Review 79, 119. https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/

Myers, A. C. and Liskov, B. (1998). Complete, Safe Information Flow with Decentralized Labels. IEEE Symposium on Security and Privacy. https://www.cs.cornell.edu/andru/papers/sp98/paper.html

W3C (2013). PROV-DM: The PROV Data Model. W3C Recommendation. https://www.w3.org/TR/prov-dm/

Judging Before Propagation: Task-Graph Contextual Integrity for Multi-Agent Privacy (2026). arXiv:2610.39532. https://arxiv.org/abs/2610.39532

Hu et al. (2026). CI-RELAY: Contextual Integrity Mediation for Privacy in LLM-based Multi-Agent Systems. Findings of EMNLP. https://aclanthology.org/2026.findings-emnlp.2421/

The Sum Leaks More Than Its Parts (2025). Compositional disclosure study. arXiv:2509.14284. https://arxiv.org/abs/2509.14284

Revoked but Still Authoritative (2026). Soft revocation in agent memory. arXiv:2609.08258. https://arxiv.org/abs/2609.08258

Kleinberg, R. and Weinberg, S. M. (2012). Matroid Prophet Inequalities. https://arxiv.org/abs/1201.4764

### Audit trail
The archive contains configs/study.json and configs/adaptive.json, each dataset, the development count table, Git history, paired per-job scores, candidate decision views, signed direction of each primary contrast and the separate replay outputs. The primary score file SHA-256 starts 72e7c719779253e2. The complete SHA-256 manifest and REPRODUCE.md accompany the release. All evidence was produced within this project; no external auditor has signed off on it.
