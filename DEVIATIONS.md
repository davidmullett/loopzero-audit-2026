# Deviations log — KKBox / τ-bench audit

Same discipline as the paper's deviations log: **logged when noticed, before investigation**, whether or not it turns out to matter. A deviation logged after its consequences are known is not a deviation log, it's a defence.

**Plan frozen:** 2026-08-24T15:33:01Z
**Plan hash:** `b15f472ef72994970957eda1e1ebc53f5480b759eb6ab71e076496145a7fda0e`
*(two superseded hashes recorded in `PRE-REGISTRATION.sha256` — neither published, nothing read under either)*

---

## Format

**D-n · [short name] · [timestamp noticed]**
What was noticed · what part of the plan it touches · whether it changes §§3–6 · what was done · outcome once resolved.

---

## Entries

**D-1 · Fabricated reviewer credential · 2026-08-24, pre-publication**

**Noticed by:** David, reading the frozen document before posting the hash.

**What was wrong.** The plan described its review as conducted by an *"external specialist reviewer"* who had *"signed off."* That phrasing implies a human expert with standing. The reality is **a separate instance of an AI language model, prompted to act as an adversarial reviewer.** No credential, no institution, no accountability.

**Why it matters more than a wording slip.** The document was minutes from being registered publicly with a permanent DOI. A claim of external expert review is a **credential claim**, and it would have been false in a permanent record — inside a project whose entire subject is instruments that certify things they haven't earned. This is the same failure the project exists to catch, committed by the project.

**Touches §§3–6?** No. The structure, units, questions and decision rule are unchanged. This is a provenance correction, not a methodological one.

**Action.** All "specialist / external review" language replaced with accurate description throughout. **New §11 added — an explicit AI disclosure** stating what the review was, why it is nonetheless recorded (it caught two blocking defects), and why it confers no warrant. Superseded hash recorded in the anchor file rather than omitted. Nothing had been read; nothing had been published.

**Outcome.** Corrected before publication. Logged here rather than silently fixed, because a silent fix is what the log exists to prevent.

---

**D-2 · Release-variant selection resolved post-freeze · 2026-08-27, before the read**

**Noticed by:** Claude Code, proposing a selection rule during the pinning step.

**What was noticed.** The frozen plan fixes the questions and the decision rule but is **silent on which KKBox release to audit**. The competition distributed two labelled sets covering different expiration months. Which one is audited **materially affects the K6 answer**, because K6 concerns behaviour at the edge of the observation window and the two releases have different edges. This is a **researcher degree of freedom the plan left open.**

**⚠️ The disclosure.** The principled rule (**R1** — audit the latest release the competition issued) selects the `_v2` set, whose label window sits harder against the stated `2017-03-31` data horizon. **That is plausibly the release more exposed to a K6 positive.** The rule was proposed on documentation alone and would have been proposed identically had the exposure not been noticed — but it *was* noticed, and it is recorded here rather than left to be found.

**Touches §§3–6?** No. Structure, units, questions and decision rule unchanged. **The plan's silence is a gap being filled, not a provision being departed from.** The "pin one, state it" instruction sits in the mutable `EXECUTION-LOG.md`, not in `PRE-REGISTRATION.md`.

**Action.** Adopted **R1′ — pin both releases** and answer K6 separately for each, reporting both. This **removes the degree of freedom rather than exercising it**, and it simultaneously covers both readings of the documented month-semantics ambiguity, so that ambiguity cannot silently decide K6.

**Outcome.** Resolved **before any data was examined**. If both releases return the same branch, the finding is stronger than either alone; if they differ, **the difference is itself the finding**.

---

**D-3 · Incidental early exposure to the labeller source · 2026-08-27, before the read**

**Noticed by:** Claude Code, immediately on capturing the page text.

**What was noticed.** `WSDMChurnLabeller.scala` is in scope for the read by the 27 Aug ruling, but its full source entered the assisting model's context during the **pinning** step, not the read — Kaggle's Data tab auto-renders the selected file inline, so the body arrived in page text captured while checking the file list for per-file sizes. **No click, no download, no archive opened.**

**Touches §§3–6?** No. Structure, units, questions and decision rule unchanged.

**Why log it anyway.** The plan assumes a sequenced read that begins on authorisation. **This exposure preceded it.** Unlogged, any later finding drawing on the labeller would appear to have come from a clean sequenced read, and **the provenance would be wrong in a way no reader could detect.**

**Action.** Recorded before any analysis.

**Outcome.** **Ruled 27 Aug: proceed with the exposure disclosed.** The exposure **postdates the freeze (`2026-08-24T15:33:01Z`) by three days**, so the registered claim — that the questions and decision rule were fixed before any data or evaluation code was examined — is unaffected. **`PRE-REGISTRATION.md:35` is a statement about the state at freeze time**; it was true then and remains true as a historical claim. The file was in scope for the read by the 27 Aug ruling; **only the sequencing differs from what the plan assumes.** **Recorded state at time of ruling: the source text was present in context, not analysed, and no answer had been formed from it.** **No mitigation is available or appropriate** — the questions are already immutable and public, and **the alternative to disclosure is concealment.**

---

**D-4 · Boundary 6 read as permitting cross-release comparison · 2026-08-27, post-read, pre-verdict**

**Noticed by:** Claude Code, flagging its own interpretation in the answers rather than burying it.

**What was noticed.** K3 requires comparing label-file membership across the two pinned releases. Boundary 6 says *"do not mix files across release variants."* **Read strictly, K3 is unanswerable; read as prohibiting cross-variant derivation rather than cross-release comparison, it is answerable.** The permissive reading was applied — **label membership and labels only, no behavioural quantity derived across mismatched horizons.**

**Touches §§3–6?** No. K3's own text (*"labelled in a later window"*) makes it **cross-release by construction**; the later window is the `_v2` release. R1′ exists to make both releases available.

**⚠️ Disclosure.** The interpretation was made **with the K3 result already visible.** It produces the **less** interesting outcome — the strict reading yields *"cannot be determined,"* the permissive one yields *"not absorbing."* **The incentive here ran against a positive finding.**

**Outcome.** **Ruled 27 Aug: permissive reading stands, K3 answer retained, logged rather than absorbed.**

---

**D-5 · Confirmatory intersection on the K4 residue · 2026-08-27, post-read, results already visible**

**Noticed by:** David, commissioning the check; run by Claude Code.

**What was noticed.** K4 reports a residue of **109,357 labelled users whose reconstructed standing expiry falls outside the February window** — users apparently sitting in the denominator while out of window. If real, that population bears directly on §6 condition (a). If it is reconstruction error, it does not. **A diagnostic run after the read, on results already visible, is exactly the kind of analysis that needs its interpretation fixed before it runs.**

**Pre-committed interpretation, recorded before the run:**

> *Expected result: near-total containment, ~109,357 of the K4 residue falling inside the 111,454 reconstruction-miss set.*
> *(i) If containment is near-total, the K4 residue is **reconstruction error**, not evidence of an in-denominator out-of-window population, and it is **not independent evidence bearing on §6 condition (a)**.*
> *(ii) If containment is substantially partial, the non-contained portion is a **real in-denominator out-of-window population** and must be counted and reported against the 992,931 denominator on its own.*

**⚠️ Direction of the incentive, recorded with the pre-commitment.** The expected outcome **weakens** the case for a positive rather than strengthening it. Branch (i) removes a population that would otherwise look like in-denominator ineligibility.

**Touches §§3–6?** No. This is a diagnostic on the reliability of a reported count, not a change to the questions, the units or the decision rule.

**Result.** Containment is **total: 109,357 of 109,357, 100.0000%.** The reverse containment is 98.1185%; the 2,097-user remainder is exactly the labelled users with no transaction before the cutoff. **Branch (i) is the outcome.**

**⚠️ But the test was degenerate, and that is the more important finding.** Set A is *labelled and reconstructed-expiry-outside-window*; set B is *labelled and not reconstructed into the cohort*, which decomposes as *expiry outside window **or** no history*. **A is a subset of B by construction. The containment could not have come out otherwise, so it is an identity, not an empirical result** — verified in the script rather than asserted (`A <= B: True`; `B \ A == no-history group: True`). **The pre-committed interpretation was written against a test incapable of discriminating between its two branches.**

**What does bear on the question, independently.** The before/after-window split of the residue, which was not predetermined: the residue is **82.87% after-window** against **8.86%** in the overall out-of-window population — a **9.36× enrichment**. That is the signature of expiries revised back into the window after the cutoff, which is what Observation 4 hypothesised. It supports branch (i)'s *conclusion* on evidence that could have come out otherwise.

**Outcome.** **Branch (i) adopted — the K4 residue is not independent evidence bearing on §6 condition (a) — but on the Part 2 enrichment, not on the containment identity.** The degeneracy of the containment test is recorded rather than passed over, because a pre-committed interpretation that cannot fail is not a safeguard, and treating it as one would be the same error this project studies. **The 9.21% cancellation figure in the same script does *not* test the hypothesis**: a post-cutoff cancellation cannot appear in a transaction selected from pre-cutoff history. That limit is stated in the script's own output.

---

**D-6 · τ-bench operational brief written post-KKBox · 2026-08-27, before the τ-bench read**

**Noticed by:** design-partner side, on writing it.

**What was noticed.** `claude-code-brief-KKBOX.md` was written **before** the freeze. The τ-bench brief was written **after** the KKBox read completed and after its branch was assigned. It was composed from **§§4–6 of the frozen plan only**, with **no knowledge of the τ-bench repository held or consulted.**

**Touches §§3–6?** No. **Q1–Q11 are quoted verbatim and unchanged; the hash proves the questions were fixed on `2026-08-24T15:33:01Z`.** What is new is the **operational wrapper** — boundaries, source hierarchy, output format, evidence grading.

**Why log it anyway.** A reader comparing the two briefs will see that one predates the freeze and one does not, and **should not have to guess whether that mattered.** It also records that the person writing the second brief **had already seen a null result**, which is a state the first brief's author did not have.

**Outcome.** **Logged before the read. Brief used as written.**

> **Verification appended 27 Aug, on the brief being checked against the frozen plan before use.** Q1–Q11 confirmed **verbatim** against `PRE-REGISTRATION.md:79–92`; §6's pass^k clause confirmed correctly quoted against `:123`; §4's two-level assignment confirmed accurately represented.
>
> **One discrepancy found and NOT corrected:** `claude-code-brief-TAU.md:75` presents the Q7 constraint as a quotation but **drops the `(§6)` cross-reference** present at `PRE-REGISTRATION.md:81`, with no ellipsis. Meaning unchanged; a passage marked verbatim is not. Reported rather than silently fixed, per the standing rule. Two further abbreviations in the brief's §4 paraphrase — *"cannot persist and keep accruing unrecordable failures"* shortened to *"cannot persist"*, and the omission of `:69`'s closing sentence *"Unit persists, accrues unrecordable failures, counted as success"* — are paraphrase, not quotation, and are recorded for completeness rather than as defects.
>
> **Both corrected on report, 27 Aug, by ruling — not silently.** `:75` now carries `(§6)`, and `:59` is restored to *"cannot persist and keep accruing unrecordable failures"* in full. **The reasons, which are different for each:** a passage marked verbatim must be verbatim, or the mark is worthless; and the shortened §4 phrasing **loses the reason trial level is excluded** — that a terminated trial cannot keep accruing unrecordable failures — **which is load-bearing for Q7**, whose whole constraint turns on condition (c) failing. The `:69` omission was left as written, being paraphrase in a section the brief restates in its own terms.
>
> **Boundary 9 added 27 Aug, by ruling, before the read.** The brief inherited its evidence conventions from the KKBox brief, which was written under a licence that **forbade** publishing the data — so aggregate answers were the ceiling there. **Both τ repositories are MIT, so quotation is permitted, and the ceiling moves.** Boundary 9 records that an answer which could have quoted the governing line and instead paraphrases is **incomplete**, and requires file path and line range at the pinned SHA so a reader can check the quotation against the commit. **Logged because it changes the standard the answers are held to, not merely their formatting** — and because the constraint it replaces came from a different instrument's licence and would otherwise have been carried over unexamined.

---

**D-7 · Completions run after the τ-bench read, results already visible · 2026-08-27, pre-verdict**

**Noticed by:** David, commissioning three completions; run by Claude Code.

**What was noticed.** The τ-bench read left two things open that bear directly on whether the §6 conditions hold: **(1)** whether `k` in B's pass^k is capped globally or per task — the single most consequential open point, because it decides whether one metric name aggregates quantities computed on different denominators; and **(2)** Q7 for repository B, where A's tool-mutation analysis was not replicated, leaving B's equivalent of *"24 of 165"* unestablished. **(3)** is presentational: moving evidence grades to the point of application so no materiality figure can be quoted without its grade.

**⚠️ Disclosure, and it is the mirror image of D-5.** **The expected direction of both (1) and (2) is to STRENGTHEN a positive-shaped finding.** If `k` is per-task, cross-task comparability under a single metric name is compromised, which pushes toward the structure §4 assigned to task level. If B has inaction-satisfiable tasks, B's Q7 surface widens toward A's. **D-5's expected outcome weakened the case for a positive; this one strengthens it.** **This is stated before the results are known**, and it is recorded because a run commissioned after results are visible, with a known favourable direction, is exactly the configuration in which a finding should be distrusted.

**Touches §§3–6?** No. No question is added, no decision rule altered. These complete answers to Q5 and Q7 as already asked.

**Action.** Pre-commitment recorded before either analysis was run. The existing read was committed first (`af459ed`) so that what the completions change is visible as a diff rather than folded into the original.

**Outcome, recorded against the pre-commitment above.**

**(1) `k` — the answer is "both, and they are different quantities."** The **range** of `k` is a single global scalar capped at the minimum surviving trial count across all tasks (`agent_metrics.py:156-166`). The **denominator inside each task's pass^k is per task** — `pass_hat_k(len(df), df.sum(), k)` under a `groupby("task_id")` (`:177-180`), where `len(df)` is that task's own surviving trial count. The suite figure is then an **unweighted mean across tasks** (`compute_metrics:241-244`). Since `C(nᵢ,k)` grows with `nᵢ`, **a task whose other attempts were excluded contributes a higher value for the same absolute successes** — at k=2, `c=2` gives 1.0000 on 2 survivors against 0.1000 on 5. **The global cap prevents an exception; it does not equalise denominators.** **This went in the pre-committed direction.**

**(2) Q7 for B — it went AGAINST the pre-committed direction.** B's inaction-satisfiable count is **11 of 2,556 tasks, 0.43%** — against A's 14.55%. Per domain: airline **0.00%**, telecom **0.00%**, banking_knowledge **4.12%** (below threshold), retail **5.26%** (above, by 0.26 points on 6 tasks). **Four of five domains came back at or near zero.** The expectation recorded before the run was that this would widen B's Q7 surface toward A's. **It did not.**

**Net.** One completion strengthened a positive-shaped reading, one weakened it. **Recording both directions is the point of having stated the expectation first** — had only (1) been run, the disclosure would have looked like a formality; had only (2), like an alibi.

**A methodological finding neither completion was looking for.** B annotates tools `@is_tool(ToolType.WRITE|READ|GENERIC)`, but `toolkit.py:44-49` states that `ToolType` **does not control evaluation-replay behaviour** — `mutates_state` does, and explicit overrides exist in both directions (`banking_knowledge/tools.py:532`, `:602` are `GENERIC` with `mutates_state=True`; `retrieval_mixins.py:186` is `WRITE` with `mutates_state=False`). **Using the obvious annotation would have produced a wrong set in both directions.** Logged because the error was available and was avoided only by reading the annotation's own documentation.

**(3)** Materiality figures now carry **[E]** or **[I]** at the point of application in `TAU-ANSWERS.md`, not only in the methods note. **The result of doing so is itself worth recording: every figure bearing on the 5% threshold is [I].** The only threshold-relevant figures graded **[E]** are B's default-pass routes, at 0.00% and 0.04% — and those fall below it.

---

**D-8 · What can raise into the retry wrapper · 2026-08-27, post-read, pre-verdict**

**Noticed by:** David, commissioning a bounded completion; run by Claude Code.

**What is being established.** `run_with_retry` (`src/tau2/runner/progress.py:19-35`) catches *"any exception"* and, on exhaustion, returns a `SimulationRun` labelled `INFRASTRUCTURE_ERROR`, which `agent_metrics.py:138-145` then removes from the metrics. **Whether that exclusion is defensible depends on what can reach that wrapper.**

**Why it bears on the branch.** The strongest argument against the pass^k structure satisfying §6 condition (c) is that an infrastructure error is a failure of the **harness**, not of the unit being measured — you cannot score an agent on a trial that never ran. **That argument holds only if what reaches the wrapper is genuinely infrastructural.**

**Interpretation fixed now, all three ways:**

> **(i)** If only genuine infrastructural faults can reach it — network, provider API, filesystem, process-level — the exclusion is **declining to measure rather than mismeasuring**. The counter to (c) holds and the positive-shaped reading of B's pass^k weakens.
>
> **(ii)** If agent or user-simulator behaviour can raise unhandled into it — malformed tool arguments, pathological outputs, parse failures escaping in-simulation handling — then **a class of genuine failure is being excluded under an infrastructure label**. The counter to (c) weakens substantially.
>
> **(iii)** If the wrapper does not discriminate at all — a blanket `except Exception` assigning a causal label without establishing the cause — **that is a third finding in its own right: the instrument asserts an attribution it has not earned**, which is the subject of this audit rather than a side note.

**⚠️ Expected direction: unknown.** Unlike D-7, no prediction is being made about which way this goes. **Recorded as genuinely open before the code was read.**

**Touches §§3–6?** No. No question is added. This completes the evidential basis for Q1 and Q5 as already asked.

**Outcome, against the three pre-committed branches. All three are partly realised; none holds alone.**

**(iii) holds outright, and it is the finding that stands on its own.** `progress.py:92` is a bare `except Exception as e:` with **no type inspection**, and `:113-130` assigns `INFRASTRUCTURE_ERROR` **unconditionally**. **The instrument asserts a causal attribution it has not established.** The mitigating detail, recorded with it: `:124-129` retains `"error_type"`, `"error_traceback"` and `"failed_after_attempts"` on the simulation — **the evidence to discriminate is preserved, the label is simply not derived from it, and `agent_metrics.py:145` filters on the label alone.** **[E]**

**(i) holds for the largest classes of in-simulation failure.** Tool-execution errors — malformed arguments included — are caught at `environment.py:474-481` and returned as `ToolMessage(error=True)`, counting toward `TOO_MANY_ERRORS`. Communication-protocol violations become `AgentError`/`USER_ERROR` at `orchestrator.py:684-689`. `MAX_STEPS` and `TIMEOUT` terminate normally. **All are scored 0.0 and retained in the denominator. The exclusion is narrow, not a general escape hatch.** **[E]**

**(ii) holds too, and with a concrete path.** `llm_utils.py:436-443` parses `arguments=json.loads(tool_call.function.arguments)` **outside any `try`** — the guarded blocks close at `:418` and `:429`. **A model emitting invalid JSON raises `JSONDecodeError`, which reaches the wrapper and is excluded as infrastructure.** That is agent behaviour, not a harness fault. `orchestrator.py:690-692` (`except Exception: raise`) and `llm_utils.py:416-418` (`raise e`) provide the propagation path, for the user simulator's LLM as well as the agent's. **[E]**

**So the answer to the question as posed is: what reaches the wrapper is a mixture, and the code does not separate it.** The counter to (c) — *"you cannot score an agent on a trial that never ran"* — **holds for some of the excluded class and not for all of it**, and the published source does not permit the two to be told apart at the point of exclusion. **Whether that suffices for (c) is not decided here.**

**Not determinable without execution. [I]** Whether a provider surfaces a context-window overflow as a raised exception (excluded) or as `finish_reason == "length"`, which `llm_utils.py:424-426` only **logs as a warning** while the run continues truncated. **Both paths exist; which fires is provider- and request-dependent.** This sharpens Q9's open **[I]** and explains the dead enum: the truncation path does not terminate, and the error path is labelled infrastructural. **The relative frequency of each class is likewise a property of a run, not of the code.**

**A second dead enum member, found in passing.** `UNEXPECTED_ERROR` (`simulation.py:1244`) joins `CONTEXT_WINDOW_EXCEEDED` (`:1243`) — grep across `src/` and `tests/` returns the definitions and nothing else. **Neither is ever assigned.** Recorded because the read had reported only one.

**On the pre-commitment.** No direction was predicted, and the result vindicates that: the outcome is not one of the three branches but a compound of all three, which no binary prediction would have captured. **Had a direction been asserted, it would have been wrong.**

---

**D-9 · B · pass^k drafted POSITIVE, reversed to NEGATIVE-exclusion · 2026-08-27, at branch assignment**

**Noticed by:** the AI assistance, re-reading §3 against its own draft.

**What was noticed.** The cell was first drafted **POSITIVE**, on a reading of §6(c)'s *"can continue to accrue"* as a **capability claim satisfied by the existence of a code path.** Re-reading §3 — *"the unit must persist and keep accruing real bad outcomes while being structurally unrecordable"* — **that reading is not supportable. A code path is not an instantiation, and the audit established the path, not the accrual.** Separately, §6(a) asks about **the unit that cannot be evaluated**: the **trial** cannot be evaluated and is **removed**; the **task** can be evaluated and is **retained**. **Neither is unevaluable-and-retained**, which is §6's exclusion definition met exactly.

**Touches §§3–6?** No. **The rule is applied as written; the first draft applied it loosely.**

**⚠️ Direction.** The reversal **moved away from the more interesting finding.** POSITIVE would have been **the only positive-shaped result in five checks** and the **most commercially valuable outcome available.** It was withdrawn on the frozen plan's own text, including the instruction — written for Q7 and applying with equal force here — ***"do not stretch (c) to capture it."***

**Outcome.** **NEGATIVE — exclusion.** The two structural defects that motivated the POSITIVE draft are **retained as F-1 and F-2, reported outside §6 rather than forced into a branch.**

---

**D-10 · Repository release documentation not consulted during the read · 2026-08-27, post-verdict, pre-maintainer-contact**

**Noticed by:** the design-partner side, while researching maintainer contact routes.

**What was noticed.** Boundary 7 names *"the repository's own documentation (README, docs, docstrings)"* as a **primary source.** `RELEASE_NOTES.md`, `CHANGELOG.md` and the GitHub release bodies **are repository documentation and were not read.** During pinning the instruction was explicitly *"do not open the release notes yet — they belong to the read"*; **they were then not opened during the read either.** `TAU-ANSWERS.md` **cites no release documentation anywhere.**

**Touches §§3–6?** No. The questions and decision rule are unchanged. **This is an incomplete source sweep within boundary 7.**

**⚠️ Expected direction, stated before reading.** The v1.0.1 release body **appears to state that leaderboard `pass^k` counts infrastructure-error simulations as failed trials** — a different convention from the code path **F-1** describes. **The expected effect is therefore to weaken F-1, possibly substantially.** Recorded as **expected-to-weaken before the re-read**, not after.

**Outcome.** **The sweep was incomplete as suspected, and what it found is not what was expected.** The release documentation does not simply contradict F-1; **it contains two different `pass^k` conventions and states both**, one of which corroborates F-1 in the maintainers' own words.

**Found, in-tree at `fc0055dc` [E]:**
- `RELEASE_NOTES.md:83` — *"pass^k values are recomputed counting infrastructure-error simulations as failed trials (the leaderboard convention)"*. **This is the statement the expectation was based on, and it is real.**
- `CHANGELOG.md:103` — describing the pre-1.0.1 behaviour of hallucinated tool calls: the exception *"propagated through `run_with_retry`, causing the entire task to be re-run up to `--max-retries` times before being binned as `INFRASTRUCTURE_ERROR` **(which is excluded from `pass^k` and `avg_reward` metrics)**"*. **This agrees with the code and with F-1.**

**So the two in-tree documents disagree with each other**, and the disagreement is reported rather than resolved, per boundary 4. **The pre-committed expectation is not what the evidence shows**: F-1 is neither plainly weakened nor plainly confirmed — the instrument appears to carry two conventions under one metric name, which is a different finding from the one F-1 currently states.

**`CHANGELOG.md:103` also independently corroborates D-8's branch (ii)** — agent-side behaviour excluded under an infrastructure label — **as a bug the maintainers found and fixed in v1.0.1.** That bears on F-2 and was not anticipated at all.

**⚠️ The pre-commitment predicted the wrong direction, and that is worth more in this log than a correct one would have been.** It expected the release documentation to **weaken F-1**. **It did not.** One document (`CHANGELOG.md:103`) **supports F-1 and agrees with the code**; another (`RELEASE_NOTES.md:83`) **contradicts it**. **The conflict between them is a stronger finding than F-1 as originally written** — an instrument publishing one metric name under two stated conventions, with nothing saying which governs a published figure. Had the sweep been done during the read, F-1 would have been written this way from the start. **A pre-commitment that turns out wrong is evidence the pre-commitment was doing work; one that is always right is evidence it was decorative.**

**Also recorded: `v1.0.0` is silent.** Its in-tree `RELEASE_NOTES.md` and `CHANGELOG.md` at `17e07b1d`, and its GitHub release body (111 lines), contain **zero occurrences** of pass^k, infrastructure, exclusion or denominator — and the body has no mention of error, retry, metric, trial or reward. **The conventions question is introduced by v1.0.1 documentation and has no v1.0.0 counterpart.**

**Revision applied 27 Aug, on ruling:** F-1 restated as *"`pass^k` has two documented conventions and the instrument does not reconcile them"*, retaining the denominator arithmetic as what follows under the exclusion convention; F-2 strengthened with the maintainer corroboration and the one-fixed/one-open pair. **No branch assignment touched — F-1 and F-2 sit outside §6 and the conditions are unaffected.**

**Hours: 0.25** for the sweep, **0.2** for the revision.

---

**D-11 · Third-party literature on KKBox read after the read closed · 2026-08-28, post-verdict, pre-publication**

**Noticed by:** the design-partner side. The paper surfaced incidentally in a web search run to find contact addresses for the WSDM Cup organisers, and was then read deliberately.

**What was read.** **arXiv:2607.00473** — Han, Xiao, Wu & Zhang, *"How Early Is Early Enough? Design-Dependent Observation-Window Sufficiency in Subscription Churn Prediction"*, submitted 1 July 2026, cs.LG, CC-BY-4.0. It uses the public KKBox / WSDM Cup 2018 dataset. Read in full, 28 August 2026.

**Why this is logged rather than treated as ordinary background reading.** §2 of the frozen plan declares third-party analyses out of scope, and boundary 7 of the τ-bench brief names them **out of scope** explicitly: *"third-party analyses, blog posts, papers about τ-bench by others… and anyone's conclusions about what the harness does."* That boundary governs **the read**. This was not a read — **`KKBOX-ANSWERS.md` was complete and filed on 27 August and `KKBOX-VERDICT.md` was assigned the same day**, both committed before this paper was opened. **Nothing in the answers or the verdict derives from it, and nothing in either was revisited after it.**

**⚠️ The sequencing is the whole point of logging it.** A related-work citation appearing in the write-up could otherwise look like it informed the audit. **It did not, and the commit history is the evidence:** the answers and verdict are in commits dated 27 August; this entry and `RELATED-WORK.md` are dated 28 August.

**Touches §§3–6?** No. No question, no decision rule, no branch assignment, no count.

**What it changes: nothing in the audit; three things in the write-up.** Recorded in full in **`RELATED-WORK.md`**, summarised here:

1. **It does not anticipate any finding.** No calendar date appears anywhere in the paper — no file horizon, no `20170228`, no observation that the transactions file ends before the labels it explains. `train.csv` is never mentioned, the labeller script is never named, and there is no month-over-month base-rate discussion. **F-1, F-2 and F-3 are all untouched.**
2. **It independently corroborates the instinct.** The authors **re-derive the labels rather than use them**, on a known expiry-date leak — an independent team declining to take the published labels at face value.
3. **Its nearest-neighbour numbers must be distinguished before someone conflates them.** They report 95.7% and 92.1% *label* agreement with `train_v2`; the audit reports **88.78%** *cohort* reconstruction. **Different quantities.** The write-up names the distinction itself rather than waiting to be asked.

**One observation carried to the book notes rather than the paper.** The paper attributes its own 4.3% / 7.9% disagreement to anchoring — *"the gap is anchor-driven, not label noise"* — **with no analysis of the disagreeing users presented.** A cause named rather than established, with the diagnostic step skipped. **That is the same structure as F-2** (`progress.py:120` assigning `INFRASTRUCTURE_ERROR` without inspecting the exception), arriving in an analysis rather than a harness. **It is a Thumb World exhibit, not an audit finding, and must not be reported as one** — it is a reading of someone else's paper, not a code fact.

**Hours: 0.3.**

