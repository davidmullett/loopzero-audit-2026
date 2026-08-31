# KKBOX — answers to K1–K6

**Read performed 27 August 2026.** Pre-specified plan frozen `2026-08-24T15:33:01Z`, SHA-256 `b15f472ef72994970957eda1e1ebc53f5480b759eb6ab71e076496145a7fda0e`, registered at `osf.io/ksm3n` / `10.17605/OSF.IO/KSM3N` before anything was read.

**No verdict is assigned in this document.** Per boundary 2 of the brief, the branch assignment under §6 of the frozen plan is made separately and published with its reasoning. What follows is what the rule says and what the data does.

**Releases.** Both pinned releases are answered, per R1′ in `EXECUTION-LOG.md`. Within every answer, files are used only from the release being answered.

| | Original release | `_v2` refresh |
|---|---|---|
| Labels | `train.csv` — 992,931 users | `train_v2.csv` — 970,960 users |
| Behaviour | `transactions.csv` — 21,547,746 rows, dates `20150101`–`20170228` | `transactions_v2.csv` — 1,431,009 rows, dates `20150101`–`20170331` |
| Expiry window | February 2017 | March 2017 |

**Sources cited below.** *Doc* = the competition data-description page. *Labeller* = `WSDMChurnLabeller.scala`, in scope per the 27 Aug ruling, with the provenance caveat in `DEVIATIONS.md` D-3. *Script* = the analysis scripts in `scripts/`, which anyone who has accepted the competition rules can run against their own copy.

### Dependency marking — read this before quoting any number

The cohort rule reproduces at **88.78%** (Observation 4). Stating that gap once is not enough, because it does not fall on every figure equally. **Every count in K4 and K6 is marked:**

- **[E] Exact.** Read directly from the distributed files — a row count, a file's date range, a set-membership test against a label file, or arithmetic on those. No model of the cohort rule is involved. **Robust to the reconstruction gap.**
- **[R] Reconstruction-dependent.** The group being counted, or the quantity itself, is defined by the reconstructed cohort rule. **Carries the 11.22% gap.**
- **[E†] Exact given the cutoff.** Direct from the files, but conditioned on the `20170131` / `20170228` cutoff being the right window boundary — a reading, per Judgement call 2, not a reconstruction.

> **One correction to how this was framed when the labelling was commissioned.** K4's headline figure is **not** independent of the reconstruction. The *membership test* — is this user in `train.csv`? — is exact. But **the group being tested is defined by reconstructed expiry**, so the numerator, the denominator and the percentage all inherit the gap. Exactness of the test does not survive inexactness of the set it is applied to. K1's cohort and persistence figures carry the same dependency for the same reason; they are not re-marked below only because the marking task was scoped to K4 and K6.

---

## The rule, as documented

> *"The criteria of 'churn' is no new valid service subscription within 30 days after the current membership expires."* — Doc

> *"The training and the test data are selected from users whose membership expire within a certain month."* — Doc

The labeller implements this as: take each user's membership expiry standing at a cutoff; keep the user if that expiry falls inside the window month; then look forward for a renewal. No forward transaction at all ⇒ churn. First non-cancelling transaction less than 30 days after expiry ⇒ not churned. 30 days or more ⇒ churned. (Labeller, `predictionCandidates` / `calculateRenewalGap`.)

---

## K1 · The gate question

**Can a user enter a state in which they can never be labelled churned within the observation window, while remaining in the denominator of the reported churn rate?**

**What the rule says.** Cohort membership is decided by *where the expiry falls*, not by the user's outcome. A user whose standing expiry lies outside the window month is never selected, so the question of labelling them does not arise (Doc: *"we will not make a prediction for the user"*, in the third worked example). Every user who *is* selected receives a label, and the churn condition remains satisfiable for all of them: a user is labelled churned by the absence of a renewal, which no prior state forecloses.

**What the data shows (original release).** Of 2,330,992 users with any transaction at or before the `20170131` cutoff, 881,535 (37.82%) carry a standing expiry inside the February window and 1,449,457 (62.18%) do not. Of that out-of-window group, **1,340,100 — 92.46% — do not appear in `train.csv` at all.** They are absent from the denominator rather than sitting in it as successes. (Script `03_cohort_rule.py`.)

**Persistence, tested against transactions rather than listening logs.** Among the reconstructed and labelled cohort of 881,477: users labelled `is_churn=0` number 830,801, of whom **794,941 (95.68%) transact again** after the cutoff; users labelled `is_churn=1` number 50,676, of whom 19,642 (38.76%) do. Continued transacting is widespread, so the cohort is not made up of terminated units — but it is being recorded, not suppressed. (Script `03_cohort_rule.py`.)

**Do rule and data agree?** Yes. Both describe a population that **leaves the denominator** when its expiry falls outside the window, rather than one that stays in and is counted as a success.

**Could not be determined.** Whether any user is *structurally* barred from a churn label in a window they are selected into cannot be settled from the original release, because none of its own labels can be verified against its own transactions — see K6 and Observation 2.

---

## K2 · The cancellation clause

**A user who has actively cancelled but whose membership has not yet expired — are they counted as retained, and for how long?**

**What the rule says.** Cancellation is explicitly not churn: *"Note that the is_cancel field indicates whether a user actively cancels a subscription. Subscription cancellation does not imply the user has churned."* (Doc.) The clause the frozen plan records — churn holds *"even if the user decides to cancel"* — is implemented by cancellation altering the expiry date rather than the label: Doc's second worked example moves an expiry *"from 2017-04-03 back to 2017-03-16 due to the user making an active cancellation."* The user is then judged by the same 30-day test against the revised expiry.

**What the data shows (original release).** `transactions.csv` carries 856,851 rows with `is_cancel=1`, from 768,456 distinct users — **32.51% of all users in the file have cancelled at least once.** Of those cancel rows:

| Gap from the cancel transaction to the expiry it records | Rows | Share |
|---|---|---|
| negative — expiry moved before the cancel transaction | 147,200 | 17.18% |
| same day | 455,685 | 53.18% |
| 1–7 days | 118,386 | 13.82% |
| 8–30 days | 96,703 | 11.29% |
| 31–90 days | 31,857 | 3.72% |
| over 90 days | 7,020 | 0.82% |

**29.64% of cancellations leave membership running past the cancellation date.** So the answer to "for how long" is: usually not at all (53.18% terminate the same day), but in nearly three cases in ten the user remains a paying-through member, and in 4.54% for more than a month.

Within the cohort, 3,600 users have a cancellation as their last pre-cutoff state. Their churn rate is **57.64%**, against **5.54%** for the 877,877 whose last state is active. Their remaining membership runs 1–7 days for 8.33%, 8–30 days for 58.08%, and 31 days or more for 33.58%. (Script `04_cancellation.py`.)

**Do rule and data agree?** Yes. Cancelled-not-yet-expired users are carried as retained until their revised expiry, and are then tested normally. Being cancelled raises the churn rate roughly tenfold rather than suppressing it.

---

## K3 · Absorbing or delayed?

**Is that state absorbing (never subsequently labelled churned) or merely delayed (labelled in a later window)?**

**⚠️ Judgement call, flagged.** Answering this requires comparing cohorts across the two pinned releases. What follows compares **label-file membership and labels only**; no behavioural quantity and no label is computed for one release from another release's transactions, which is what boundary 6 forbids. The comparison is what R1′ was adopted to make possible. It is separated here so it can be discounted if you read the boundary more strictly.

**What the data shows.** The `_v2` labelled cohort **is** the original release's test cohort, exactly: 970,960 users in each, intersection 970,960, **100.00%, with zero users on either side only** (Script `02_release_shape.py`). Successive windows are therefore directly comparable.

Of the 992,931 users labelled in the February window, **881,701 (88.80%) are labelled again in the March window.**

| February → March | Users | Share of those labelled in both |
|---|---|---|
| 0 → 0 | 824,659 | 93.53% |
| 0 → 1 | 40,721 | 4.62% |
| 1 → 0 | 5,269 | 0.60% |
| 1 → 1 | 11,052 | 1.25% |

Of the 929,460 users labelled **not churned** in February, 865,380 (93.11%) are re-labelled in March, and **40,721 of those — 4.71% — are labelled churned there.** Of the 64,080 not re-labelled, 42,561 appear in the April test cohort.

Of the 63,471 labelled **churned** in February, only 16,321 (25.71%) are labelled again in March — consistent with a churned user having no membership expiring in the next window — and 5,269 of them return to `is_churn=0`.

**Do rule and data agree?** Yes, and in the same direction. **The state is not absorbing.** A user recorded as not-churned is re-examined in the following window and can be recorded as churned there; a user recorded as churned can revert. Nothing in the observed transitions is one-directional.

**Could not be determined.** Whether the 6.89% of February non-churned users who are *not* re-labelled in March are absent because they were excluded by the window rule or for some other reason cannot be settled without reconstructing the March cohort, which the `_v2` release cannot do in-release (K6, and Observation 3).

---

## K4 · Out-of-window expirations

**How are users whose membership expires outside the labelling window treated — excluded, or retained in the denominator as non-churned?**

**What the rule says.** Excluded, explicitly. Doc's third worked example ends: *"not between 2017-03-01 and 2017-03-31, so we will not make a prediction for the user."* The labeller enforces it as a filter on candidacy, not as a label (`predictionCandidates`, `last_expire` between the window bounds).

**What the data shows (original release).** Of the 1,449,457 **[R]** users whose standing expiry at the cutoff falls outside the February window:

- **1,340,100 (92.46%) are absent from `train.csv`** **[R]** — outside the denominator entirely;
- 109,357 (7.54%) **[R]** do appear in it, of whom 12,132 (11.09%) **[R]** are labelled churned.

The out-of-window group splits 91.14% **[R]** expiring **before** the window and 8.86% **[R]** **after** it. (Script `03_cohort_rule.py`.)

**Dependency note for this answer.** Every figure above is **[R]**. The membership test against `train.csv` is exact, but *which users are tested* is decided by reconstructed expiry, so the gap propagates to all three columns. Two supporting figures are firmer: **2,330,992 [E†]** users have at least one transaction at or before the cutoff — a distinct-`msno` count needing no ordering rule, exact given the cutoff date — and **992,931 [E]** is the `train.csv` denominator, read straight from the file. **The direction of the K4 answer does not rest on the reconstruction**: the documentation states exclusion outright (*"we will not make a prediction for the user"*), and the reconstruction agrees with it. **The magnitudes do rest on it.**

**Do rule and data agree?** Yes, on the dominant behaviour: out-of-window expiry means exclusion from the denominator. **This is the answer to the C1 gate for this instrument: the unit leaves the denominator.**

**Could not be determined.** The 7.54% residue is not resolved. It is most likely an artefact of the reconstruction rather than of the rule — see Judgement call 2 and Observation 4 — but the material distributed does not allow the two to be separated, so the residue is reported rather than explained away.

> **Annotation added 27 Aug, after a confirmatory intersection with its interpretation pre-committed (`DEVIATIONS.md` D-5). Script `07_residue_containment.py`. The answer above is not restated; this qualifies its residue.**
>
> **The 109,357 residue lies entirely inside the 111,454-user reconstruction miss — 109,357 of 109,357, 100.0000%.** The reverse containment is 98.1185%, the 2,097 remainder being exactly the labelled users with no pre-cutoff transaction. **No part of the residue falls outside the reconstruction miss**, so there is no separately-countable in-denominator out-of-window population to report against the 992,931 denominator.
>
> **⚠️ That containment is an identity, not evidence.** The residue is defined as *labelled and reconstructed-expiry-outside-window*; the miss is defined as *labelled and not reconstructed into the cohort*, which is the same predicate plus the no-history case. **The one set is a subset of the other by construction and the test could not have come out otherwise.** It is recorded because it was run and pre-committed, not because it discriminates.
>
> **What does discriminate is the before/after split, which was not predetermined.** The residue is **82.87% after-window** against **8.86%** in the overall out-of-window population — a **9.36× enrichment [R]**. Expiries standing *after* the window at the cutoff are precisely those a later revision could pull back into it. **This is independent support for reading the residue as reconstruction error rather than as an in-denominator out-of-window population** — and unlike the containment check, it could have come out the other way.
>
> **Consequence, stated without assigning a branch:** the residue **should not be treated as independent evidence bearing on §6 condition (a)**. That conclusion rests on the enrichment, not on the containment.

---

## K5 · The metric and the decision

**Which reported metric carries the denominator, and what decision would it drive in a live subscription business?**

**What the rule says.** The metric is the churn rate over the labelled cohort: `is_churn` is *"the target variable"*, `is_churn = 1 means churn, is_churn = 0 means renewal` (Doc). The denominator is the set of users selected into the window — those *"whose membership expire within a certain month."*

**What the data shows.**

| Release | Denominator | `is_churn=1` | Churn rate |
|---|---|---|---|
| Original (Feb 2017) | 992,931 | 63,471 | **6.392%** |
| `_v2` (Mar 2017) | 970,960 | 87,330 | **8.994%** |

(Scripts `01_structure.py`, `05_v2_and_k3.py`.)

**What it would drive.** A monthly subscriber churn rate on this construction is the input to retention forecasting, lifetime-value estimation and the retention-spend decision — how much may be spent to save a subscriber, and on whom. The plan's reserve-equivalent framing applies: in a live subscription business this number gates the deferred-revenue and retention-cost assumptions carried in the plan.

**Do rule and data agree?** Yes. The metric is exactly the mean of the label over the selected cohort, and both releases compute cleanly.

**Flagged, not resolved.** The two releases differ by 2.6 percentage points on adjacent months — a 41% relative difference. Nothing in the pinned material establishes whether that is seasonality, a change in cohort composition, or a difference in how the two label sets were produced.

---

## K6 · The window edge

**A user whose membership expires fewer than 30 days before the observation window closes cannot satisfy the churn condition — there aren't 30 days left in which to fail it — yet plausibly remains in the denominator, counted as retained.**

> The frozen plan's own constraint applies here: this may resolve to censoring rather than absorption, and must not be forced into POSITIVE. It is answered separately per release, per R1′.

### Original release — the structural precondition is present in the distributed file, but not in the labelling

**What the rule requires.** 30 days of observed non-renewal after expiry.

**What the release contains.** `transactions.csv` ends at `transaction_date = 20170228` **[E]**. The last February expiry with a full 30 days of subsequent observation inside this file would be `20170129` **[E]** — *before the window opens*. So **0 of the 881,477 [R] reconstructed cohort users have their 30-day test fully observable inside this release's own transactions file** (Script `03_cohort_rule.py`).

> **The zero here is [E], not [R].** No February expiry can carry 30 days of observation inside a file ending `20170228`, whatever the cohort turns out to be — it is arithmetic on the file's own date range. **Only the 881,477 denominator is reconstruction-dependent.** This is the one place in K6 where the reconstruction gap cannot touch the conclusion.

**But the labels do not come from that file.** The Doc states: *"On our cluster, the log history starts from 2015-01-01 to 2017-03-31."* A February expiry plus 30 days runs to 30 March at the latest, which that cluster window covers. **So for this release the labeller had the data the rule requires, even though the distributed transactions file does not.** The truncation is in what was published, not in what was labelled.

**What the data shows across the window.** Churn rate by expiry day is flat at roughly 6% across days 1–27, with no gradient as the observable-days column falls from 27 to 1:

| Observation available inside the file | Users | Churn rate | Auto-renew | |
|---|---|---|---|---|
| 15–29 days | 369,816 | 6.29% | 86.09% | **[R]** |
| 1–14 days | 392,417 | 6.17% | 86.91% | **[R]** |
| 0 days (expiry on the file's last date) | 119,244 | **2.67%** | **97.01%** | **[R]** |

**Every cell in that table is [R]** — the rows are groupings by reconstructed expiry, and the auto-renew column is read off the reconstruction-selected transaction, so it is dependent twice over.

The single anomaly is the window-close day itself. Expiry on `20170228` accounts for 119,244 **[R]** users — **13.53% [R] of the reconstructed cohort, 12.01% [R] of the 992,931-user [E] `train.csv` denominator**, above the plan's 5% materiality threshold — and carries a churn rate of 2.67% **[R]** against 6.23% **[R]** for the rest of the window.

> **What this means for the materiality call.** The 12.01% clears the 5% threshold with room, but it is **[R]** on both the numerator and the grouping, against a rule that reproduces at 88.78%. **A materiality judgement resting on it is resting on the reconstruction.** The flat gradient across days 1–27 that argues against an edge effect is likewise **[R]**.

**⚠️ The confound was tested before the correspondence was reported, and it does not survive intact.** Those same window-close users are **97.01% auto-renewing [R]**, against 86.51% **[R]** for the rest of the cohort, and 0.06% **[R]** cancelled against 0.46% **[R]**. Month-end expiry is heavily concentrated *and* heavily auto-renewing. A lower churn rate in a group that is ten points more auto-renewing has a mundane explanation available, and the flatness of the gradient across days 1–27 — where observability varies from 27 days to 1 and the churn rate does not move — argues against reading the day-28 drop as an observability effect. **The data does not support an edge effect in this release.** (Script `06_window_edge.py`.)

### `_v2` release — cannot be determined in-release, and this is where the precondition actually bites

**Why it bites here.** The `_v2` window is March 2017 expiries. A `20170331` expiry plus 30 days runs to `20170430` **[E]** — **beyond the `2017-03-31` end of the log history the Doc states KKBox itself used.** Of the 31 expiry days in the window, only `20170301` **[E]** has a full 30 days available within that stated history.

**Why it cannot be checked here.** `transactions_v2.csv` holds 1,431,009 **[E]** rows, of which 74.76% **[E]** fall in March 2017 and only 361,187 (25.24%) **[E]** predate the window at all. **Of the 970,960 [E] labelled users, 878,274 — 90.45% [E†] — have no pre-window transaction anywhere in this release's own transactions file.** Their cohort-entry expiry cannot be established, so the expiry-day distribution that K6 requires cannot be built. (Script `05_v2_and_k3.py`.)

> **The `_v2` answer is the firmest in this document.** Every figure supporting it is **[E]** or **[E†]** — row counts, date-range arithmetic and a set-membership test asking only whether a user has *any* transaction at or before `20170228`. **No cohort reconstruction is involved, because the point is precisely that none is possible.** The 90.45% is marked **[E†]** only because it is conditioned on the cutoff date; the ordering rule that carries the 11.22% gap plays no part.

**The answer is therefore: cannot be determined from the pinned release, because the `_v2` transactions file does not contain the pre-window history that cohort entry depends on, for 90.45% of the labelled cohort.**

**⚠️ Stopped and flagged rather than reached for.** The February transactions that set most March expiries do exist — in `transactions.csv`, in the *other* release. Using them would answer this question. **Boundary 6 forbids it and I did not do it.** This is reported as a blocked answer rather than closed by mixing variants.

---

## Counts against the named denominator

The plan fixes materiality at 5% of labelled users in the observation window. That denominator is `train.csv` (992,931) and `train_v2.csv` (970,960) respectively.

| State | Users | Denominator | Share | Dependency |
|---|---|---|---|---|
| Out-of-window expiry, absent from the denominator (original) | 1,340,100 | — outside the metric entirely | n/a | **[R]** |
| Out-of-window expiry, present in the denominator (original) | 109,357 | 992,931 | 11.01% | **[R]** — 100.00% contained in the reconstruction miss; see D-5 |
| Expiry on the window-close date (original) | 119,244 | 992,931 | **12.01%** | **[R]** |
| Cohort users whose last pre-cutoff state is a cancellation (original) | 3,600 | 992,931 | 0.36% | **[R]** |
| February non-churned users re-labelled churned in March | 40,721 | 992,931 | 4.10% | **[E]** |
| `_v2` cohort whose entry expiry is unreconstructible in-release | 878,274 | 970,960 | **90.45%** | **[E†]** |

**Read the dependency column before the share column.** The four **[R]** rows are grouped by reconstructed expiry and carry the 11.22% gap. **Row 2 is now further qualified**: its 109,357 users lie entirely within the reconstruction miss (D-5), so the row records a property of the reconstruction rather than a population of the instrument, and **no in-denominator out-of-window count survives to be reported against the 992,931 denominator.** The two that do not — the February-to-March re-labelling, which is a set operation on two label files, and the `_v2` unreconstructibility, which asks only whether a transaction exists — are the two firmest counts in this document. **The only figure here that clears the 5% materiality threshold on [E]-grade evidence is the 90.45%, and what it establishes is that a question cannot be answered.**

**Not established:** any count of users structurally unable to receive a churn label while remaining in the denominator. No such state was identified in the original release, and in the `_v2` release the question is undeterminable for the reason given under K6.

---

## OBSERVATIONS (not findings)

Outside K1–K6. Reported separately per boundary 1, and not folded into any answer.

**1 · `train_v2.csv` is the original release's test cohort, relabelled — exactly.** 970,960 users each, intersection 970,960, zero on either side only. This resolves, from the data, the month-semantics ambiguity recorded at pinning: `train_v2` covers **March 2017 expirations** — reading (i) — not February churn behaviour. The documentation alone could not settle it; the cohort identity does.

**2 · A release's behavioural file ends at the start of its own label window.** *(Recorded as an observation at David's instruction, 27 Aug, as it falls outside K1–K6.)* `transactions.csv` ends `20170228`; the February expiries it is meant to explain need observation through 30 March. So **not one of the 992,931 labels in `train.csv` can be verified against the transactions file distributed alongside it.** The same holds for `_v2`: transactions end `20170331`, and its March expiries need April. This is a fact about the instrument as published, not about the labelling — KKBox's own stated log history covers the February case. A downstream user reproducing the label rule from the distributed files alone cannot check either release's labels.

**3 · `transactions_v2.csv` is not a cumulative file.** 74.76% of its rows fall in March 2017, 9.01% in February, and the remaining 16% thin out back to January 2015 — 1,431,009 rows against 21,547,746 in the original. This resolves ambiguity #2 as recorded in `EXECUTION-LOG.md`: it is **substantially incremental**, and it does not carry the history a user's cohort entry depends on. The size-ratio observation logged at pinning (≈14.5× and ≈10.4×) pointed here; it is now measured rather than inferred.

**4 · The cohort rule cannot be reproduced exactly from the distributed material.** The best reconstruction matches 881,477 of 992,931 labelled users — **88.78%**. Of the 111,454 misses, 81.31% have a standing expiry *after* the window under the reconstruction, 16.81% before it, and 1.88% have no transaction before the cutoff at all. Their churn rate is 11.48% against 6.39% overall. The Doc states the labeller's *"date values in the script is modified so it is easier to run on personal laptops"*, so the distributed script is explicitly not the production configuration. The residual is consistent with post-cutoff cancellations pulling expiries back into the window — but that is a hypothesis the distributed material cannot test, and it is not asserted here.

**5 · `membership_expire_date` carries sentinel and out-of-range values.** `transactions.csv` spans `19700101`–`20170331`; `transactions_v2.csv` spans `20160419`–`20361015`. Epoch-zero and year-2036 values are present. No K-question turns on them and no cleaning was applied; recorded because a reader reproducing these counts will meet them.

---

## Judgement calls

Flagged per item 5 of the brief, rather than buried in an answer.

**1 · Cross-release comparison for K3.** K3 asks whether a state is absorbing or delayed, which is a question about *later windows*. Answering it inside one release is not possible. I compared label-file membership and labels across releases, and computed nothing behavioural across variants. I read boundary 6 as prohibiting the derivation of one release's quantities from another's files, not the comparison of two pinned releases' outputs — which is what R1′ exists to permit. **If you read it more strictly, K3 becomes "cannot be determined in-release" for both releases**, and the counts in that section should be discounted.

**2 · Which history window reconstructs the cohort.** The distributed labeller filters history to `transaction_date >= 20170101`, but the Doc says its dates were modified for laptop use. I ran both readings and reported both: the literal script matches 86.26% of the labelled cohort, all-history-to-cutoff matches 88.78%. Downstream counts use the better-matching reading. Neither reproduces the cohort exactly, and every reconstruction-dependent count in K4 and K6 inherits that 11.22% gap.

**3 · Treating "days observable inside the file" as the K6 exposure variable.** For the original release I measured the edge against the distributed file's horizon, because that is what the pinned release contains. Measured against KKBox's stated cluster history instead, the February window has no edge exposure at all. Both are stated under K6; the second is why I do not report an edge effect for this release.

**4 · Not fetching `user_logs*`.** Agreed in scoping. Persistence was tested against transactions instead, on the reasoning that the pathology concerns subscription state. No K-answer turned out to hinge on listening behaviour, so the exclusion was never load-bearing.

---

## Hours

| Task | Hours |
|---|---|
| Scoping: read brief and plan, map K1–K6 to files, set up ignore rules and volume | 0.25 |
| Download, byte-verification against the pinned manifest, extraction | 0.10 |
| Script 01–02: structure, release shape, cohort set relations | 0.20 |
| Script 03–04: cohort-rule reconstruction, both readings, K2 and diagnostics | 0.35 |
| Script 05–06: `_v2` in-release assessment, K3, window edge and confound test | 0.30 |
| Writing this document | 0.25 |
| **Total** | **1.45** |

Wall-clock from first download to last script: 26 minutes. Total machine time across all six scripts: under 4 minutes on one laptop core, no dependencies beyond the Python standard library.

---

*Answers only. No branch assigned — that is made separately, under §6 of the frozen plan, and published with its reasoning.*
