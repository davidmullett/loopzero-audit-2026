# Pre-specified audit plan v3 — KKBox, then τ-bench

**Author:** David Mullett
**v1:** 24 August 2026 · **v2** (after first adversarial review): 24 August 2026 · **v3** (after second adversarial review): 24 August 2026
**Status: FROZEN.** Revised across two rounds of adversarial review — see §11 for exactly what that review was, and was not. No data or evaluation code has been examined. §§3–6 are now immutable; any change is a logged deviation.

**v3 changes (second adversarial-review round):** the §4/§5a contradiction resolved — Q7 is answered at trial level, **adjudicated at task level** · a **MISSCORING** branch added, since a crashed trial scored as a pass had no home in the rule and would otherwise have tempted a stretch of the persistence criterion · adjudication made **externally checkable** rather than delegated to a non-independent party · **K6** added (the window-edge case, KKBox's likeliest positive) · the 5% denominator **named per instrument**.

**Changes from v1, all prompted by adversarial review:** the vacuous monotonicity criterion is removed · the unit of analysis is corrected and doubled · four enumeration gaps closed and one new primary question added · a prevalence threshold is fixed in advance · the delegation limits are named honestly instead of standing as safeguards · **KKBox runs first** · the plan is hashed and the hash posted before the read.

---

## 0. What this document is, and what it is not

A **pre-specified audit plan for existing public artifacts**. Not a pre-registered experiment: I do not control either instrument, and both already exist publicly. What I commit to in advance is the question, the decision rule, and publication either way — not the unavailability of the data.

**Verification of that commitment:** on freezing, this document is hashed (SHA-256) and the hash posted publicly, before any read begins. That converts "trust me, I wrote it first" into something checkable. Same move as the deviations-log anchor in the paper.

---

## 1. Order of work — KKBox first

**This is the most important change from v1, and the reason is upstream of any rule I could write.**

I chose τ-bench partly because it is the domain I am selling into. I said so in v1 and treated downstream safeguards as sufficient. They are not: **no downstream rule fixes an upstream selection.**

So: **KKBox runs first.** I have no commercial stake in churn datasets. Its rule is quotable verbatim. Publishing that result first — whatever it returns — establishes the protocol on neutral ground and makes any subsequent τ-bench result substantially harder to read as motivated.

τ-bench runs second, under this same frozen plan.

---

## 2. Prior knowledge and declared expectation

**KKBox:** I know the published churn definition — *"no new valid service subscription within 30 days after the current membership expires,"* holding *"even if the user decides to cancel."* I have not examined the data, the competition's label-generation code, or any solution notebooks.

**τ-bench:** I know it evaluates tool-and-user interaction in customer-service domains, that success is checked by comparing final database state to a goal state, and that it reports pass^k across repeated trials. **I have not read the evaluation code**, the scoring path, the error handling, or the issue tracker.

**Declared expectation — and it is now better calibrated than in v1.** In the past two weeks I ran gate checks on coding-benchmark construction, crash-free release gates, and infrastructure deterioration models. **All three failed.** Against that base rate I expect **both of these to come back negative**, and I expect KKBox in particular may turn out to be **window censoring rather than absorption** — a different mechanism that would correctly read as negative.

**The negative write-up, drafted now so it doesn't feel like a loss later:** *the structure appears rarer than I initially believed; here is where it is not, and here is what distinguishes those cases from the one where it is.* That is a real contribution and almost nobody publishes it.

---

## 3. The structure being tested

From *Absorbing Shadow Classes in Conjunctive Label Rules* (arXiv, Aug 2026). Requires **all three**:

1. **Conjunctive rule** — recorded as a failure only if a failure condition holds **AND** an eligibility condition holds.
2. **Absorbing ineligibility** — once the unit crosses the eligibility bound it can never again be recorded as a failure.
3. **Residual success class** — the ineligible unit **remains in the denominator of a named reported metric and is counted as a success.**

**What gives the mechanism its bite, and what v1 got wrong.** The unit must *persist and keep accruing real bad outcomes while being structurally unrecordable.* In the paper, starved users kept being served badly for thirty more steps, generating genuine harm the rule could never see.

**Termination is not absorption.** A trial that crashes and stops has not entered an absorbing state in any meaningful sense — every terminal state is trivially monotone. v1's "monotone within the trial" criterion was therefore **vacuous** and is removed. A criterion satisfied by definition tests nothing.

**The gate question, unchanged:** *does the unit leave the denominator, or stay in it and get counted as a success?*

---

## 4. Units of analysis — two levels, pre-assigned

v1 used a single unit and that choice predetermined a negative. Both levels are now specified, with their roles fixed in advance:

**Trial level** *(τ-bench)* — one attempt at a task. **The paper's pathology cannot appear here**, because a terminated trial cannot persist and keep accruing unrecordable failures. But trial level **can** carry a distinct and serious defect: a trial scored as a *pass* because it died before it could fail. That is **MISSCORING** (§6), not the paper's mechanism, and it is reported as its own finding rather than folded into either.

> **Q7 is answered at trial level but adjudicated at task level.** Whether a crashed-trial-scored-as-pass is *material* depends on whether those passes propagate into pass^k and thereby into the task's reported reliability. The observation is made below; the significance is decided above.

**Task level across k repetitions** *(τ-bench)* — **this is the level that can carry the pathology.** If unevaluable trials are dropped and pass^k is computed over the survivors, the task remains in the suite denominator with a score derived only from its evaluable attempts. A task that fails to execute most of the time can report as reliable. Unit persists, accrues unrecordable failures, counted as success.

**User level within the observation window** *(KKBox)* — the level that can carry it there.

---

## 5. Questions — fixed before reading

### 5a · τ-bench

**Q7 · Goal-state-by-inaction — PRIMARY.** *(Answered at trial level, adjudicated at task level per §4.)* Scoring compares final database state to goal state. **For which tasks is the goal state satisfiable by taking no action at all?** On those tasks, what does a crashed, timed-out, or no-op trial score? If the initial state equals the goal state, a trial that dies before acting may be recorded as a **pass** while remaining in the denominator.

> *This is **silence read as success** — but note precisely what it is and isn't. It satisfies (a) remains in denominator and (b) counted as success, and **fails (c) persistence**, because the trial is over. So it is **not** the paper's pathology. It routes to **MISSCORING** (§6) — arguably a worse defect than exclusion, since exclusion is at least honest about what it doesn't know. **Do not stretch (c) to capture it.***

**Q1** Runtime error: scored as failure, excluded, retried-and-replaced, or passed by default?
**Q2** Timeout / step-budget exhaustion: which of the above?
**Q3** Unclassifiable terminal state (comparable to neither goal nor known failure): which?
**Q4** Retry semantics: is any trial retried? Is the retry scored in place of, alongside, or instead of the original?
**Q5** pass^k composition: how do errored, timed-out, or unclassifiable trials enter the pass^k computation — as failures, exclusions, or passes? **Answered at task level.**
**Q6** Denominator: attempted, successfully executed, or suite size? If they differ, where does the difference go, and **which named reported metric** does each feed?
**Q8** User-simulator failure: the simulated user is itself an LLM. If it errors or departs from script, is that distinct from agent error, and how is it handled?
**Q9** Cost / token-budget exhaustion, as a path distinct from time or step limits.
**Q10** Partial goal satisfaction: is the state comparison all-or-nothing? If not, where does a partial land?
**Q11** Agent refusal as a terminal state that is not an error.

### 5b · KKBox

**K1 · The gate question.** Can a user enter a state in which they can **never be labelled churned within the observation window**, while **remaining in the denominator** of the reported churn rate?
**K2** The cancellation clause: a user who has actively cancelled but whose membership has not yet expired — are they counted as retained, and for how long?
**K3** Is that state **absorbing** (they can never subsequently be labelled churned) or merely **delayed** (they would be labelled in a later window)?
**K4** How are users whose membership expires outside the labelling window treated — excluded, or retained in the denominator as non-churned?
**K5** Which reported metric carries the denominator, and what decision would it drive in a live subscription business?

**K6 · The window-edge case — KKBox's most likely positive.** The churn rule requires **30 days of non-renewal after expiry**. So a user whose membership expires **fewer than 30 days before the observation window closes cannot satisfy the churn condition — there aren't 30 days left in which to fail it** — yet plausibly remains in the denominator, counted as retained. Stay-in-denominator, counted-as-success, and real churn the rule cannot record.
> *Note in advance: this may resolve to **censoring** rather than absorption — the user would be labelled correctly in a later window. That is a finding either way, and routes to the NEGATIVE–censoring branch. **Do not force it into POSITIVE.***

**Exhaustiveness:** these lists are declared exhaustive for their instruments. Anything else found is an **observation, not a finding**, and must be labelled so.

---

## 6. Decision rule — fixed before reading

Applied per instrument, at the unit specified in §4.

**POSITIVE requires all three:** (a) a unit that cannot be evaluated **remains in the denominator of a named reported metric**; (b) it is **counted as a success** there; (c) it **can continue to accrue real failure events that the rule cannot record** — persistence, not merely termination.

**Prevalence split, fixed now.** Bare presence is technically true and rhetorically misleading; my own finding was 69.2% and a reader will hear "present" as "material."
- **POSITIVE-MATERIAL** — affected units are **≥5%**, measured against a **named denominator, fixed now per instrument**:
  - **τ-bench: 5% of tasks in the suite.**
  - **KKBox: 5% of labelled users in the observation window.**
  *(Q6 establishes there may be several candidate denominators; these are the ones that govern. Rationale for 5%: benchmark leaderboards routinely separate systems by 2–3 points, so a distortion at this scale can invert a ranking and therefore a decision.)*
- **POSITIVE-PRESENT-BUT-RARE** — below 5%.
- **Prevalence is reported either way**, against the named denominator above, with any other affected denominators reported separately rather than substituted.

**pass^k gets its own branch** (τ-bench). pass^k is a different object from a per-trial score. State separately whether unevaluable trials enter it as failures, exclusions, or passes, and report that finding on its own rather than folded into Q1–Q3.

**MISSCORING — silence read as success, without persistence.** The unevaluable unit **remains in the denominator and is counted as a success**, but **cannot continue accruing failures** — condition (c) fails. Not the paper's pathology; same family. **Arguably a worse defect than exclusion, since exclusion at least does not assert a result it hasn't earned.** Publishable in its own right, reported as its own finding, never as evidence for the paper's mechanism. *(This is the expected landing zone for Q7.)*

**NEGATIVE — exclusion:** the unevaluable unit is removed from the denominator. Different mechanism. Publish as such.
**NEGATIVE — correctly handled:** scored as a failure. The conservative, correct treatment. Publish as such.
**NEGATIVE — censoring, not absorption** *(the expected KKBox branch)*: the unit would be labelled in a later window. Related hazard, different mechanism. Publish as such.
**INDETERMINATE:** configuration-dependent, undocumented, or version-variable beyond resolution. Publish as indeterminate; **do not report the most interesting branch as the finding.**

**Binding constraints:** the pinned commit / dataset version governs; variation across versions is reported, never selected from. The rule is applied as written, not adjusted to what is found.

---

## 7. Method, and the honest limits of its safeguards

1. Pin the commit hash (τ-bench) and dataset version (KKBox). Record here **before** reading.
2. Hash this frozen document; post the hash publicly.
3. Answer the questions with **file-and-line citations** (τ-bench) or explicit rule/field references (KKBox). Where ambiguous, say so; do not infer intent.
4. Apply §6 as written.
5. **Log actual hours spent.** Without that log, the claim that the check is cheap to run is unsupported and will be dropped.

**The delegation limits, stated plainly rather than presented as protections:**

- **Claude Code is not an independent checker.** It is an instrument I direct, answering questions I wrote, and it will find what the brief points at. It reduces my execution error; it does not reduce my framing bias.
- **The reviewing model instance is not an independent adjudicator.** It is an AI system I prompted, in a conversation carrying this project's commercial context. It has no institutional standing, no stake in being right, and no accountability for being wrong. Its review materially improved this plan; it is not an arm's-length audit and must not be described as one. See §11.
- **The one genuinely independent check is maintainer contact** — and it is strengthened accordingly: the maintainers' response is published **in full and unedited, adjacent to the finding**, not summarised, not excerpted.

**Who adjudicates §6 — and how that's made honest.** v1 delegated the branch call to the reviewing model. v2 correctly established that it isn't independent — but removing them left the call defaulting back to me, which is the arrangement the delegation existed to prevent. **The fix is not another name. It is external checkability:**

> **I apply §6 myself, and I make the application inspectable.** Published together, in one place: the frozen plan and its hash · the pinned version/commit · every answer with its file-and-line or field citation · the branch I assigned and why.
>
> **Any reader can apply the rule to the evidence and see whether they reach my branch. I am explicitly inviting disagreement, and any substantive disagreement gets published alongside the finding.**

That is weaker than a genuinely arm's-length adjudicator and stronger than a delegation I can't actually make arm's-length. Stating it plainly is the point.

---

## 8. Publication commitment

Published either way — including indeterminate — within two weeks of completing each read. Maintainers (τ-bench) and the dataset's publishers (KKBox) receive the finding before public write-up, with a reasonable correction window; their reply is published verbatim alongside.

**No commercial use of an unpublished finding.** Nothing here appears in a pitch, one-pager, or conversation before publication and the correction window has closed.

---

## 9. What this can and cannot support

**Can:** instances of the protocol applied to instruments I did not build; evidence about where the structure does and does not appear; a mapped boundary for the method.

**Cannot:** resolve the generalization objection from n=1 — I am still the one running it, and neither delegate is independent. **Independent replication requires other hands.** This does not substitute for it and will not be described as if it does.

---

## 10. Freeze

This document is **immutable from the moment its hash is published.** It contains no fields to be filled in later — by design. A frozen artifact that is written into afterwards cannot verify against its own hash, which would defeat the purpose of hashing it.

**Execution state — what was pinned, when the read began, hours spent, results, maintainer responses, publication — is recorded in `EXECUTION-LOG.md`**, a separate mutable file. Deviations are recorded in `DEVIATIONS.md`.

**Nothing in §§3–6 may change, ever.** Any change means this plan was not frozen, and must be logged as a deviation with its reason, when noticed and before investigation.

Adversarial review of v3 completed 2026-08-24, after two rounds. No data or evaluation code examined prior to freezing.

---

## 11. AI disclosure — what the "review" actually was

**This matters more than the review itself, so it is stated plainly rather than buried.**

The two review rounds that shaped this document were conducted by **a separate instance of an AI language model**, prompted by me to act as an adversarial reviewer, in a conversation that did not include the drafting of the plan. It is **not** a human expert, not an institutional reviewer, and holds no credential of any kind.

**Why it is nonetheless recorded:** the review was substantive and it changed the plan materially. It identified that a criterion I had written was vacuous — satisfied by definition, therefore testing nothing — and that my chosen unit of analysis made a negative result structurally inevitable. Both were blocking defects. It also identified the strongest available question (goal-state-reachable-by-inaction) which I had not enumerated, and it corrected the order of work on conflict-of-interest grounds I had reasoned past. Suppressing that provenance would misrepresent how this document came to exist.

**Why it must not be mistaken for external validation:** an AI reviewer has no stake in being right, no accountability for being wrong, no independent knowledge of the instruments, and no standing to certify anything. It is a thinking aid with adversarial framing. **It is not peer review and confers no warrant.**

**The whole plan was drafted with AI assistance**, consistent with the disclosure covenant on the associated paper.

**What this means for the reader:** the only external checks on this work are (a) the published hash, which fixes the rule in time, (b) the instrument maintainers, who can contradict the finding and whose response is published unedited, and (c) you, applying the stated rule to the published evidence. **Nothing in the review process substitutes for those.**
