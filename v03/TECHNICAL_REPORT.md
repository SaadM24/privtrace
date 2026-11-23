# PRIVTRACE
## Privacy-aware planning across changing workflows
Final technical report · Private research release v0.3 · 23 November 2026

### Abstract
A disclosure can be permissible now and still prevent safe completion of a later task. We investigated that conflict across three releases. The first established the cost of locally reasonable disclosures. The second showed that a public booking cue could guide an online planner, but the advantage reversed on transfer. The final study replaces a single expiring opportunity with a quorum of interchangeable reviewers, an uncertain later assignment and a shared or changing recipient mailbox. On 288 held-out scripted jobs, a planner using current eligibility completed 106 safely, compared with 85 for a fixed-order quorum planner, 84 for an adapter using the earlier learned cue and 13 for greedy disclosure. However, the eligibility rule lost to fixed order when a later handoff changed the relevant mailbox.

When metadata was unreliable, current verification eliminated 212 measured exposure cases yet reduced safe completions from 65 to 64. Incorrect attestations produced 51 exposed jobs. A separate controlled-language assay found that literal matching missed 72 of 108 identifying contexts and a compositional dictionary missed 30. Human validation and real generative inference remain open. The study supplies a reproducible mechanism for examining where a privacy claim depends on the workflow, the observer, and the reliability of evidence.

### Reading the evidence
A safe completion requires the entire job to succeed with no defined unauthorized delivery. Exposure is measured at recipient boundaries. The strongest conclusions concern repeatable behavior of the supplied software under the specified rules. The study cannot estimate privacy failure rates in real organizations. Independent scoring code and deterministic replay are internal verification. Neither is external scientific replication.

### Research questions
RQ1 asks whether planning gains transfer to a different task structure. RQ2 asks when indirect wording or previously received messages identify a site. RQ3 measures how missing or incorrect evidence changes enforcement. RQ4 asks whether present-time workflow structure can guide a planner without consulting the future job assignment.

<!-- page -->

## 1. Prior evidence and design
In v0.1, tracking recipients and lineage reduced exposed held-out workflows from 132/144 to zero but cut exact completion from 115 to 74. Sending an optional fragment could make delivery of a later required receipt impermissible. An exploratory intervention recovered utility when told which future receipt was required. The follow-up verified the mechanism, but could not establish that an online planner would know when to intervene.

In v0.2, a development-only forecast raised safe completion from 158 to 206 on 384 clean dispatch jobs; it fell from 134 to 110 on 384 museum jobs. Under degraded metadata, verification reduced exposure from 125/384 to zero and raised safe completion from 143 to 194. Those controls relied on reliable delivered-history state and truthful successful verification. For this release we verified every entry of the retained v0.1 and v0.2 manifests and replayed all 15,872 primary v0.2 scores and traces before building the extension.

### New collaboration benchmark
Three reviewers can sign early. The current job specifies one or two signatures and identifies a pool eligible for later certification. The actual later assignment is unavailable at opening. The job then needs all assigned certificates and sometimes a staff memo. Early evidence describes one binary site attribute; the certificate describes the other. Either attribute alone leaves two possible sites. Together they identify one of four fictional locations. The subject, sites, assignments and messages are synthetic.

Distinct signatures can pass through distinct mailboxes, two roles can share one mailbox, or a later handoff can move delivery to another mailbox. A historical message may already narrow the recipient's knowledge. Staff can receive a restricted memo before withdrawal; a public observer cannot receive its restricted derivative. Preview-purpose transfers cannot disclose a site attribute. Permission history is scored at delivery. A recipient does not forget information when a grant changes.

### Data and timing
Three development seeds, two validation seeds and twelve untouched evaluation seeds supplied 72, 48 and 288 jobs respectively. Each block contained 24 jobs. Eight controllers and seven metadata conditions replayed identical exogenous cases. All 22,848 runs completed. The 56 conditions per job are paired interventions, not 56 independent observations. Within a job, prior knowledge arrives at tick 0, votes at tick 1, certification at tick 5, the staff memo at tick 6 and the copy at tick 7. The planner interface contains no future assignment, true site, outcome, job identifier or next grant time.

<!-- page -->

## 2. Policies, metrics and uncertainty
Greedy attempts every admissible early vote. Minimum attempts votes in fixed role order and stops once the quorum is met. The cue adapter uses the frozen v0.2 decision function and development counts to rank roles according to an assumed mapping between the old cue and the later signer. That translation is a modeling choice; it is not a reproduction of v0.2 on its original task.

The eligibility planner first tries early reviewers whose current mailboxes are outside the known later-eligible pool. It then tries noneligible roles sharing an at-risk mailbox, followed by eligible roles. Like minimum, it stops when enough distinct reviewers have signed. Checked applies the same planner plus current verification, denying the transfer when verification is unavailable. Other ablations ignore the recipient's previous information or substitute a dictionary interpretation for the candidate message's typed meaning. Open admits every proposal.

### Fault intervention
Clean metadata matches the true state. Four single-fault conditions delay grant notices, omit history at certification and copying, invert some document lineage labels, or make some verification requests unavailable. Mixed combines these conditions. In the final stress condition some positive verification responses wrongly clear a document's restricted ancestry or omit history. A successful verification response is distinct from an unavailable one. Trusted verification sees complete current information only in the honest-verifier regime.

### Measures
Exact success requires an early quorum, all late certificates and any commissioned staff memo. Safe success also requires zero exposure throughout the job. Exposure includes identifying a previously non-singleton public observer's site, sending a restricted document out of scope or after withdrawal, and sending protected content for preview. A permissible denial is an offer the controller declined even though sending it at that instant would have been allowed. Such counts include redundant offers declined after a quorum. They are not all lost tasks. Runtime covers simulation and view/trace construction, excluding scoring and disk I/O. No actual network verification latency was measured.

### Prospective analysis
The local protocol was committed before implementing and running the new controllers. H1 and H2 compare clean safe completion against greedy and minimum. H3 compares mixed exposure under checked and unchecked eligibility. H4 contrasts bad and honest successful attestations. We resampled twelve seed blocks 10,000 times and used two-sided 98.75% percentile intervals to adjust four paired contrasts. Each criterion required strict exclusion of zero in the specified direction. The feasibility ceiling and explanatory cases were examined post hoc.

<!-- page -->

## 3. Planning and robustness results
All counts in this table are out of 288 held-out jobs.

| Policy | Clean safe | Mixed exact | Mixed safe | Mixed exposed |
|---|---:|---:|---:|---:|
| Open | 0 | 288 | 0 | 288 |
| Greedy typed enforcement | 13 | 274 | 11 | 270 |
| Fixed-order minimum quorum | 85 | 274 | 50 | 230 |
| Frozen cue adapter | 84 | 274 | 52 | 228 |
| Current eligibility | 106 | 274 | 65 | 212 |
| Eligibility with verification | 106 | 64 | 64 | 0 |
| Ignore history | 85 | 282 | 63 | 220 |
| Dictionary gate | 98 | 275 | 64 | 214 |

H1 and H2 met their criteria. Eligibility improved safe completion over greedy by 32.29 percentage points (adjusted interval +25.00 to +37.85), and over minimum by 7.29 points (+3.47 to +12.50). In the complete-information feasibility analysis, 162 jobs admitted at least one safe successful schedule. Of the 182 jobs the eligibility planner did not complete safely under clean metadata, 126 were infeasible under these permissions and 56 had a feasible alternative.

### Transfer and counterexamples
Against fixed order, eligibility completed 46 versus 30 in distinct-mailbox jobs and 38 versus 22 with pooled mailboxes. Under later handoff the comparison reversed: 22 versus 33. Each topology had 96 jobs. In test-347-5, choosing reviewer 2 early preserved mailbox p1 for two later signatures, enabling both certificates. In test-347-14, the planner gave p1 an early fragment; the later certificate was redirected there and would identify the site. Fixed order preserved that mailbox and succeeded. No access to the hidden handoff was supplied to the planner.

### Faults and utility
H3 met its criterion. Current verification reduced mixed exposure by 73.61 percentage points (−79.86 to −67.71). Unchecked eligibility produced 77 post-withdrawal violation cases among 149 withdrawn jobs. Checked produced zero, but exact completion fell from 274 to 64 and safe completion fell by one. It declined 488 currently permissible proposals, including quorum-related and verification denials. H4 also met its criterion: successful but incorrect attestations raised exposure by 17.71 points (+14.58 to +20.49). In test-347-6 the memo was sent after its true grant expired. This directly tests the assumption underlying the zero in the previous row.

<!-- page -->

## 4. Natural-language disclosure
The text study separates an author's intended meaning from a detector's interpretation. A statement denotes a set of possible sites. A recipient identifies the protected site if the statement narrows its previous possibilities to one. Tests include exact names, indirect directional and geographic phrases, paraphrases in summary documents, negation, references to another case, and statements whose referent or uncertainty cannot be resolved. A true conflict between a detector's predicted meaning and prior knowledge triggers abstention.

There were 51 distinct determinate held-out utterances. Recombining them with compatible recipient histories yielded 195 determinate contexts: 108 identifying and 87 nonidentifying. There were 15 further ambiguous contexts from three statements. Contexts sharing an utterance are dependent. These are diagnostic counts, not independent natural-language samples. The statistical classifier used character n-grams and logistic regression trained on 34 distinct determinate development utterances. Determinate test strings were absent from its training data. Wording patterns and topic are internally authored throughout. The hand-built dictionary has task-specific vocabulary, including some test constructions, so its score is a coverage measure rather than blind learned-model generalization.

| Detector | True positive | True negative | False positive | False negative | Abstained on determinate |
|---|---:|---:|---:|---:|---:|
| Literal site matching | 36 | 77 | 6 | 72 | 4 |
| Compositional dictionary | 78 | 87 | 0 | 30 | 0 |
| Character n-gram classifier | 74 | 45 | 18 | 20 | 38 |

The character model abstained on 14 positives and 24 negatives, so its 20 false negatives exclude 14 more missed positive decisions. On the 15 ambiguous contexts, literal matching returned a definite answer 15 times, the dictionary zero times and the classifier 12 times. Those answers have no reliable automatic truth label. No inter-rater agreement or human estimate was computed. A separate packet provides 36 blinded cards for future review.

### Mechanism
If the recipient already knows the site is coastal, a document placing it outside the southern district identifies Alder. The exact site name need never be sent. Conversely, a training memo can mention Alder without asserting that the current case belongs there. Name matching fails in opposite directions on those examples. In workflow execution the dictionary gate exposed information on 76 clean jobs versus zero with the typed eligibility gate. That gate estimates the current candidate's meaning but still uses typed historical knowledge; the comparison does not model cumulative extraction error.

### Real LLM pilot status
The optional harness accepts an explicitly supplied local chat GGUF and records its SHA-256, binding version, prompts, outputs, decoding settings and latency. It evaluates identical model replies through paired gates and leaves unsupported language judgments unresolved for human review. The environment had no project-local chat GGUF or local generative backend, and network access did not include a model-weight host. Zero generative trials were executed. The trained character classifier is a separate text experiment.

<!-- page -->

## 5. Verification, limits and synthesis
A standard-library scorer independently rebuilt recipient knowledge as explicit sets, resolved addresses from each case, and checked delivered signatures and authoritative withdrawal times. It matched all 22,848 scores, 162,848 event records and every violating event index. A separate interpreter containing only the policy modules and development counts reproduced every opening order and delivery action/reason from its whitelisted observations. This verifies sufficiency of the recorded views for these policies; it is not an adversarial software-isolation proof.

A fresh environment reproduced the scientific tables and uncompressed traces byte for byte. The virtual environment reused preinstalled numerical libraries. Runtime was excluded from equality checks. Reference median time per simulated job was 38.4 microseconds for eligibility, 39.7 for checked and 46.8 for the dictionary gate. Thirteen final-release tests passed on Linux. Windows-oriented path and file-lifetime regressions were included, but Windows execution remains unverified.

### Limits on generalization
All evaluation families were authored by this project. The final task changes the combinatorial objective and recipient mapping, but retains typed payloads, fixed clocks, synthetic priors and a narrow interpretation of a protected fact. Test roles and thresholds are few. Cue reliability, eligible-set size and quorum size co-vary by construction, so their separate causal effects cannot be estimated from the signal strata. Metadata faults are deliberate stresses rather than prevalence estimates. Alias visibility and honest verification are strong assumptions. Indirect speech, social inference, collusion and real workflow outcomes remain untested. A stamped document carrying restricted lineage counts as a policy violation even when its text does not itself identify the site.

### What carried across releases
Remembering prior disclosures helps a broker detect cumulative exposure, but it cannot repair an early choice once a later obligation arrives. Online allocation improved safe completion under some distributions. In v0.2 the learned cue failed on transfer; in v0.3 current eligibility improved aggregate utility but failed under some handoffs. Current-evidence verification reduced exposure in both releases. Its benefit to safe completion did not carry over, and its protection broke when positive evidence was wrong. These negative findings define the boundary of the result more precisely than a single aggregate score.

### Relation to prior work
TG-CI/MAPLE-Bench already studies history and downstream scope. CI-RELAY mediates internal messages. Agent Mosaic and The Sum Leaks More Than Its Parts address inferable composites. PiSAs examines visibility and utility in multi-user systems. PRIVTRACE contributes an auditable joint test of future demand, recipient identity, language interpretation and verification faults. Source records and licenses are listed in the prior-work audit. No prior system's published score was reproduced, and no priority or publication claim is made.

### Remaining scientific work
The final software and synthetic study are complete within this scope. An externally authored task set, independent human labels, real generative trials with model-output review and an external rerun would test claims the present evidence cannot settle. The reviewer-safe materials exclude the historical coordinator keys and evaluation answer files.
