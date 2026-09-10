# τ-bench — branch assignments under §6

**Instrument:** τ-bench / τ²-bench evaluation harness
**Pins (R2′, `EXECUTION-LOG.md`):**
**A** `sierra-research/tau-bench` `main` `59a200c6d575d595120f1cb70fea53cef0632f6b`
**B** `sierra-research/tau2-bench` `v1.0.1` `fc0055dc4e0a316c3f83133267fbd6faaa770992`
**C** `sierra-research/tau2-bench` `v1.0.0` `17e07b1da2bbc0cadfddeea36412686e0604127b` *(diff-scoped)*
**Frozen plan:** `b15f472e…` · frozen `2026-08-24T15:33:01Z` · `osf.io/ksm3n` · DOI `10.17605/OSF.IO/KSM3N`
**Answers:** `TAU-ANSWERS.md` · **Deviations:** D-6, D-7, D-8, D-9
**Assigned by:** David Mullett · 2026-08-27

---

## SUMMARY OF ASSIGNMENTS

|  | Instrument (Q1–Q11) | pass^k |
|---|---|---|
| **A** `tau-bench` | **MISSCORING** | **NEGATIVE — correctly handled** |
| **B** `tau2-bench` | **MISSCORING** | **NEGATIVE — exclusion** |

**Four assignments, not one.** The two repositories behave oppositely on error handling: A retains errored trials as failures; B excludes them after retry.

**The paper's mechanism was not found in either repository.** Two structural defects were found that §6's branch scheme does not cover; they are reported below **as findings in their own right**, not folded into any branch.

---

## Disclosure

The read that produced `TAU-ANSWERS.md` was executed by an AI coding agent against a pre-registered brief, under boundaries fixed before the read. **The evidence summary and the rule-application analysis were prepared with AI assistance, and the assignments below were drafted by it.** The author verified each condition against §§3–6, ruled on the two questions the frozen text does not settle, and accepted the reasoning.

**Not expert review, not peer review, confers no warrant.** Standard set by §11 of the frozen plan and guard G-3.

> **Two matters bearing on how much weight to give the AI-assisted analysis, disclosed rather than omitted.**
>
> **1.** During the KKBox assignment the same assistance specified a confirmatory test that was **structurally incapable of failing** and presented it as a two-branch pre-commitment. The executing agent caught the degeneracy and refused to bank it (`KKBOX-VERDICT.md`, D-5).
>
> **2.** During *this* assignment the same assistance first drafted **B · pass^k as POSITIVE**, then reversed itself on re-reading §3. **The reversal moved away from the more interesting finding and is logged as D-9.** A reader should weigh both directions.

---

## STRUCTURAL RULING — four assignments

§6 applies *"per instrument"*; it separately requires that *"pass^k gets its own branch."*

**A and B are different codebases**, not two versions of one — distinct repositories, distinct histories, no shared lineage in the audited paths. They **behave oppositely on Q1**: A scores runtime errors as failures and retains them; B retries, relabels and excludes them. **Collapsing them would hide the only structural divergence the audit found.**

`v1.0.0` (**C**) is a version of B, diff-scoped under R2′. `agent_metrics.py` is **byte-identical** between B and C, so **B's pass^k assignment governs C unchanged.**

---

## A · INSTRUMENT — MISSCORING

**(a) Remains in the denominator? YES.** The task is scored and appears in both reported metrics. `calculate_reward` (`envs/base.py:124-140`) starts `reward = 1.0` and only reduces it. **[E]** mechanism.

**(b) Counted as a success? YES.** With no mutating reference action and no required outputs, `gt_data_hash` equals the untouched-database hash, `r_actions` is `True`, reward remains **1.0**. **[E]** mechanism · **[I]** count.

**(c) Can it keep accruing failures the rule cannot record? NO.** The trial has terminated. §4 forecloses this in advance: *"the paper's pathology cannot appear here."* Q7's own note: *"fails (c) persistence, because the trial is over."*

**Result: (a) and (b) hold, (c) fails — MISSCORING**, exactly as §5a and §6 predicted before the read.

**Prevalence, reported alongside** — §6 gives MISSCORING no material/rare split:

- 24 of 165 test tasks — **14.55% [I]** pooled
- airline **19 of 50 — 38.00% [I]**
- retail 5 of 115 — 4.35% **[I]**

**Every figure is [I]**, resting on an AST analysis that was **wrong twice before it was right** (judgement call 1).

**Sharpest supporting fact:** on **19 of the 24**, an immediate `transfer_to_human_agents` scores **1.0**, and the reference solution involves no transfer at all. **An agent that gives up instantly is recorded as having succeeded perfectly.**

**Narrowing that must travel with the finding.** A *crashed* trial never reaches the reward path — `run.py:89-96` assigns `reward=0.0`; step-budget exhaustion returns 0 because `done` was never true. **[E]** What passes by inaction is a trial terminating **normally** without acting. That is materially smaller than Q7's premise and it is the honest statement of it.

---

## A · pass^k — NEGATIVE, correctly handled

An errored trial carries `reward=0.0`, so `is_successful` is `False`; it decrements no counter and **remains in `num_trials`** (`run.py:181-199`). **[E]**

**The unevaluable trial is scored as a failure and retained.** §6: *"NEGATIVE — correctly handled: scored as a failure. The conservative, correct treatment."*

**Worth stating plainly: the older, dormant repository does the more conservative thing.**

---

## B · INSTRUMENT — MISSCORING

**The abnormal-termination route is closed.** `evaluator.py:119-129` returns `reward=0.0` for any termination outside `{AGENT_STOP, USER_STOP}`, documented as *"Premature termination = 0 reward"* (`AGENTS.md:56`). **Code and documentation agree. [E]**

**What survives is A's shape, an order of magnitude smaller:**

> **🔴 CORRECTED 10 September 2026.** This table omitted the `mock` row while carrying a pooled figure that included it, so it summed to **2,546 tasks and 10 findings against a stated 11 of 2,556**. The row is restored from `TAU-ANSWERS.md:183`. **Found while writing the manuscript that reports this audit, not by a reader.** The branch assignment is unaffected: **NEGATIVE on either reading.**

| Domain | Inaction-satisfiable | Share |
|---|---|---|
| retail | 6 / 114 | **5.26% [I]** |
| banking_knowledge | 4 / 97 | 4.12% **[I]** *(4 of 9 in its `ACTION`-basis subset)* |
| airline | 0 / 50 | **0.00% [I]** |
| telecom | 0 / 2,285 | **0.00% [I]** |
| mock *(fixture)* | 1 / 10 | **10.00% [I]** |
| **pooled** | **11 / 2,556** | **0.43% [I]** |

**(a) and (b) hold; (c) fails identically** — the trial is over. **MISSCORING**, at 0.43% pooled, ~~retail the only domain clearing 5%~~ — **corrected 10 Sept 2026: two domains clear 5%, mock at 10.00% and retail at 5.26%** — retail clearing it **by 0.26 points on six tasks, on [I] evidence**, and mock being the ten-task fixture whose standing in a suite-level threshold this audit does not resolve. **NEGATIVE on either reading.**

**The only threshold-relevant figures in the entire audit graded [E]** are B's default-pass routes — 0.00% and 0.04%. **Both below threshold. Nothing that clears the threshold anywhere in this audit is read rather than inferred.**

---

## B · pass^k — NEGATIVE, exclusion

**This cell was drafted POSITIVE and reversed. The reasoning for the reversal is the substance of the assignment. See D-9.**

### (a) Does a unit that cannot be evaluated remain in the denominator? NO.

**§6(a) asks about the unit that cannot be evaluated. In this instrument the answer splits, and neither branch satisfies the condition:**

- **The trial** cannot be evaluated — and it is **removed**. `agent_metrics.py:138-145` filters `INFRASTRUCTURE_ERROR` rows out of the frame. **[E]**
- **The task** *can* be evaluated — on its surviving trials — and it is retained. **A unit that is evaluated is not a unit that cannot be evaluated.**

**There is no unit here that is both unevaluable and retained.** §6's exclusion definition is met exactly: *"the unevaluable unit is removed from the denominator."*

### (b) Not reached.

### (c) Not established, and not establishable from a code read.

**§3 is stronger than §6's shorthand and it governs:** *"The unit **must persist and keep accruing** real bad outcomes while being structurally unrecordable."* The paper's own instance is demonstrated accrual — *"starved users **kept being served badly** for thirty more steps."*

**What this audit established is that a code path exists.** D-8 showed at **[E]** that agent behaviour can reach the exclusion — `llm_utils.py:440` parses `json.loads(tool_call.function.arguments)` outside any `try`, so a model emitting invalid JSON is retried, relabelled `INFRASTRUCTURE_ERROR`, and dropped. **Whether any task actually persists and keeps accruing such failures is a property of a run, and boundary 8 forbids producing it.**

> **⚠️ Why (c) is not stretched to cover it.** §6's phrasing is *"can continue to accrue"*; §3's is *"must persist and keep accruing."* Reading the modal alone would license a positive on the existence of a code path. **The frozen plan already forbade exactly this move for Q7** — *"do not stretch (c) to capture it"* — and a prohibition stated for one question is not weakened by the plan's failure to anticipate a second. **Applying it here costs the only positive-shaped finding in five checks. That is the point of having written it down first.**

### Result

**(a) fails. NEGATIVE — exclusion.**

**Not the other branches:** not POSITIVE (a fails, c unestablished); not MISSCORING (requires (a) and (b) to hold); not correctly-handled (the trial is not scored as a failure, it is removed); not censoring (nothing is labelled in a later window); **not INDETERMINATE** — the mechanism is documented, quotable, and byte-identical across two releases. What is undeterminable is a *frequency*, and §6 reserves INDETERMINATE for findings that are *"configuration-dependent, undocumented, or version-variable beyond resolution."* **This one is none of the three.**

### Mitigations, recorded because they bear on how the exclusion should be read

1. **`max_k` is capped at the minimum surviving trial count**, with a warning (`agent_metrics.py:158-165`) — exclusions on one task lower `k` for the whole suite rather than inflating that task at full `k`. **[E]**
2. **`infra_error_count` is computed and carried** on `AgentMetrics` (`:217-221`), and the exclusion is logged (`:142-144`). **The instrument discloses its own exclusion.** **[E]**

---

# FINDINGS OUTSIDE §6

**Two defects were established at [E] that the branch scheme has no slot for.** They are reported here rather than forced into a branch, and **neither requires the paper's mechanism to be worth reporting.**

## F-1 · `pass^k` has two documented conventions and the instrument does not reconcile them

**Revised 27 Aug after D-10, which found that the release documentation was never swept during the read.** The original F-1 described the code path alone. **The instrument states two different conventions for the same metric name, and the audit found both.** All three sources below are at the same pinned commit, `fc0055dc`.

**1 · The code excludes. [E]** `agent_metrics.py:138-145`:

```python
infra_count = (df.termination_reason == TerminationReason.INFRASTRUCTURE_ERROR).sum()
if infra_count > 0:
    logger.warning(f"Excluding {infra_count} infrastructure error simulation(s) from metrics.")
    df = df[df.termination_reason != TerminationReason.INFRASTRUCTURE_ERROR]
```

**2 · The CHANGELOG says the same thing. [E]** `CHANGELOG.md:103`, describing pre-1.0.1 behaviour:

> *"…before being binned as `INFRASTRUCTURE_ERROR` **(which is excluded from `pass^k` and `avg_reward` metrics)**"*

**Agrees with the code.**

**3 · The release notes say the opposite. [E]** `RELEASE_NOTES.md:83`:

> *"pass^k values are recomputed counting infrastructure-error simulations as **failed trials** (the leaderboard convention)"*

**Disagrees with both.**

**The two in-tree documents conflict, and nothing in either states which convention governs a published figure.** A reconciliation is available — that the leaderboard convention is a recomputation separate from the library metric — **but neither document says so, and this audit does not supply it.** Boundary 4 governs: where documentation and code disagree, report both and say they disagree. **The conflict is the finding.**

**A disclosed instantiation, in the same paragraph. [E]** `RELEASE_NOTES.md:83`:

> *"glm-5-think's trajectory file contains only 3 trials for some tasks, so pass^4 is not recomputable; its previous value is retained."*

**Unequal per-task trial counts, in the published leaderboard, disclosed by the maintainers** — and a published `pass^4` carried forward from a prior grading run because the current one could not produce it.

### What follows under the exclusion convention

**This is the code's default and the CHANGELOG's statement**, so the arithmetic below is what the library computes.

`agent_metrics.py:177-180`:

```python
res = df.groupby("task_id")["success"].apply(
    lambda df: pass_hat_k(len(df), df.sum(), k)
)
```

`len(df)` is **that task's surviving trial count**, passed as `num_trials` into `math.comb(success_count, k) / math.comb(num_trials, k)` (`:126`). The suite figure is an **unweighted mean across tasks** (`:241-244`).

Because `C(nᵢ,k)` grows with `nᵢ`, **the same absolute success count contributes more from a task with fewer survivors:**

| Surviving trials *n* | Successes *c* | Contribution to `pass^2` |
|---|---|---|
| 2 | 2 | **1.0000** |
| 3 | 2 | 0.3333 |
| 5 | 2 | 0.1000 |

**A task whose other attempts were excluded contributes the maximum, and is then averaged with equal weight against tasks measured on their full trial count.** The global `max_k` cap prevents `pass_hat_k` raising on `num_trials < k`; **it does not equalise the denominators.**

**Grade: [E]** throughout — published code, a combinatorial identity, and two quoted documents, all checkable by any reader against the pinned SHA. The code path is **byte-identical between `v1.0.0` and `v1.0.1`.**

**Why this is not a §6 branch:** §6's branches are all about how an *unevaluable unit* is treated. This is about **how evaluable units are combined, and about an instrument publishing one metric name under two stated conventions.** Neither is a question §6 asks, and **the §6 conditions are unaffected by this revision.**

## F-2 · The exclusion is applied on an attribution the code never establishes

`progress.py:92` is a bare `except Exception as e:` with **no type inspection anywhere.** `:120` assigns `INFRASTRUCTURE_ERROR` **unconditionally**. `agent_metrics.py:145` then filters on that label alone.

**And `:124-129` retains `error_type`, the traceback and the attempt count.** The instrument keeps precisely the information that would let it distinguish a provider outage from a model emitting malformed JSON — and does not use it.

**D-8 established at [E] that both reach the same handler.** Genuine infrastructure faults and at least one class of agent failure are excluded under a single label asserting the former.

### Maintainer corroboration, added 27 Aug after D-10

**The maintainers documented this exact failure and repaired one instance of it.** `CHANGELOG.md:103` at `fc0055dc` **[E]**:

> *"Hallucinated tool calls in agent trajectories are now treated as no-ops during `Environment.set_state` replay … instead of raising `ValueError`. Previously, the exception propagated through `run_with_retry`, causing the entire task to be re-run up to `--max-retries` times before being binned as `INFRASTRUCTURE_ERROR` (which is excluded from `pass^k` and `avg_reward` metrics)."*

**A hallucinated tool call is agent behaviour.** It was being excluded under an infrastructure label, the maintainers found it, and v1.0.1 fixes it.

**Two instances, one fixed and one open:**

| Instance | Path | Status at `fc0055dc` |
|---|---|---|
| Hallucinated tool calls in replay | raised `ValueError` → `run_with_retry` → `INFRASTRUCTURE_ERROR` | **Fixed in v1.0.1** (`CHANGELOG.md:103`) |
| Malformed JSON in the model's own tool-call arguments | `json.loads` outside any guard → `run_with_retry` → `INFRASTRUCTURE_ERROR` | **Still live** (`llm_utils.py:440`, D-8) |

**This strengthens F-2 rather than qualifying it.** The class is not hypothetical and not merely inferred by this audit: **the maintainers independently identified it, described its mechanism in the same terms, and closed one route into it.** The second route remains open at the pinned commit.

**Grade: [E].**

**Why this is not a §6 branch:** §6 asks what happens to unevaluable units. This is about whether the instrument is entitled to call them unevaluable. **A metric that excludes on a stated cause it never checked is asserting something it has not earned** — which is the subject of the paper this protocol comes from, appearing in the error handling of an instrument audited for something else entirely.

---

## Calibration against the declared expectation

§2, before the read: *"I expect both to come back negative."* §5a and §6 predicted **Q7 as the MISSCORING landing zone**; §4 predicted the **task-level pass^k structure**.

| Prediction | Outcome |
|---|---|
| Q7 lands on MISSCORING | **Right**, on both repositories |
| §4's task-level structure would be where the pathology could appear | **Right about where to look**; the structure is present and **does not satisfy the conditions** |
| "Both come back negative" | **Right** |

**Across both instruments: five checks, five negatives.** KKBox negative by exclusion, τ-bench negative on all four cells.

**The honest reading of that record.** The mechanism-level predictions were accurate — §4 named the exact place to look and the code had the structure there. **What the plan did not anticipate is that the structure can be present without the conditions being met**, because a code path is not an instantiation. That distinction is now the most useful thing this audit produced about the protocol itself.

---

## What could not be determined

- **Frequency of infrastructure errors**, and therefore whether any task actually persists and keeps accruing them. A property of a run; boundary 8 forbids producing it. **This is why (c) is unestablished rather than refuted.**
- **Whether provider context-window overflow raises** (→ excluded) **or surfaces as `finish_reason == "length"`**, which `llm_utils.py:424-426` only logs as a warning while the run continues on a truncated message. Both paths exist. **[I]**
- **Whether C's NL-assertion `raise` propagated to `INFRASTRUCTURE_ERROR` or crashed the run.** Not settleable without executing. **[I]**

---

## Strongest and weakest evidence

**Strongest.** F-1, the pass^k arithmetic. Four lines of published code and a combinatorial identity, quotable at the pinned SHA, checkable with a calculator, byte-identical across two releases. It requires no reconstruction, no inference, and no trust in the auditor.

**Weakest.** A's 14.55% inaction count. **[I]**, resting on an AST alias analysis that was **wrong twice before it was right** — tuple unpacking broke taint propagation, then over-generous taint misclassified a read-only search tool. It is inferred, and it is the figure most likely to be quoted.

---

## Context — outside the audit's evidence base

> **Marked as outside boundary 7**, which excludes third-party sources from the audit. Included because it bears on significance, not on any condition. **Nothing here was used to answer Q1–Q11.**

τ-bench is published by Sierra. **Anthropic reported Claude 3.7 as top performer on τ-bench**, so it appears in frontier-model reporting. There is a **public leaderboard**, and the July 2026 `v1.0.1` grading update caused **affected leaderboard submissions to be re-graded** — the maintainers themselves treated a grading change as requiring published scores to be recomputed, which corroborates the R2′ decision independently. It is also used in third-party agent evaluation work including the Holistic Agent Leaderboard.

**No claim is made here about internal use at any laboratory. The evidence supports "a benchmark whose scores appear in model reporting and on a public leaderboard" and nothing broader.**

---

## OBSERVATIONS carried forward

Outside Q1–Q11, never folded into an answer.

- **"τ-bench" does not stably identify a version.** It designates the original repository, the `tau2-bench` repository, and `v1.0.1` of that repository; `v1.0.0` is titled τ³-bench; no `tau3-bench` repository exists. **A reader comparing published results across papers cannot resolve which artefact was used from the name alone.** Recorded at pinning, before the read.
- **Two declared terminal states are never assigned:** `CONTEXT_WINDOW_EXCEEDED` and `UNEXPECTED_ERROR` (`simulation.py:1243-1244`).
- **Repository A is dormant but not archived** — no tags ever, zero commits in the 90 days to pinning, final commit pointing readers to the successor. Still installable and citable.
- **The `mock` fixture domain contains six tasks with an empty `reward_basis`**, leaving reward at 1.0 under the multiplicative composition.

---

*Branches assigned under §6 of the frozen plan, applied as written and not adjusted to what was found. Answers in `TAU-ANSWERS.md`; deviations D-6 through D-9 in `DEVIATIONS.md`; analysis scripts in `scripts/tau/`, runnable against the pinned commits under MIT.*

Sources for the context section: [tau2-bench](https://github.com/sierra-research/tau2-bench) · [Sierra, τ-bench](https://sierra.ai/blog/tau-bench-shaping-development-evaluation-agents) · [Holistic Agent Leaderboard](https://arxiv.org/pdf/2510.11977)
