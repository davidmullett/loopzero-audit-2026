# τ-bench — answers to Q1–Q11

**Read performed 27 August 2026.** Pre-specified plan frozen `2026-08-24T15:33:01Z`, SHA-256 `b15f472ef72994970957eda1e1ebc53f5480b759eb6ab71e076496145a7fda0e`, registered at `osf.io/ksm3n` / `10.17605/OSF.IO/KSM3N` before anything was read.

**No verdict is assigned in this document.** Per boundary 2, the §6 branch assignment is made separately and published with its reasoning.

**The pins, per R2′ in `EXECUTION-LOG.md`. Answered separately throughout; never mixed.**

| | Repository | Ref | Commit |
|---|---|---|---|
| **A** | `sierra-research/tau-bench` | `main` | `59a200c6d575d595120f1cb70fea53cef0632f6b` |
| **B** | `sierra-research/tau2-bench` | `v1.0.1` | `fc0055dc4e0a316c3f83133267fbd6faaa770992` |
| **C** | `sierra-research/tau2-bench` | `v1.0.0` | `17e07b1da2bbc0cadfddeea36412686e0604127b` |

**C is not answered in full.** It exists under R2′ to test whether scoring behaviour changed. The diff comes first, and it determines which questions C is answered for.

**Evidence grades.** **[E]** = read directly off the code or documentation at the pinned commit, quoted. **[I]** = inferred from control flow traced but not executed. Per boundary 9, quotations carry file path and line range at the pinned SHA.

**Nothing was executed.** No agent trial, no model call, no benchmark run, no cost incurred. All counts come from static analysis of source and task JSON.

---

# Part 0 · B against C — the diff, and what it reaches

**The R2′ trigger was `v1.0.1`'s release title, *"banking_knowledge Grading Fixes."* The diff is wider than that title implies, and per instruction I widened rather than held to the stated scope.**

**Scale [E]:** 126 commits, 388 files, between `17e07b1d` and `fc0055dc`.

### What changed in the scoring path

**1 · NL-assertion evaluation went from *raising* to *running*.** In C, a task whose `reward_basis` contained `NL_ASSERTION` under an evaluation type other than `ALL_WITH_NL_ASSERTIONS` **raised**:

```python
if task_reward_basis & nl_bases:
    if evaluation_type != EvaluationType.ALL_WITH_NL_ASSERTIONS:
        raise ValueError(
            "NL assertions are part of the reward basis, but they are not being evaluated."
        )
```

In B that raise is deleted, and the assertions run instead — `evaluator.py:215-216` at `fc0055dc`:

```python
task_needs_nl = RewardType.NL_ASSERTION in task.evaluation_criteria.reward_basis
if evaluation_type == EvaluationType.ALL_WITH_NL_ASSERTIONS or task_needs_nl:
```

**A configuration that previously aborted now produces a score.** This is a change in what happens to an unevaluable configuration, which is Q1/Q3 territory. **[E]**

**2 · A new guard raises when a declared reward component is not evaluated** — `evaluator.py:230-236` at `fc0055dc`, absent in C:

```python
unevaluated = task_reward_basis - evaluated_bases
if unevaluated:
    raise ValueError(
        f"Task reward_basis includes {unevaluated} but these were "
        f"not evaluated. evaluation_type={evaluation_type.value}"
    )
```

**A new failure mode was added while another was removed.** **[E]**

**3 · `strict_replay` was introduced** — `evaluator.py:96`, defaulting `True`, documented at `:110-114`: *"Live evaluation keeps the default (True); trajectory re-grading passes False so recorded outputs that cosmetically predate current tool code do not abort the replay."* **A path now exists in which a replay mismatch does not abort.** **[E]**

**4 · The batch default evaluation type changed** from `ALL_WITH_NL_ASSERTIONS` to `ALL` (`runner/batch.py`). Coherent with change 1: NL assertions no longer need the special type to run. **[E]**

### What did NOT change

- **`pass^k` is byte-identical.** `git diff 17e07b1d..fc0055dc -- src/tau2/metrics/agent_metrics.py` returns **empty**. The computation, the infrastructure-error filter and the `max_k` capping are the same in both. **[E]**
- **`TerminationReason` is untouched** — no member added, removed or renamed. **[E]**
- **Task definitions changed in one domain only:** `banking_knowledge`, 11 task files plus `tasks.json`. **Task count is unchanged, 97 → 97.** No `reward_basis`, `evaluation_criteria` or `nl_assertions` key appears anywhere in the `data/` diff — **zero occurrences**. The edits are to `actions` (`action_id`, `requestor`, `name`, `arguments`, `agent_tool_name`) and to document content. **[E]**

### Which questions C is therefore answered for

| Question | C answered separately? | Basis |
|---|---|---|
| **Q1, Q3** | **Yes** — see below | The raise/run inversion and `strict_replay` change error-path behaviour |
| **Q5, pass^k** | **No — diff shows unaffected** | `agent_metrics.py` identical |
| **Q2, Q4, Q6, Q8, Q9, Q11** | **No — diff shows unaffected** | No change to `TerminationReason`, the orchestrator's termination assignment, the retry wrapper or the metrics denominators |
| **Q7, Q10** | **No — diff shows unaffected for the mechanism** | Reward composition is `reward *= component` in both; the banking task edits change *content*, not *structure* |

**"Not separately answered" here is a recorded finding, not an omission:** for those questions the diff establishes that C's code is the same as B's, so B's answer is C's answer.

### C answered where the diff reaches

**Q1/Q3 in C.** A task with `NL_ASSERTION` in its `reward_basis`, evaluated under any type other than `ALL_WITH_NL_ASSERTIONS`, **raises `ValueError` inside the evaluator** rather than producing a reward. **[E]** In B the same task is scored. Whether the C-era raise propagated to `INFRASTRUCTURE_ERROR` (and thus to exclusion, see Q5) or crashed the run **could not be determined without executing the harness, which boundary 8 forbids.** **[I]-unresolved.**

**Materiality of that difference, measured:** in B, **112 of 114 retail tasks** carry `('DB','NL_ASSERTION')` as their reward basis. Under C's rule, those 112 tasks raise unless run under `ALL_WITH_NL_ASSERTIONS` — which was C's batch default, so in the default configuration they did not raise. **The two releases are consistent in default operation and diverge only off-default.** **[E]/[I]**

---

# Part 1 · Answers

## Q7 · Goal-state-by-inaction — PRIMARY
*Answered at trial level, adjudicated at task level per §4.*

### Repository A — the goal state IS satisfiable by inaction on a material share of tasks

**What the code does.** Reward is computed only on termination, and only by hash comparison — `tau_bench/envs/base.py:124-140` at `59a200c`:

```python
def calculate_reward(self) -> RewardResult:
    data_hash = self.get_data_hash()
    reward = 1.0
    ...
    self.data = self.data_load_func()
    for action in self.task.actions:
        if action.name not in self.terminate_tools:
            self.step(action)
    gt_data_hash = self.get_data_hash()
    info = RewardActionInfo(
        r_actions=data_hash == gt_data_hash, gt_data_hash=gt_data_hash
    )
```

**`reward` starts at 1.0 and is only reduced.** If the reference actions do not mutate the database, `gt_data_hash` equals the hash of an untouched database — so a trial that did nothing produces the same hash and `r_actions` is `True`. With no required `outputs`, the reward remains **1.0**. **[E]**

**How many tasks are in that state.** Static analysis of which tools write through the `data` argument, then of which tasks' reference actions call any of them (`scripts/tau/t01_inaction_tasks_A.py`):

| Suite (test split) | Tasks | No mutating reference action | …and no required outputs |
|---|---|---|---|
| retail | 115 | 9 (7.83%) | **5 (4.35%)** |
| airline | 50 | 20 (40.00%) | **19 (38.00%)** |
| **both** | **165** | 29 (17.58%) | **24 (14.55%)** |

**24 of 165 test tasks — 14.55% — have a goal state that an inactive trial satisfies.** Against the plan's named denominator, 5% of tasks in the suite, this is **above threshold**. **[I]** — the tool-mutation classification is traced statically, not executed.

**⚠️ But the crash path does not reach it, and that materially narrows the finding.** `calculate_reward` is called only under `if done:` (`base.py:114-117`), and `done` is set only by a user `###STOP###` or a terminate tool (`:99`, `:108-109`). A trial that raises is caught in `run.py:89-96` and assigned **`reward=0.0`**; a trial that exhausts its step budget returns the last `env_response.reward`, which is `0` because `done` was never true (`base.py:94`, `tool_calling_agent.py:39-51`). **So a crashed or timed-out trial scores zero, not a pass.** **[E]**

**What reaches the pass-by-inaction state is a trial that terminates *normally* without acting** — the user simulator emitting `###STOP###`, or the agent calling the terminate tool. On the 24 tasks above, **an agent that immediately hands off to a human scores 1.0**: `transfer_to_human_agents` is a terminate tool (`envs/airline/env.py:37`, `envs/retail/env.py:41`), it sets `done`, it is excluded from the reference replay (`base.py:135`), and it mutates nothing. Of those 24 tasks, **19 do not have a transfer in their reference actions at all** (retail 3, airline 15) — the reference solution is something else, and the handoff still scores 1.0. **[I]**

**Rule versus documentation:** the repository's README does not describe the inaction case. **No disagreement to report; an absence.**

### Repository B — the inaction route is closed for abnormal termination, and near-absent by construction

**What the code does.** B gates on termination *before* evaluating — `src/tau2/evaluator/evaluator.py:119-129` at `fc0055dc`:

```python
if simulation.termination_reason not in {
    TerminationReason.AGENT_STOP,
    TerminationReason.USER_STOP,
}:
    return RewardInfo(
        reward=0.0,
        reward_basis=None,
        info={
            "note": f"Simulation terminated prematurely. Termination reason: {simulation.termination_reason.value}"
        },
    )
```

**Any termination that is not a clean agent or user stop scores 0.0 before any evaluator runs.** The repository documents this as a rule: *"Premature termination = 0 reward"* (`src/tau2/evaluator/AGENTS.md:56`). **Code and documentation agree.** **[E]**

**The default-pass route that remains** is `evaluator.py:130-135`:

```python
if task.evaluation_criteria is None:
    return RewardInfo(
        reward=1.0,
        reward_basis=None,
        info={"note": "No evaluation criteria"},
    )
```

**Measured across all five shipped domains (`scripts/tau/t02_inaction_tasks_B.py`): zero tasks have absent evaluation criteria.** 2,556 tasks; **0 (0.00%)**. One retail task has criteria containing no actions, no `communicate_info` and no `nl_assertions` (0.88% of retail). **The default-pass route exists in code and is essentially unpopulated in data.** **[E]**

### B's mutation analysis — completed 27 Aug (D-7). The gap is closed.

**Which annotation governs is itself a finding, and the obvious one is wrong.** B annotates every tool `@is_tool(ToolType.WRITE|READ|GENERIC)`, but `src/tau2/environment/toolkit.py:44-49` says of `ToolType`: *"It does **not** control evaluation-replay behaviour -- see the ``mutates_state`` parameter on :func:`is_tool` for that."* The governing flag is documented at `:72-80`:

> *"mutates_state: Whether this tool mutates environment / DB state. When ``None`` (the default) the value is **inferred** from tool_type: ``True`` for WRITE, ``False`` otherwise. … During evaluation replay (``set_state``), only tools with ``mutates_state=True`` are re-executed; all others are skipped."*

**Taking `ToolType` at face value would have been wrong in both directions**: `banking_knowledge/tools.py:532` and `:602` declare `GENERIC` with `mutates_state=True`, and `banking_knowledge/retrieval_mixins.py:186` declares `WRITE` with `mutates_state=False`. The count below resolves the flag as the decorator does (`toolkit.py:82-83`). **[E]**

**B's equivalent of A's "24 of 165"** — tasks with no state-changing reference action *and* no env assertions, communicate_info or NL assertions, so nothing a no-op trial can fail (`scripts/tau/t03_inaction_tasks_B_mutation.py`):

| Domain | Tasks | Mutating tools | **Inaction-satisfiable** | Share |
|---|---|---|---|---|
| airline | 50 | 6 | **0** | **0.00%** **[I]** |
| retail | 114 | 7 | **6** | **5.26%** **[I]** |
| telecom | 2,285 | 21 | **0** | **0.00%** **[I]** |
| banking_knowledge | 97 | 10 | **4** | **4.12%** **[I]** |
| mock *(fixture)* | 10 | 3 | 1 | 10.00% **[I]** |
| **total** | **2,556** | — | **11** | **0.43%** **[I]** |

**Against the plan's 5%-of-tasks threshold, ~~one domain clears it: retail at 5.26%~~** — six of the 112 tasks whose basis is `('DB','NL_ASSERTION')`. `banking_knowledge` is below threshold overall at 4.12%, but **4 of its 9 `ACTION`-basis tasks (44.44%)** are inaction-satisfiable. **airline and telecom are clean at zero.** **[I]**

> **🔴 Corrected 10 Sept 2026: two domains clear the threshold — mock at 10.00% and retail at 5.26%.** mock was omitted from this sentence and from the verdict's table. **Whether a ten-task fixture domain belongs in a suite-level threshold is a question the frozen plan did not anticipate and this audit does not resolve; both readings are now reported.** Neither changes the branch.

**So B's Q7 surface is real but an order of magnitude smaller than A's** — 0.43% against 14.55% — and it is ~~concentrated in two domains~~ **concentrated in three domains — corrected 10 Sept 2026: retail, `banking_knowledge` and mock; the fixture was omitted here too** rather than general. **Taken with the termination gate at `evaluator.py:119-129`, which already scores every abnormal termination 0.0, B closes most of the route A leaves open.**

**⚠️ The disclosed incentive ran the other way.** D-7 recorded, before this was run, that the expected direction was to **strengthen** a positive-shaped finding. **It mostly did not.** Four of five domains came back at or near zero and the pooled figure is 0.43%. ~~The one figure that clears threshold — retail's 5.26%~~ **corrected 10 Sept 2026: two figures clear it, mock's 10.00% and retail's 5.26%** — retail clears it by 0.26 points on 6 tasks, and **both are [I], not [E]**.

---

## Q1 · Runtime error

**Level: trial.**

**A — scored as a failure, retained.** `tau_bench/run.py:89-96`:

```python
except Exception as e:
    result = EnvRunResult(
        task_id=idx,
        reward=0.0,
        info={"error": str(e), "traceback": traceback.format_exc()},
        traj=[],
        trial=i,
    )
```

**Not excluded, not retried, not passed by default.** The result is appended to `results` like any other and flows into both reported metrics. **[E]**

**B — retried, then excluded.** This is the substantive difference between the repositories. Exceptions are caught by a retry wrapper whose docstring states the outcome — `src/tau2/runner/progress.py:32-35`:

> *"Retries on any exception. If all retries are exhausted, returns a failed SimulationRun with INFRASTRUCTURE_ERROR instead of raising."*

Called at `src/tau2/runner/batch.py:676-681` with `max_retries=config.max_retries`. **The resulting `INFRASTRUCTURE_ERROR` simulation is then removed from the metrics** — `src/tau2/metrics/agent_metrics.py:138-145`:

```python
infra_count = (
    df.termination_reason == TerminationReason.INFRASTRUCTURE_ERROR
).sum()
if infra_count > 0:
    logger.warning(
        f"Excluding {infra_count} infrastructure error simulation(s) from metrics."
    )
    df = df[df.termination_reason != TerminationReason.INFRASTRUCTURE_ERROR]
```

with the function's own docstring at `:132`: *"Filters out infrastructure errors (simulations that never ran)."* The same filter is applied again at `:220-226` when building `evaluated_sims`. **[E]**

**So: A scores runtime errors as failures; B excludes them from the denominator after retrying.** Other in-simulation errors in B (`AGENT_ERROR`, `USER_ERROR`, `TOO_MANY_ERRORS`) are *not* infrastructure errors — they terminate the simulation and score 0.0 via `evaluator.py:119`, remaining in the denominator. **The exclusion is specific to exceptions that survive retry.** **[E]**

**Do code and documentation agree?** In B, yes and explicitly — the exclusion is documented in the docstring and logged at runtime, and `infra_error_count` is carried on `AgentMetrics` (`agent_metrics.py:234`). **It is disclosed, not hidden.** In A there is no documentation of the error path; the code is the only statement. **[E]**

> ### Annotation — what can actually reach the retry wrapper (D-8, completed 27 Aug)
>
> The answer above says exceptions become `INFRASTRUCTURE_ERROR` and are excluded. **What can raise into that wrapper decides whether the exclusion is declining to measure or mismeasuring.** Traced at `fc0055dc`; the answer is mixed, and all three pre-committed branches are partly realised.
>
> **The wrapper does not discriminate.** `progress.py:92` is a bare `except Exception as e:` with **no type inspection anywhere**, and `:113-130` assigns `termination_reason=TerminationReason.INFRASTRUCTURE_ERROR` **unconditionally**. **The causal label is not derived from the cause.** **[E]**
>
> **It does, however, retain the evidence.** `:124-129` records `"error"`, `"error_type": type(last_exception).__name__`, `"error_traceback"` and `"failed_after_attempts"` on the simulation. **The information needed to discriminate is preserved; the label simply is not computed from it, and `agent_metrics.py:145` filters on the label alone.** **[E]**
>
> **What CANNOT reach the wrapper — genuine in-simulation failures are contained. [E]**
> - **Tool-execution errors, including malformed arguments.** `environment.py:474-481` wraps the call: `except Exception as e: resp = f"Error: {e}"; error = True`, returning a `ToolMessage(error=True)`. The orchestrator counts it (`orchestrator.py:326-327`) toward `TOO_MANY_ERRORS`. **A tool failure is scored, not excluded.**
> - **Communication-protocol violations** — empty messages, mixed content-and-tool-calls, solo-mode violations — become `AgentError`/`UserError` and are caught at `orchestrator.py:684-689` into `AGENT_ERROR`/`USER_ERROR`. Scored 0.0, retained in the denominator.
> - **Step-budget and wall-clock exhaustion** — `MAX_STEPS`, `TIMEOUT`. Scored 0.0, retained.
>
> **What CAN reach the wrapper. [E]**
> - **Anything raised during communication validation that is not `AgentError`/`UserError`.** `orchestrator.py:690-692` is explicit: `except Exception: # Re-raise all other exceptions / raise`.
> - **Any exception from either LLM call — the agent's or the user simulator's.** `llm_utils.py:416-418` catches and re-raises: `except Exception as e: logger.error(e); raise e`. Nothing between `generate()` and the wrapper catches it.
> - **⚠️ Malformed JSON in the model's own tool-call arguments.** `llm_utils.py:436-443` parses `arguments=json.loads(tool_call.function.arguments)` **outside any `try`** — the two guarded blocks close at `:418` and `:429`. A model emitting invalid JSON raises `JSONDecodeError`, which reaches the wrapper. **This is agent behaviour, excluded under an infrastructure label.** It is the clearest instance of pre-committed branch (ii).
>
> **What could not be determined without execution. [I]**
> - Whether a given provider surfaces a context-window overflow as a **raised exception** (→ excluded) or as `finish_reason == "length"`, which `llm_utils.py:424-426` only **logs as a warning** while the run continues on a truncated message. **Both paths exist in the code; which fires is a provider- and request-dependent fact.** This sharpens Q9's open **[I]** and explains why `CONTEXT_WINDOW_EXCEEDED` is never assigned: **the truncation path does not terminate, and the error path is labelled infrastructural.**
> - The relative frequency of each class in a real run. **A property of a run, not of the code.**
>
> **Two dead enum members, not one.** `UNEXPECTED_ERROR` (`simulation.py:1244`) joins `CONTEXT_WINDOW_EXCEEDED` (`:1243`): grep across `src/` and `tests/` returns the definitions and nothing else. **Neither is ever assigned.** **[E]**

## Q2 · Timeout / step-budget exhaustion

**Level: trial.**

**A — scored as a failure.** The agent loop is bounded at `tau_bench/agents/tool_calling_agent.py:28,39`: `def solve(self, env, task_index=None, max_num_steps: int = 30)` … `for _ in range(max_num_steps):`. On exhaustion the loop simply ends and `SolveResult` carries the last `env_response.reward`, which is `0` because `reward` is only assigned on `done` (`envs/base.py:94,114-116`). **No timeout path exists at all** — there is no wall-clock limit in A. **[E]**

**B — scored as a failure, with named reasons.** `src/tau2/orchestrator/orchestrator.py:744-750`:

```python
if self.step_count >= self.max_steps:
    self.done = True
    self.termination_reason = TerminationReason.MAX_STEPS
if self.num_errors >= self.max_errors:
    self.done = True
    self.termination_reason = TerminationReason.TOO_MANY_ERRORS
```

and a wall-clock timeout at `:233` setting `TerminationReason.TIMEOUT`. **All three are outside `{AGENT_STOP, USER_STOP}`, so all three yield reward 0.0** at `evaluator.py:119-129`, and all three stay in the denominator — they are not infrastructure errors. **[E]**

## Q3 · Unclassifiable terminal state

**Level: trial.**

**A — no such category exists.** Reward is binary by construction: `r_actions` is a hash equality, and outputs are substring checks (`base.py:139,150-161`). Anything that is neither a hash match nor a completed output check is a 0. **An unclassifiable state is scored as a failure by default, not flagged.** **[E]**

**B — the category is named and scored as a failure.** `TerminationReason` includes `UNEXPECTED_ERROR` (`src/tau2/data_model/simulation.py:1244`), which like all non-stop reasons yields 0.0. **[E]**

**⚠️ One member of that enum is never assigned.** `CONTEXT_WINDOW_EXCEEDED` (`simulation.py:1243`) appears **nowhere else in `src/` or `tests/`** — grep returns the definition and nothing more. **A terminal state is declared but no code path produces it.** See Q9. **[E]**

## Q4 · Retry semantics

**Level: trial.**

**A — no retry of any kind.** No retry logic appears in `run.py`, in the agent loop, or in the environment. Each `(task, trial)` pair is executed once and its result recorded. **[E]**

**B — retries exist and replace the original.** `run_with_retry` (`src/tau2/runner/progress.py:19-35`) retries on any exception up to `max_retries`, and **only the final `SimulationRun` is returned** — earlier attempts are not scored alongside. A second, distinct mechanism re-runs on detected hallucination (`batch.py:690-700`), overwriting `result` in place, bounded by `config.hallucination_retries` and applied to full-duplex runs only. **In both cases the retry is scored *in place of* the original, not alongside it.** **[E]**

**Consequence worth stating plainly and not folding into Q1:** because a retried-and-still-failing trial becomes `INFRASTRUCTURE_ERROR`, and `INFRASTRUCTURE_ERROR` is filtered from the metrics, **the retry mechanism and the exclusion mechanism compose**: repeated infrastructure failure on the same trial removes it from the denominator rather than recording it. **[E]**

## Q5 · pass^k composition

**Level: task.** *Reported in full in Part 2 below, per the plan's instruction that pass^k gets its own branch.*

## Q6 · Denominator

**Level: task and trial.**

**A — two metrics, two different denominators, both of which include errors.** `tau_bench/run.py:180-199`:

- **Average reward** — `avg_reward = sum(rewards) / len(rewards)` at `:186`. Denominator = **every attempted trial**, including those that raised, since the exception handler still appends a result. **[E]**
- **pass^k** — `sum_task_pass_hat_k / len(c_per_task_id)` at `:199`. Denominator = **the number of distinct task ids that produced any result**. `num_trials` is `len(set([r.trial for r in results]))` at `:184` — derived from the results, not from the configured trial count. **[E]**

**B — one filtered denominator feeding both.** `get_metrics_df` (`agent_metrics.py:129-166`) removes `INFRASTRUCTURE_ERROR` rows, then `avg_reward = df.reward.mean()` (`:238`) and pass^k are both computed from the filtered frame. **The difference between attempted and evaluated is carried explicitly as `infra_error_count`** rather than discarded. **[E]**

**Which named reported metric does each feed?** In both repositories, the two named metrics are **average reward** and **pass^k**, printed by `display_metrics` (A, `run.py:200-203`) and assembled into `AgentMetrics` (B, `agent_metrics.py:202+`). **[E]**

## Q8 · User-simulator failure

**Level: trial.**

**A — not distinguished from agent error.** The ReAct user simulator raises on a response it cannot parse — `tau_bench/envs/user.py:146`: `raise ValueError(f"Invalid response format: {response}")`. That exception propagates through `env.step` and `agent.solve` into the single generic handler at `run.py:89`, producing the same `reward=0.0` with a string in `info["error"]` as any other failure. **A user-simulator malfunction and an agent failure are recorded identically.** **[E]**

**B — distinguished, by design.** `TerminationReason.USER_ERROR` and `TerminationReason.AGENT_ERROR` are separate members (`simulation.py:1240-1241`), assigned at separate sites (`orchestrator.py:686` agent, `:689` user), and reported separately in the termination breakdown (`agent_metrics.py:331-333`). **Both still score 0.0** and both remain in the denominator. **[E]**

## Q9 · Cost / token-budget exhaustion

**Level: trial.**

**A — cost is measured, never enforced.** `total_cost` accumulates per step (`tool_calling_agent.py:30,48`) and user cost is recorded (`envs/base.py:118`), but **no threshold is compared anywhere and no termination path consults cost.** A run cannot end for budget reasons. **[E]**

**B — a terminal state is declared for it and nothing produces it.** `CONTEXT_WINDOW_EXCEEDED` exists in the enum (`simulation.py:1243`) and is assigned nowhere in the repository. No `max_cost`, `cost_budget` or `token_budget` termination path exists. **[E]**

**So for both repositories the honest answer is: cost/token exhaustion is not a distinct handled path.** In A it is not represented; in B it is represented in the type system and unimplemented. **Whether a provider-side context-window error surfaces as a generic exception — and therefore, in B, as a retried `INFRASTRUCTURE_ERROR` — cannot be determined without executing the harness**, which boundary 8 forbids. **[I]-unresolved.**

## Q10 · Partial goal satisfaction

**Level: trial.**

**A — all-or-nothing.** `r_actions` is a single hash equality (`base.py:139`); any output not found sets `r_outputs = 0.0` **and** `reward = 0.0` (`:159-161`). There is no intermediate value. **[E]**

**B — components are multiplied, so partial credit is possible in principle and eliminated in practice.** `evaluator.py` composes `reward *= env_reward_info.reward`, `reward *= action_reward_info.reward`, `reward *= nl_reward_info.reward` over the components in the task's `reward_basis` (`:240-252`). **A product of components each in [0,1] admits fractional rewards**, and `is_successful` treats only ≈1.0 as a success (`agent_metrics.py:151`). **So a partially satisfied task lands strictly between 0 and 1, is not a success for pass^k, but does raise `avg_reward`.** **[E]** for the composition; **[I]** for the claim that components are individually fractional, which I traced but did not execute.

## Q11 · Agent refusal as a terminal state that is not an error

**Level: trial.**

**A — refusal terminates and is then scored by DB comparison.** `transfer_to_human_agents` is registered as a terminate tool in both domains (`envs/airline/env.py:37`, `envs/retail/env.py:41`); calling it sets `done = True` (`base.py:108-109`) and triggers `calculate_reward`. It is excluded from the reference replay (`base.py:135`). **It is not an error and is not recorded as one.** **[E]**

**⚠️ Combined with Q7 this is the sharpest structure in A**: on the 24 test tasks whose goal state needs no DB change, **an immediate refusal scores 1.0** — and on **19 of those 24** the reference solution does not involve a transfer at all. **[I]**

**B — refusal is a clean stop.** The transfer tool is the agent's stop signal (`src/tau2/agent/llm_agent.py:330`: `TRANSFER_TOOL_NAME = "transfer_to_human_agents"`), producing `AGENT_STOP`, which passes the `evaluator.py:119` gate and is then evaluated normally against the task's criteria. **Not an error; scored on the merits.** **[E]**

---

# Part 2 · pass^k, reported on its own

*Per §6: "pass^k is a different object from a per-trial score. State separately whether unevaluable trials enter it as failures, exclusions, or passes, and report that finding on its own rather than folded into Q1–Q3."*

### Repository A — unevaluable trials enter pass^k as **failures**

`tau_bench/run.py:181-199`:

```python
def is_successful(reward: float) -> bool:
    return (1 - 1e-6) <= reward <= (1 + 1e-6)
...
c_per_task_id[result.task_id] += 1 if is_successful(result.reward) else 0
...
sum_task_pass_hat_k += comb(c, k) / comb(num_trials, k)
```

An errored trial carries `reward=0.0`, so `is_successful` is `False`, so it decrements no counter but **is counted in `num_trials`** via `len(set([r.trial for r in results]))`. **It enters as a failure and stays in the denominator.** **[E]**

### Repository B — unevaluable trials enter pass^k as **failures, except infrastructure errors, which are excluded**

`agent_metrics.py:169-191`:

```python
df, max_k = get_metrics_df(results)
...
res = df.groupby("task_id")["success"].apply(
    lambda df: pass_hat_k(len(df), df.sum(), k)
)
```

`get_metrics_df` has already removed `INFRASTRUCTURE_ERROR` rows. **Per task, `num_trials` is `len(df)` — the count of that task's *surviving* trials — and `success_count` is the sum over the same survivors.** So a task whose trials repeatedly fail infrastructurally is scored on the attempts that ran, while **remaining in the suite denominator**, since `groupby("task_id")` still yields a row for it. **[E]**

**This is the exact structure §4 pre-assigned to task level**: *"If unevaluable trials are dropped and pass^k is computed over the survivors, the task remains in the suite denominator with a score derived only from its evaluable attempts."* **Reported, not adjudicated — the branch assignment is not mine to make.**

### ⚠️ Is `k` capped globally or per task? Completed 27 Aug (D-7). **Both — and they are different quantities.**

This was the read's most consequential open point, and the answer is that two distinct things are named `k`.

**The k RANGE is global.** `agent_metrics.py:156-166`:

```python
max_k = df.info_num_trials.max()
task_ids_counts = [(tid, count) for tid, count in df.task_id.value_counts().items()]
task_ids_counts.sort(key=lambda x: x[1])
min_k = task_ids_counts[0][1]
if min_k < max_k:
    logger.warning(...)
    max_k = min_k
return df, max_k
```

One scalar, the minimum surviving trial count across **all** tasks, bounding which `pass^k` columns are produced. **[E]**

**The DENOMINATOR inside each task's pass^k is per task.** `agent_metrics.py:177-180`:

```python
for k in range(1, max_k + 1):
    res = df.groupby("task_id")["success"].apply(
        lambda df: pass_hat_k(len(df), df.sum(), k)
    )
```

`len(df)` inside the lambda is the size of **that task's group** — its own surviving trial count — passed as `num_trials` to `pass_hat_k(num_trials, success_count, k)`, which returns `math.comb(success_count, k) / math.comb(num_trials, k)` (`:126`). **[E]**

**And the suite figure is an unweighted mean across tasks** — `compute_metrics:241-244`:

```python
for column in df_pass_hat_k.columns:
    if match := re.match(r"pass\^(\d+)", column):
        k = int(match.group(1))
        pass_hat_ks[k] = df_pass_hat_k[column].mean()
```

**[E]**

**What this means for cross-task comparability under a single metric name.** For a reported `pass^k`, task *i* contributes `C(cᵢ, k) / C(nᵢ, k)` where `nᵢ` is *that task's* surviving trials — and the `nᵢ` need not be equal. Since `C(nᵢ, k)` grows with `nᵢ`, **the same absolute number of successes yields a higher contribution from a task with fewer survivors.** Computed from the published formula, at k=2:

| Surviving trials *n* | Successes *c* | Contribution to `pass^2` |
|---|---|---|
| 2 | 2 | **1.0000** |
| 3 | 2 | 0.3333 |
| 4 | 2 | 0.1667 |
| 5 | 2 | 0.1000 |

**A task whose other attempts were excluded as infrastructure errors contributes the maximum value, and is then averaged with equal weight against tasks measured on their full trial count.** The global cap prevents `pass_hat_k` from raising on `num_trials < k` (`:124-125`); **it does not equalise the denominators.** So `pass^k` as reported is a mean over per-task quantities that were not computed on a common base. **[E]** for the code and the arithmetic; **[I]** for the claim that this occurs in practice, which depends on infrastructure errors actually arising in a run and cannot be established without executing the harness.

**Two mitigations are present in the same code and must be reported with it.**

1. **`k` is capped at the minimum surviving trial count**, with a warning — `agent_metrics.py:158-165`:

```python
min_k = task_ids_counts[0][1]
if min_k < max_k:
    logger.warning(
        f"The minimum number of trials for a task is {min_k}, which is less than the expected number of trials {max_k}. Setting max k to {min_k}."
    )
    max_k = min_k
```

So exclusions on one task **lower `k` for the whole suite** rather than silently inflating that task's score at full `k`.

2. **The exclusion is counted and surfaced**: `infra_error_count` is computed at `:217-221` and carried on the returned `AgentMetrics`, and a warning is logged at `:142-144`. **[E]**

> ### Annotation — what the excluded class contains (D-8, completed 27 Aug)
>
> The section above reports that `INFRASTRUCTURE_ERROR` trials leave the pass^k denominator while their task stays in the suite. **The completion establishes what that excluded class contains, which is what decides whether the exclusion is defensible.**
>
> **It is not purely infrastructural.** Alongside network, provider and process faults, the class admits **malformed JSON in the model's own tool-call arguments** (`llm_utils.py:436-443`, parsed outside any guard) and **any non-protocol exception re-raised from communication validation** (`orchestrator.py:690-692`). **So a trial can leave the denominator because the agent emitted output the harness could not parse.** **[E]**
>
> **It is also not exhaustive of failure.** Tool errors, protocol violations, step-budget exhaustion and timeouts are all contained in-simulation and scored 0.0 in the denominator. **The exclusion is narrow — it is not a general escape hatch for failing trials.** **[E]**
>
> **The attribution itself is unearned, and that is reportable independently of the branch.** `progress.py:92` catches `Exception` without inspecting it and `:120` labels the result `INFRASTRUCTURE_ERROR` regardless of cause, while `:124-129` retains the `error_type` that would have permitted a distinction. **The instrument records enough to tell these apart and does not use it.** Whether that bears on §6 condition (c) is not decided here.
>
> **Frequency is unmeasurable from the code. [I]** How often each class arises — and therefore how much of the denominator moves — is a property of a run, and boundary 8 forbids producing one.

> ### Annotation — the release documentation, swept after the read (D-10, 27 Aug)
>
> **Boundary 7 names the repository's own documentation a primary source. `RELEASE_NOTES.md`, `CHANGELOG.md` and the release bodies were not read during the read.** This document cited none of them. Swept afterwards; **no answer above is revised, and the §6 branch assignments are untouched.**
>
> **The instrument states two conventions for `pass^k`, at the same pinned commit `fc0055dc`.**
>
> - **`CHANGELOG.md:103` [E]** — `INFRASTRUCTURE_ERROR` *"(which is excluded from `pass^k` and `avg_reward` metrics)"*. **Agrees with `agent_metrics.py:138-145` and with what Part 2 reports.**
> - **`RELEASE_NOTES.md:83` [E]** — *"pass^k values are recomputed counting infrastructure-error simulations as **failed trials** (the leaderboard convention)"*. **Disagrees.**
>
> **Nothing in either document states which convention governs a published figure.** A reconciliation is available — that the leaderboard convention is a recomputation separate from the library metric — **but neither says so, and this audit does not supply it.** Per boundary 4 both are reported and the disagreement is left standing. **F-1 in `TAU-VERDICT.md` is restated around the conflict.**
>
> **A disclosed instantiation of the unequal-denominator mechanism [E]**, same line: *"glm-5-think's trajectory file contains only 3 trials for some tasks, so pass^4 is not recomputable; its previous value is retained."* **Unequal per-task trial counts in the published leaderboard, with a prior figure carried forward.**
>
> **Maintainer corroboration for the D-8 annotation above [E].** `CHANGELOG.md:103` documents that **hallucinated tool calls — agent behaviour — previously propagated through `run_with_retry` and were binned as `INFRASTRUCTURE_ERROR`**, and that v1.0.1 fixes that route. **The class this audit identified is one the maintainers independently identified and partly closed.** The second route, malformed JSON at `llm_utils.py:440`, **remains open at the pinned commit.**
>
> **`v1.0.0` is silent** on all of it — zero occurrences of pass^k, infrastructure, exclusion or denominator in its in-tree documentation or release body. **[E]/[D]**
>
> **Grades: [E]** for in-tree documentation quoted at the pinned commit; **[D]** for GitHub release bodies, which are maintainer-published but live outside the tree.

---

# Part 3 · Counts against the named denominator

The plan fixes materiality at **5% of tasks in the suite**.

| State | Tasks | Denominator | Share | Grade |
|---|---|---|---|---|
| **A** · goal state satisfiable by inaction — airline | 19 | 50 | **38.00%** | **[I]** |
| **A** · goal state satisfiable by inaction — retail | 5 | 115 | **4.35%** | **[I]** |
| **A** · both suites combined | 24 | 165 | **14.55%** | **[I]** |
| **A** · of those, reference expects no transfer | 19 | 165 | 11.52% | **[I]** |
| **B** · tasks with no evaluation criteria (default pass) | 0 | 2,556 | **0.00%** | **[E]** |
| **B** · criteria present with nothing to check | 1 | 2,556 | 0.04% | **[E]** |
| **B** · inaction-satisfiable — retail | 6 | 114 | **5.26%** | **[I]** |
| **B** · inaction-satisfiable — banking_knowledge | 4 | 97 | 4.12% | **[I]** |
| **B** · …of its `ACTION`-basis subset | 4 | 9 | 44.44% | **[I]** |
| **B** · inaction-satisfiable — airline | 0 | 50 | **0.00%** | **[I]** |
| **B** · inaction-satisfiable — telecom | 0 | 2,285 | **0.00%** | **[I]** |
| **B** · inaction-satisfiable — all domains | 11 | 2,556 | **0.43%** | **[I]** |

**Which of these clear the 5% threshold, with the grade attached at the point of application:**

- **A · airline, 38.00% [I]** — clears by a wide margin, on inferred tool classification.
- **A · both suites, 14.55% [I]** — clears, same basis.
- **A · retail, 4.35% [I]** — **does not clear.**
- **B · retail, 5.26% [I]** — clears **by 0.26 points, on 6 tasks**, inferred not read.
- **B · banking_knowledge, 4.12% [I]** — does not clear; its `ACTION`-basis subset does, on 4 tasks of 9.
- **B · airline and telecom, 0.00% [I]** — do not clear.
- **B · default-pass routes, 0.00% and 0.04% [E]** — do not clear. **These are the only threshold-relevant figures in this document graded [E].**

**Every figure bearing on the 5% threshold is [I].** Not one of the counts that clears it is read directly off the code; each depends on the inference that "no state-changing reference action" implies "goal state equals initial state". **[E]** attaches to the annotations and the code paths, not to the prevalence.

**Denominator note.** For A the suite is the test split, which is what the repository reports. For B, `telecom` alone carries 2,285 of 2,556 tasks, so the pooled 0.43% is dominated by a domain that scores zero; the per-domain figures above are the ones that bear on materiality.

**Cannot be counted without execution:** the frequency of infrastructure errors, and therefore how many trials B's filter actually removes in practice. **That is a property of a run, not of the code**, and boundary 8 forbids producing it.

---

# OBSERVATIONS (not findings)

Outside Q1–Q11. Reported separately per boundary 1.

**1 · "τ-bench" does not stably identify a version.** The name designates the original repository, the `tau2-bench` repository (whose GitHub description reads *"τ-Bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"*), and `v1.0.1` of that repository (release title *"τ-bench 1.0.1"*). `v1.0.0` of the same repository is titled *"τ³-bench 1.0.0"*. There is no `tau3-bench` repository. The original repository's final commit is *"Merge pull request #80 from sierra-research/update-readme-tau3-bench."* **A reader comparing published results across papers cannot resolve which artefact was used from the name alone.** Recorded at pinning in `EXECUTION-LOG.md` before the read began.

**2 · Repository A is dormant but not archived.** 93 commits, last `2026-03-18`, zero in the 90 days to the pin date; no tags, ever. It remains installable and citable, and its last act was to point readers elsewhere.

**3 · The `mock` domain contains six tasks with an empty `reward_basis`.** Under `evaluator.py`'s composition, `reward` starts at 1.0 and is multiplied only by components present in the basis — so an empty basis leaves 1.0. `mock` is a fixture domain and is not a reported suite, which is why this is an observation and not part of Q7.

**4 · A's `Env.__init__` and `reset` can select an out-of-range task index.** `envs/base.py:69` and `:80` both use `random.randint(0, len(tasks))`, whose upper bound is inclusive; `tasks[len(tasks)]` would raise. Reached only when no `task_index` is supplied, which the runner always supplies (`run.py:73`). **Latent, not live.**

**5 · A's reward info object is replaced, not merged, when outputs are checked.** `base.py:138-162`: `info` is first a `RewardActionInfo`, then reassigned to a `RewardOutputInfo` if the task has outputs — so for those tasks the DB-hash detail (`r_actions`, `gt_data_hash`) is absent from the recorded result even though it determined the reward.

---

# Judgement calls

**1 · Classifying which tools mutate the database (A).** A's inaction count depends on it, and no annotation exists in the repository, so I wrote an AST alias analysis. **It was wrong twice before it was right**, and both corrections are visible in the script's design: tuple unpacking (`products, orders, users = data["products"], ...`) initially broke taint propagation and understated mutators; then over-generous taint marked `search_onestop_flight` as mutating because a fresh dict comprehension mentioned a tainted name. The final classification — retail 7 mutators, airline 6 — matches the tools' semantics on inspection. **Every count derived from it is graded [I], not [E].**

**2 · Treating "no mutating reference action + no required outputs" as "inaction-satisfiable."** This is the condition under which `gt_data_hash` equals the initial hash. It does not prove a real agent would score 1.0 by doing nothing — the user simulator must also terminate. **I did not execute anything to confirm it.**

**3 · Which C questions to answer separately.** I answered C only where the diff reaches, and recorded the rest as diff-shows-unaffected. The alternative — a full Q1–Q11 pass on C — would have produced three near-identical answer sets and obscured the two places the releases actually differ.

**4 · Reporting B's exclusion mitigations alongside the exclusion.** The `max_k` cap and `infra_error_count` could have been left to the verdict stage. I report them in Part 2 because omitting them would make the exclusion look undisclosed when the code discloses it.

**5 · ~~Not replicating the mutation analysis for B.~~ CLOSED 27 Aug under D-7.** It was the read's largest gap; it is now answered above. **The completion changed one thing about how it should be read:** B's tools are annotated, so the classification is **[E]** rather than the **[I]** it was for A — but the annotation that looks authoritative (`ToolType`) is documented as *not* governing replay, and using it would have produced a wrong set in both directions. **The lesson generalises past this repository: an annotation is only evidence for what its own documentation says it controls.**

**6 · Which criteria count as "nothing a no-op trial can fail" (B).** I required no state-changing reference action **and** no env assertions, no `communicate_info`, no NL assertions. A looser test — ignoring communicate/NL — would raise B's counts. **The stricter reading was chosen before the counts were seen**, on the ground that a task requiring the agent to *say* something is not satisfied by silence.

---

# Hours

| Task | Hours |
|---|---|
| Brief verification against the frozen plan; boundary 9 added; D-6 annotated | 0.15 |
| B-versus-C diff: scoring path, error handling, pass^k, task definitions | 0.30 |
| Repository A read: runner, env, agent, user simulator, tools | 0.35 |
| Repository A static analysis: tool mutation classification, two corrections, task counts | 0.40 |
| Repository B read: evaluator, orchestrator, metrics, runner, retry path | 0.35 |
| Repository B task counts | 0.15 |
| Writing this document | 0.40 |
| **Total** | **2.10** |

Wall-clock 12:30–13:05. No execution, no API calls, no cost.

---

*Answers only. No branch assigned — that is made separately, under §6 of the frozen plan, and published with its reasoning.*
