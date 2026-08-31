# Analysis scripts

**Every count in the audit that is not read directly off a file or a line of code was produced by one of these.** They are published so the counts can be checked rather than trusted.

**Licence: MIT** (`LICENSE`). Python **standard library only** — no dependencies, no install step.

---

## ⚠️ No data is published here, and that is a licence condition

**§7.B of the WSDM Cup 2018 competition rules forbids redistributing the Data.** So the KKBOX data is not in this repository and will not be. **§8.B permits publishing code developed against it**, which is the mechanism that lets verification transfer without the data moving.

**To reproduce the KKBOX counts you must accept the competition rules yourself and download your own copy.** That is not a formality — it is the condition under which these scripts are lawful to publish.

**The scripts print aggregates only.** No row value, and no `msno`, is ever emitted. Where `msno` appears in the source it is used as a set member or dictionary key and never printed; the only user-level output is a count. `01_structure.py` states the rule in its own docstring.

---

## Two instruments, two directories

| Path | Instrument | Data required |
|---|---|---|
| `./` | KKBOX / WSDM Cup 2018 churn dataset | **Your own accepted copy.** Both releases. |
| `./tau/` | τ-bench / τ²-bench | **None.** These read task definitions from public MIT-licensed repositories at pinned commits. |

---

## KKBOX scripts

Run in order. Each is independent and prints its own results.

| Script | What it establishes |
|---|---|
| `01_structure.py` | File shapes, row counts, date ranges, distinct user counts per release |
| `02_release_shape.py` | Set relations between the two releases. **Produces the finding that `train_v2.csv` is the original release's test cohort exactly** — 970,960 each, intersection 970,960 |
| `03_cohort_rule.py` | Reconstructs the cohort selection rule under both readings of the labeller's history window. **Produces the 88.78% match rate** that every `[R]`-graded count inherits |
| `04_cancellation.py` | The auto-renew and cancellation confound test used to assess the window-close-day anomaly |
| `05_v2_and_k3.py` | The `_v2` in-release assessment and the February-to-March re-labelling. **Produces the 90.45% `[E†]` unreconstructibility figure and the 4.10% `[E]` re-labelling figure** |
| `06_window_edge.py` | The expiry-day distribution and churn gradient across the observation window |
| `07_residue_containment.py` | The confirmatory containment test on the K4 residue. **See `DEVIATIONS.md` D-5 before reading its output** — the test as originally specified was structurally incapable of failing, and the substantive conclusion came from a different measurement |

`common.py` holds shared path resolution and CSV iteration. **Set the data root there before running anything.**

## τ-bench scripts

No data required; they read task definitions from the pinned public repositories.

| Script | What it establishes |
|---|---|
| `tau/t01_inaction_tasks_A.py` | Inaction-satisfiable task count for `tau-bench` at the pinned commit |
| `tau/t02_inaction_tasks_B.py` | The same for `tau2-bench` v1.0.1 |
| `tau/t03_inaction_tasks_B_mutation.py` | Tool-mutation classification supporting `t02` |

> **⚠️ These three produce the `[I]`-graded counts, and the grade is the point.** The analysis they implement was **wrong twice before it was right** — tuple unpacking broke taint propagation, then over-generous taint misclassified a read-only search tool. **The 14.55% and 0.43% figures are inferred from traced control flow, not executed.** They are the numbers most likely to be quoted and the ones with the weakest evidence grade in the audit. Read `TAU-VERDICT.md` on this before citing either.

---

## Pinned versions

Counts reproduce only against these.

**KKBOX** — both releases as listed in `EXECUTION-LOG.md`, with per-file byte sizes recorded there. Verify your download against that manifest before running anything; all seven files used were byte-verified on arrival.

**τ-bench**

| | Repository | Ref | Commit |
|---|---|---|---|
| **A** | `sierra-research/tau-bench` | `main` | `59a200c6d575d595120f1cb70fea53cef0632f6b` |
| **B** | `sierra-research/tau2-bench` | `v1.0.1` | `fc0055dc4e0a316c3f83133267fbd6faaa770992` |
| **C** | `sierra-research/tau2-bench` | `v1.0.0` | `17e07b1da2bbc0cadfddeea36412686e0604127b` |

*`v1.0.1` is an annotated tag; the tag object is not the commit. The commit SHAs above govern.*

---

## Cost, recorded because a claim depends on it

**Total machine time across all ten scripts: under four minutes** on one laptop core. **Total human effort across both instruments: 3.55 hours.**

That number supports the claim that this kind of check is cheap to run on a public instrument. It is stated plainly rather than favourably: it covers the reads by someone who already knew the plan, and excludes the pre-registration, the review rounds, and the pinning work.

---

*Findings in `KKBOX-VERDICT.md` and `TAU-VERDICT.md`. Questions and decision rule in `PRE-REGISTRATION.md`, frozen and hash-anchored before any of this ran. Deviations in `DEVIATIONS.md`.*
