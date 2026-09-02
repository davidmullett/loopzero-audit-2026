# τ-bench / τ²-bench — as sent

**Channel:** public GitHub issue, [sierra-research/tau2-bench #497](https://github.com/sierra-research/tau2-bench/issues/497)
**Posted:** 28 August 2026 · **Correction window closes:** 6 September 2026
**Title:** *Pre-registered audit: two documented conventions for pass^k, and a question about which governs published figures*

> **One correction made at the submit step, recorded rather than hidden.** The draft carried the sentence *"which is the reason I'm sending this one privately rather than posting it"* — written while the channel was still undecided, and **false the moment the channel became a public issue.** Caught before posting and corrected. Logged because it would have been a false statement inside the one document whose value rests on not overclaiming.

---
Hello,

I've completed a pre-registered audit of τ-bench and τ²-bench, and I'm bringing it to you before publishing anything. If you reply, your reply will be published verbatim and unedited alongside the findings. If you'd rather not reply, I'll note that I contacted you and had no response.

**What this was.** I fixed eleven questions about how the harness handles trials it can't evaluate, hashed the document, and registered the hash publicly before opening any code — OSF `osf.io/ksm3n`, DOI `10.17605/OSF.IO/KSM3N`, timestamped 24 August. The questions came from a paper of mine on a label-rule defect I found in my own benchmark. **I did not find that defect in yours.** Two other things turned up, and they're why I'm writing.

**Commits audited**
`sierra-research/tau-bench` `main` @ `59a200c6d575d595120f1cb70fea53cef0632f6b`
`sierra-research/tau2-bench` `v1.0.1` @ `fc0055dc4e0a316c3f83133267fbd6faaa770992`
`sierra-research/tau2-bench` `v1.0.0` @ `17e07b1da2bbc0cadfddeea36412686e0604127b`

No benchmark was executed, no model was called, nothing was run. This was a code read.

---

**Finding 1 — two documented conventions for `pass^k`, and I can't tell which produced the published numbers.**

This is a question rather than a defect claim, and it's the main reason I'm writing.

**Three in-tree sources at `fc0055dc` say the metric excludes. One says it counts them as failures.**

**The code excludes.** `agent_metrics.py:145` — `get_metrics_df` filters `INFRASTRUCTURE_ERROR` rows out of the frame before `pass_hat_k` is applied.

**The code says so, in its own warning.** `agent_metrics.py:143`: *"Excluding {infra_count} infrastructure error simulation(s) from metrics."*

**`CHANGELOG.md:103` agrees:** *"…binned as `INFRASTRUCTURE_ERROR` (which is excluded from `pass^k` and `avg_reward` metrics)."*

**`RELEASE_NOTES.md:83` says the opposite:** *"pass^k values are recomputed counting infrastructure-error simulations as failed trials (the leaderboard convention)."*

I can see a reconciliation — that the leaderboard convention is a recomputation separate from the library metric — **but neither document says so**, and I'd rather ask than assume. **Which convention governs a figure published on taubench.com, and is that stated anywhere I've missed?**

**Why it matters under the exclusion convention.** `pass_hat_k` is applied per task group with `len(df)` — that task's *surviving* count — as `num_trials`:

```python
res = df.groupby("task_id")["success"].apply(
    lambda df: pass_hat_k(len(df), df.sum(), k)
)
```

Since it returns `math.comb(success_count, k) / math.comb(num_trials, k)` and `C(n,k)` grows with `n`, the same success count contributes more from a task with fewer surviving trials — at k=2, two successes give **1.0000** on two survivors and **0.1000** on five — and the suite figure is an unweighted mean across tasks. The `max_k` cap prevents `pass_hat_k` raising on `num_trials < k`; it doesn't equalise the denominators.

**You've already met this.** `RELEASE_NOTES.md:83`: *"glm-5-think's trajectory file contains only 3 trials for some tasks, so pass^4 is not recomputable; its previous value is retained."* Unequal per-task trial counts, in the published leaderboard, disclosed by you.

I don't know how often it bites in a live run — that depends on infrastructure-error rates and I executed nothing. The mechanism is in the code; the frequency isn't something a code read can produce.

**Finding 2 — the exclusion is applied on an attribution the code doesn't establish. And you found one instance of this yourselves.**

`progress.py:92` catches with a blanket `except Exception as e:` and `:120` assigns `INFRASTRUCTURE_ERROR` unconditionally, with no inspection of the exception. `agent_metrics.py:145` then filters on that label alone.

Most in-simulation failures don't reach it — tool errors become `ToolMessage(error=True)` and count toward `TOO_MANY_ERRORS`; protocol violations become `AGENT_ERROR`/`USER_ERROR`; `MAX_STEPS` and `TIMEOUT` terminate normally. All scored 0.0 and retained. **The exclusion is narrow.**

**But agent behaviour can reach it, and `CHANGELOG.md:103` documents that you found this too** — hallucinated tool calls propagating through `run_with_retry` and being *"binned as `INFRASTRUCTURE_ERROR`."* Agent failure, excluded under an infrastructure label. Fixed in v1.0.1.

**A second instance appears still live at the pinned commit.** `llm_utils.py:440` parses `arguments=json.loads(tool_call.function.arguments)` **outside any `try`** — the preceding guarded block ends at `:430` and nothing wraps `:431-441`. So a model emitting malformed JSON raises, is retried, is labelled infrastructural, and is excluded. Same class as the one you repaired.

The part I found most striking is that `progress.py:124-129` **retains** `error_type`, the traceback and the attempt count — everything needed to discriminate — and the filter then runs on the label alone.

---

**One observation that runs in your favour, and I want it on the record.**

I audited the original `tau-bench` repository alongside `tau2-bench`, and on the Q7 question — tasks whose goal state is satisfiable by taking no action, so an agent that terminates without acting scores 1.0 — the difference between them is large. In the original: **24 of 165 test tasks, 14.55%**, and 38% in airline. In `v1.0.1`: **11 of 2,556, 0.43%**, with airline and telecom at zero.

I'd assumed I was measuring a static property and found I was measuring an improvement. The τ³ release notes credit the 75+ task fixes to outside analysis (SABER, Cuadron et al.), which is presumably why. **The surface shrank by more than an order of magnitude, and it shrank because you acted on someone else's audit** — which is the reason I'm bringing this to you as a question rather than a write-up, and why nothing gets published until you've had the window.

**Two smaller notes**, offered as observations rather than findings:

`CONTEXT_WINDOW_EXCEEDED` and `UNEXPECTED_ERROR` are declared in `TerminationReason` and assigned nowhere in `src/` or `tests/`.

`v1.0.0`'s in-tree release documentation and its release body say nothing about `pass^k`, infrastructure errors, exclusion or denominators — so Finding 1's conventions question has no `v1.0.0` counterpart to compare against.

And on naming: "τ-bench" currently designates the original repository, the `tau2-bench` repository, and `v1.0.1` of that repository, while `v1.0.0` is titled τ³-bench. A reader comparing published results across papers can't resolve which artefact produced them from the name alone. Not a defect — but the `v1.0.1` grading update required re-grading leaderboard submissions, which suggests version identity already matters to you.

---

**What I'd value from you.** Whether the `pass^k` denominator behaviour is intended, whether infrastructure errors are common enough in practice to matter, and whether I've misread anything. **Corrections are what this window is for** — I'd rather fix an error in email than in public.

**Correction window closes 6 September.** After that I publish the findings, the frozen plan in full, the analysis scripts, and your reply if you send one.

Nothing here has been used commercially and won't be until publication and the window have closed — that's a condition in the registered plan, not a courtesy.

Best,
David Mullett
Independent researcher · ORCID 0009-0004-2543-1664
`d@loopzero.org
