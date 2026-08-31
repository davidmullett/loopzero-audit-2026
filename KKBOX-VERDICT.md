# KKBox — branch assignment under §6

**Instrument:** KKBOX / **WSDM Cup 2018** churn dataset *(corrected 28 Aug 2026 from "2017" — the data covers 2017, the Cup ran at WSDM 2018)*
**Releases pinned:** original + `_v2` (R1′, `EXECUTION-LOG.md`)
**Frozen plan:** `b15f472e…` · frozen `2026-08-24T15:33:01Z` · registered `osf.io/ksm3n` · DOI `10.17605/OSF.IO/KSM3N`
**Answers:** `KKBOX-ANSWERS.md` · **Deviations:** D-2, D-3, D-4, D-5
**Assigned by:** David Mullett · 2026-08-27

---

## BRANCH: NEGATIVE — exclusion

**The unevaluable unit is removed from the denominator. This is not the paper's mechanism.**

Censoring — the predicted branch — was tested for under K6 and not found in the release where it could be tested; it is undetermined in the other.

---

## Disclosure

**What was done by whom, stated because the alternative is a credential claim.**

- The read that produced `KKBOX-ANSWERS.md` was executed by an AI coding agent against a pre-registered brief, under boundaries fixed before the read.
- **The evidence summary and the rule-application analysis in this document were prepared with AI assistance.** Each condition was mapped to the evidence bearing on it, with evidence grades, by an AI model instance.
- **The author made the two determinations that the frozen text does not settle** — whether to assign or return INDETERMINATE, and whether the mechanism is exclusion or censoring — and verified each condition against §3 and §6 before accepting it.

**This is not expert review, not peer review, and confers no warrant.** It follows the standard set in §11 of the frozen plan and guard G-3.

> **One disclosure that bears directly on how much weight to give the AI-assisted analysis.** During this assignment the AI instance specified a confirmatory set-intersection test that was **structurally incapable of failing** — the two sets stood in a subset relation by construction — and presented it as a two-branch pre-commitment. The executing agent identified the degeneracy and refused to bank the result. **The substantive conclusion was recovered from a different, non-degenerate measurement** (the after-window enrichment). Recorded as D-5. A reader weighing this document should know that the assistance produced an invalid instrument inside an audit of invalid instruments, and that it was caught by a second check rather than by the party that designed it.

---

## Preliminary ruling — which sense of "cannot be evaluated" §6 governs

Two senses appear in the answers:

- **Sense 1 — unevaluable by the labelling rule.** The rule cannot record a failure for this unit.
- **Sense 2 — unverifiable by a downstream reader from the distributed files.** The labeller could evaluate; a reader reproducing from what was shipped cannot.

**Ruling: Sense 1 governs §6 (a)–(c).**

§3 of the frozen plan uses that sense throughout and uses no other: *"**recorded** as a failure only if a failure condition holds AND an eligibility condition holds"* · *"can never again be **recorded** as a failure"* · *"persist and keep accruing real bad outcomes while being **structurally unrecordable**"* · *"generating genuine harm **the rule could never see**."* Nothing in §3 concerns what a downstream reader can verify.

**Consequence.** The 90.45% **[E†]** `_v2` unreconstructibility figure — the firmest number in the answers — is a **Sense 2** finding. It bears on the instrument *as published*, not on whether the pathology is present, and belongs with Observation 2. **It is not evidence for or against any of the three conditions.**

---

## Condition (a) — does the unevaluable unit remain in the denominator of a named reported metric?

**Evidence for.** The K4 residue — 109,357 users with out-of-window expiry appearing in `train.csv`, 11.01% of the 992,931 denominator — was the only candidate. **D-5 removed it.** The residue is wholly contained in the reconstruction-miss set, with after-window expiries enriched 9.36× (82.87% against 8.86% in the overall out-of-window population), consistent with post-cutoff transactions revising expiry into the window. It records a property of the reconstruction, not a population of the instrument. **No other evidence for (a) appears anywhere in the answers.**

**Evidence against.**
- **92.46% [R]** of out-of-window users (1,340,100 of 1,449,457) are absent from `train.csv` entirely.
- Documentation states exclusion outright: *"not between 2017-03-01 and 2017-03-31, so we will not make a prediction for the user."* The labeller enforces it as a candidacy filter (`predictionCandidates`), not as a label.
- K1 identified no state in which a selected user is barred from a churn label.

**Holds? NO.**

The out-of-window unit does not remain in the denominator; it is absent from it. **This conclusion does not rest on the reconstruction** — the documentation states exclusion and the reconstruction agrees with it. The one figure that pointed the other way has been shown to be an artefact of the measuring instrument rather than a feature of the instrument being measured.

---

## Condition (b) — is it counted as a success there?

**Evidence.** None independent of (a). The only candidate group was the K4 residue, attributed to reconstruction error under D-5.

**Holds? NO.**

**(b) is not capable of holding where (a) fails.** It asks what a unit is counted as *in the denominator*; a unit absent from the denominator is not counted as anything there. There is no separate population for which (b) could be independently assessed.

---

## Condition (c) — can it continue accruing real failures the rule cannot record?

**Evidence that units persist.** **95.68% [R]** of the 830,801 not-churned cohort users transact again after the cutoff. The cohort is emphatically not made of terminated units — §3's warning that *"termination is not absorption"* does not apply here.

**Evidence that failures are recordable.** **[E]** — of 929,460 February non-churned users, 93.11% are re-labelled in the March window and **4.71% of those are labelled churned there**. 5,269 users revert 1 → 0. Nothing in the observed transitions is one-directional.

**Holds? NO.**

§6 (c) requires failures the rule **cannot record**, not merely a unit that persists. Persistence is present; unrecordability is not. A user recorded as not-churned is re-examined in the following window and can be recorded as churned there.

**Note the grade asymmetry, which favours this conclusion rather than undercutting it:** the evidence bearing against (c) is **[E]** — a set operation on two label files, no reconstruction involved. The evidence bearing for (c) is **[R]** and speaks to activity rather than to recordability.

---

## Result of the three conditions

§6: **POSITIVE requires all three.** All three fail. **POSITIVE is out**, in both its material and present-but-rare forms.

**MISSCORING is out.** It requires (a) and (b) to hold with only (c) failing — the unit stays in the denominator, is counted as a success, but cannot keep accruing failures. Here (a) and (b) fail, so the structure MISSCORING describes is not present.

**This leaves the NEGATIVE family.**

---

## Which branch, and why not the others

**Chosen: NEGATIVE — exclusion.** The unevaluable unit is removed from the denominator.

**Ruled out:**

- **POSITIVE-MATERIAL / POSITIVE-PRESENT-BUT-RARE** — all three conditions fail; the prevalence split is never reached.
- **MISSCORING** — requires (a) and (b) to hold. Both fail.
- **NEGATIVE — correctly handled** — would require the unevaluable unit to be scored as a failure. It is not scored at all; it is not selected.
- **NEGATIVE — censoring, not absorption** — see Hard call 2. Tested for under K6 and not found where it could be tested.
- **INDETERMINATE** — see Hard call 1. §6's triggers are not met.

---

## Prevalence

**Named denominator, fixed in §6:** 5% of labelled users in the observation window — `train.csv` (992,931), `train_v2.csv` (970,960).

**Prevalence is reported here, not determining.** The 5% threshold splits POSITIVE only. The branch was determined by the failure of conditions (a)–(c), and no prevalence figure was used to reach it.

| Figure | Users | Share | Grade |
|---|---|---|---|
| Expiry on the window-close date (original) | 119,244 | 12.01% | **[R]** |
| February non-churned re-labelled churned in March | 40,721 | 4.10% | **[E]** |
| `_v2` cohort whose entry expiry is unreconstructible in-release | 878,274 | 90.45% | **[E†]** |

**The only figure clearing 5% on [E]-grade evidence is the 90.45%, and what it establishes is that a question cannot be answered.** Under the preliminary ruling above it is a Sense 2 finding and bears on none of the conditions.

**No count of units structurally unable to receive a label while remaining in the denominator was established, because no such population was identified.**

---

## Hard call 1 — two releases, two K6 answers

**Determination: assign the branch. Record K6-on-`_v2` as indeterminate at the sub-question level.**

**Reasoning.** §6 reserves INDETERMINATE for results that are *"configuration-dependent, undocumented, or version-variable beyond resolution."* The `_v2` block is none of the three. Nothing varies by configuration; the rule is documented; and the two releases did not disagree about the rule — one shipped the pre-window history the question needs and the other did not. That is data completeness, not instrument ambiguity.

**The load-bearing point: none of the three conditions rests on K6.** (a) fails on documentation, K1 and K4. (b) has no independent evidence. (c) fails on K3's **[E]**-graded re-labelling. K6 is the question most likely to *find* the pathology, which makes it decisive for whether POSITIVE would have been reached and for prevalence within it — but it is not what determines whether the conditions hold. A blocked K6 cannot change a branch settled by conditions that do not depend on it.

**Against this, at its strongest:** K6 is named in the frozen plan as *"the most likely positive."* Assigning while it is unanswered on half the pinned material could be read as assigning on the convenient half, and §6 warns against reporting the most interesting branch as the finding.

**Why that objection does not hold here: the incentive runs the other way.** A POSITIVE would be considerably more useful to the author, commercially and reputationally, than a NEGATIVE. The branch assigned is the inconvenient one, with the blocked question reported prominently rather than buried.

**Recorded as indeterminate at the sub-question level:** K6 on the `_v2` release is **blocked, not negative**. 90.45% **[E†]** of that cohort cannot have their entry expiry established from the release's own files. This is where the pathology was most likely to appear, and it was not testable there.

---

## Hard call 2 — exclusion, not censoring

**Determination: exclusion.**

**Reasoning — the two branches describe two different populations, and the evidence separates them.**

**Censoring**, as §6 defines it, is a unit that is *in* the denominator, counted as a success, whose failure is unobservable inside the window. That is precisely K6's premise: a user whose expiry falls near the window close, selected into the cohort, unable to accrue the 30 days the churn condition requires.

**K6 tested for that and did not find it** in the release where it could be tested. Churn is flat at roughly 6% across expiry days 1–27 while observability falls from 27 days to 1. The single anomaly — day 28, 2.67% against 6.23% — did not survive the confound test: those users are 97.01% **[R]** auto-renewing against 86.51% **[R]** for the rest. And KKBox's stated cluster history runs to 2017-03-31, covering February expiries plus 30 days, so the labeller had the data the rule requires; the truncation is in what was published, not in what was labelled.

**Exclusion** is a unit removed from the denominator. That is K4: 92.46% **[R]** of out-of-window users absent from `train.csv`, documentation stating it outright, labeller enforcing it as a candidacy filter.

**Against this, at its strongest:** from the instrument's own perspective, out-of-window users are not excluded from a study population — they belong to a different monthly slice, and their event will be observed in the month it falls due. On that reading, "removed from the denominator" is a bookkeeping description and "would be labelled in a later window" is what actually happens to them.

**Why that reading is not adopted.** The hazard censoring names is that a reported metric **understates failures because some go unobserved inside its own denominator**. Out-of-window users do not understate February's churn rate; they were never in it. Whether their absence biases that rate is a *selection* question, and §6 has a branch for selection: exclusion.

> **⚠️ The incentive on this call, stated because it is real.** **Censoring was the predicted branch**, recorded in §2 before the read: *"I expect KKBox in particular may turn out to be window censoring rather than absorption."* Choosing exclusion makes that recorded prediction **wrong on mechanism**. The pull ran toward censoring and it was resisted on the reading above. A reader should weigh this call knowing which answer would have flattered the author.

---

## What could not be determined

- **K6 on the `_v2` release — blocked, not negative.** 90.45% **[E†]** of the labelled cohort have no pre-window transaction in that release's own transactions file, so cohort-entry expiry cannot be established and the expiry-day distribution K6 requires cannot be built. The February transactions that would answer it exist in the *other* release; **boundary 6 forbids reaching for them and they were not used.**
- Whether the 6.89% of February non-churned users not re-labelled in March are absent by operation of the window rule or otherwise.
- The mechanism behind the 11.22% reconstruction gap. The cancellation hypothesis is supported by the after-window enrichment but not uniquely identified — any post-cutoff expiry revision predicts the same pattern. **Both are reconstruction error, so the D-5 conclusion holds under either.**

---

## Hard call 2's companion: what the reconstruction gap reaches

**It does not reach the branch.** Following D-5, condition (a) rests on documentation the reconstruction agrees with rather than on the reconstruction itself. Condition (c) fails on **[E]**-graded evidence. The K6 zero is **[E]** — no February expiry can carry 30 days inside a file ending `20170228`, whatever the cohort turns out to be.

**It does reach every magnitude in K4 and K6**, including the 12.01% **[R]** day-28 figure that clears materiality *and* the flat gradient used to argue against an edge effect. Both sides of the K6 original-release argument rest on the same 88.78% model. **Any statement about the scale of anything in this instrument carries that gap; the branch does not.**

---

## Calibration against the declared expectation

On record in §2 before the read: *"I expect both to come back negative, and I expect KKBox in particular may turn out to be window censoring rather than absorption."*

**Partly right, and the wrong half is the informative one.**

**Right:** the direction. NEGATIVE, as predicted, against a stated base rate of three prior gate checks that also failed.

**Wrong:** the mechanism. The prediction named censoring; the finding is exclusion. And this is not merely imprecision — **censoring was specifically tested for under K6 and found absent** in the release where it could be tested. The predicted mechanism was not just different from the observed one; it was examined and ruled out.

**Why this is recorded before the write-up rather than after:** a prediction that names a mechanism and gets a different one is only partly right, and stating which half failed is the part that carries information about calibration. Recorded here so it cannot read as retrofitted.

---

## Strongest and weakest evidence in this assignment

**Strongest.** The February-to-March re-labelling: 40,721 users labelled not-churned in February and churned in March, 4.10% of the denominator, **[E]** — a set operation on two label files with no reconstruction involved. It bears directly on condition (c) and it is exact. Supported by the documentation's own worked example on exclusion, which is a primary-source statement of the rule rather than an inference from data.

**Weakest.** The K6 original-release no-edge-effect conclusion. Every cell of that table is **[R]**, including the auto-renew column, which is dependent twice over since the flag is read off the reconstruction-selected transaction. **Both the anomaly and the argument that dismissed it rest on the same 88.78% model.** The conclusion is stated in the answers with that caveat and it is repeated here: this is the softest-graded reasoning in the exercise, and it happens to be the reasoning that rules out the predicted branch.

---

## Hours

1.45 for the read (`EXECUTION-LOG.md`), plus the diagnostic under D-5. Wall-clock from first download to last script: 26 minutes. Machine time under 4 minutes on one laptop core, Python standard library only, no dependencies.

**The claim this supports:** a pre-specified validity check of this kind is cheap to run on a public instrument. Recorded plainly because §7 of the frozen plan requires it — without the number, the claim gets dropped rather than softened.

---

*Branch assigned under §6 of the frozen plan, applied as written and not adjusted to what was found. Answers in `KKBOX-ANSWERS.md`; deviations D-2 through D-5 in `DEVIATIONS.md`; analysis scripts in `scripts/`, runnable by anyone who has accepted the competition rules against their own copy of the data.*
