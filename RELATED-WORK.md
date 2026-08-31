# Related work — read after the audit closed

**Filed 28 August 2026.** For the write-up's related-work section.

> ## ⚠️ Sequencing, stated first because it is the point
>
> **Everything in this file was read *after* the audit was complete.** `KKBOX-ANSWERS.md` was filed and `KKBOX-VERDICT.md` assigned on **27 August**, both committed before any paper here was opened. **No answer, count, or branch assignment derives from anything in this file, and none was revisited after reading it.**
>
> §2 of the frozen plan and boundary 7 of the τ-bench brief put third-party analyses **out of scope for the read**. They do not bar related-work checking before publication — but the sequencing has to be visible, or a citation in the write-up looks like it informed the audit. **Logged as `D-11`; the commit dates are the evidence.**

---

## 1 · Han, Xiao, Wu & Zhang (2026)

**"How Early Is Early Enough? Design-Dependent Observation-Window Sufficiency in Subscription Churn Prediction"**
arXiv:2607.00473 · cs.LG · submitted 1 July 2026 · CC-BY-4.0
Xiao Han, Yao Xiao, Chenyu Wu, Tongchen Zhang

**Read in full 28 Aug 2026.** Surfaced incidentally during a search for WSDM Cup organiser addresses, then read deliberately.

### What it is, and why it is not this audit's question

The paper asks **how many days of post-acquisition behaviour suffice as model features**, and finds that the answer is not portable across analysis designs. Its thesis, §VI:

> *"a reported 'N days suffice' is not portable without them"* — them being cohort construction, target horizon, and feature families.

**That is predictive window sufficiency. This audit is about measurement validity** — whether the published labels are checkable and reproducible at all. The paper's *"cohort construction / target definition"* caveat concerns choices **its own authors** make and vary deliberately (survival filters at 180/120 days; anchored `t₀+180` versus moving `(N,180]` targets). **It is not a claim about whether the distributed labels are sound.** §V *"Threats to validity"* covers survivor conditioning, dropped zero-log users, single-dataset scope and dependent folds — **no data-quality content beyond the leak noted below.**

### It does not anticipate F-1, F-2 or F-3

| Audit finding | Status in this paper |
|---|---|
| **F-1** — labels unverifiable against the distributed behavioural files | **Not addressed.** No calendar date appears anywhere in the paper. No file horizon, no `20170228`, no observation of any gap between the label window and the data horizon. All time reasoning is relative to a per-user `t₀`. |
| **F-2** — cohort rule reproduces at 88.78% | **Not addressed as such.** `WSDMChurnLabeller.scala` is never named; the *"date values… modified so it is easier to run on personal laptops"* note is never mentioned; no attempt is made to reproduce **which users the competition placed in the cohort.** The paper builds its own cohort from first principles. |
| **F-3** — churn rate moves 41% between adjacent months | **Not addressed.** `train.csv` is never mentioned; no release comparison; no month-over-month base-rate discussion. Its reported prevalences (8.37%, 0.4264, 0.1358) are for its own constructed designs, not for either published label file. |

**Releases and files used.** `train_v2` only, and only as an external check — all headline results train on self-derived labels. Files: `members`, `transactions`, and *"∼30 GB of daily `user_logs`"*. **No absolute data horizon is stated anywhere in the paper.**

---

### Point 1 · It corroborates the instinct, and is worth citing for that

The authors **re-derive the churn label rather than use the published one**, §II:

> *"we re-derive the label from transactions to avoid the known ∼1% expiry-date leak"*

And §III, *Leakage controls*: *"We do not use the leaked expiry file."*

**An independent team, July 2026, declining to take the published KKBox labels at face value.** Their reason is a leak, not verifiability — so this is **not** support for F-1. **It is support for the weaker and still useful claim that this dataset's labels warrant checking rather than trust.** Cite it that way and no further.

### Point 2 · Their agreement numbers sit next to the 88.78% and must be distinguished

§III, *Dataset and label*:

> *"We report two agreement numbers: (1) the re-derived mechanism reproduces `train_v2` on **95.7%** of March-2017-decision users; (2) the t₀-anchored labels we train on agree with `train_v2` on **92.1%** of overlapping users."*

**These measure a different quantity from the audit's 88.78%.**

- **Theirs:** does a re-derived *label* match the published label, on users already known to be in the cohort.
- **Ours:** does the *cohort* reproduce at all — which users enter `train.csv` in the first place.

**A reader will conflate three percentages in the high eighties and low nineties unless the write-up separates them first.** Do that explicitly rather than waiting to be asked.

**One further distinction worth stating:** the paper's *"following the official labeller logic"* is taken from the prose definition of churn. **No code artefact is cited or run.** The audit read the distributed `WSDMChurnLabeller.scala` (in scope by ruling, `EXECUTION-LOG.md`).

### Point 3 · A question their paper raises about itself — carefully stated

The paper anchors against `train_v2` and re-derives labels from `transactions` using *"no valid renewal within 30 days of expiration."*

**If the transactions file is truncated relative to what that rule requires — which is F-1 — then the re-derivation inherits the truncation.** The `_v2` window is the one the audit finds runs past KKBox's own stated `2017-03-31` history, with only `20170301` of 31 expiry days fully observable inside it.

> **⚠️ This is a question, not a claim, and must stay one.** **The paper never states its data horizon**, so whether the truncation actually bites its re-derivation cannot be established from the text. The audit executed nothing against this paper and makes no assertion about its results.
>
> **What it does establish: F-1 is not academic.** A July 2026 paper re-derives labels from the file whose sufficiency F-1 questions, and does not discuss the question.

---

## Carried to the book notes, not to the paper

On its own 4.3% / 7.9% disagreement, §V:

> *"the gap is anchor-driven, **not label noise**"*

**No analysis of the disagreeing users is presented anywhere in the paper.** The cause is named; the diagnostic step that would establish it is skipped.

**That is the structure of F-2** — `progress.py:120` assigning `INFRASTRUCTURE_ERROR` unconditionally while `:124-129` retains everything needed to discriminate — **arriving in an analysis rather than a harness.**

> **⚠️ This is a Thumb World exhibit and nothing more.** It is a reading of someone else's paper, not a code fact, and it must never appear as an audit finding or be counted among the seven. Rung-3 material handles it; `Rule 10b` applies — **found, not proven common.**

---

## What is *not* here

**No systematic literature search has been run.** This file records one paper that surfaced incidentally and was then read properly. **It is not a related-work survey and must not be presented as one.** If the write-up needs a survey, it is a separate piece of work with its own scope statement — and it too would postdate the read.
