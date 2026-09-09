# Execution log — KKBox / τ-bench audit

**Mutable by design.** The frozen plan (`PRE-REGISTRATION.md`) contains no fields to fill in, so it verifies against its hash forever. Everything that accumulates during execution lives here.

**Frozen plan hash:** *(see `PRE-REGISTRATION.sha256` — the authoritative record)*

---

## Status

| | KKBox *(runs first)* | τ-bench |
|---|---|---|
| AI adversarial review completed, v3 *(two rounds — **not** expert or peer review; see §11 of the plan and D-1)* | ✅ 2026-08-24 | ✅ 2026-08-24 |
| Plan frozen | ✅ 2026-08-24 | ✅ 2026-08-24 |
| **Hash posted publicly (OSF)** | ✅ **2026-08-27 — archived, `osf.io/ksm3n`** | ✅ same registration |
| Dataset version / commit pinned | ✅ **2026-08-27 — R1′, both releases; manifest complete with per-file sizes** | ✅ **2026-08-27 — R2′, three commits (A/B/C)** |
| Read begun | ✅ **2026-08-27** — both pinned releases | ✅ **2026-08-27** — all three pins |
| Read complete | ✅ **2026-08-27** — answers in `KKBOX-ANSWERS.md` | ✅ **2026-08-27** — answers in `TAU-ANSWERS.md` |
| Hours logged | ✅ **1.45** (see Hours) | ✅ **2.10** (see Hours) |
| Branch assigned under §6 | ✅ **2026-08-27** — NEGATIVE, exclusion (`KKBOX-VERDICT.md`) | ✅ **2026-08-27** — four assignments (`TAU-VERDICT.md`) |
| Maintainer / publisher contacted | ☐ | ✅ **2026-08-28 — GitHub issue #497** |
| Response received (published verbatim) | ☐ | ☐ |
| Published | ☐ | ☐ |

**Gate: nothing is read until the hash is posted *and archiving is confirmed*.** That is the whole point of the hash.

### OSF registration

- **Type:** Open-Ended Registration · **Registered:** 24 Aug 2026 · **Public, no embargo**
- **Associated project:** https://osf.io/k75zw
- **✅ ARCHIVING COMPLETE — confirmed 27 Aug 2026. The registration timestamp is secured.**
- **Registration GUID:** **`ksm3n`** — https://osf.io/ksm3n/
- **DOI:** **`10.17605/OSF.IO/KSM3N`** — https://doi.org/10.17605/OSF.IO/KSM3N *(recorded 27 Aug 2026)*
- **🔓 THE HARD GATE IS LIFTED.** Nothing was read before this point. The anchor existed before the read, which is the entire purpose of the exercise.
- **The do-not-modify constraint is also lifted** — it applied only while archiving was in progress.
- **Contains:** `PRE-REGISTRATION.sha256` only. The plan itself is withheld until publication.

⚠️ **While archiving is in progress, do not modify any file in the OSF project or its components.** OSF's warning is explicit: changes during archiving cause archiving failure and **loss of the registration timestamp**. If it runs beyond 72 hours, email support@osf.io.

**Why the read waits for confirmation rather than starting now:** until archiving completes, the timestamp is not secured. Reading before it lands would mean the read began before the anchor existed — which is precisely the thing the anchor is there to rule out. The wait is likely minutes to hours; the cost of not waiting is the whole point of the exercise.

---

## Pinned versions

*(record exactly what was examined — recorded before the read, not after)*

**KKBox — to pin before the read:**

- **Source:** **WSDM Cup 2018** — KKBOX's Churn Prediction Challenge (Kaggle), public competition data release. *(Corrected 28 Aug 2026 from "WSDM Cup 2017". The data covers 2017; the Cup ran at WSDM 2018. The rules page quoted at §7.A below is titled "WSDM 2018 Cup Official Competition Rules", which was already in this file and contradicted this line.)*
- **⚠️ The release variant must be named explicitly.** The competition distributed more than one labelled set covering **different expiration months**, with `_v2` file variants issued later in the competition. **Which one is audited directly determines the K6 answer**, because K6 is about behaviour at the edge of the observation window — a different window is a different edge. Pin one, state it, and do not silently mix files across releases.
### ✅ PINNED — 2026-08-27. Selection rule **R1′: pin both releases.**

**Sourced from the competition's public data-description page only** (`kaggle.com/competitions/kkbox-churn-prediction-challenge/data`). That page is documentation, and its churn definition is already recorded as declared prior knowledge in §2 of the frozen plan. **No data files opened, nothing downloaded, no rules accepted, no forum posts or solution notebooks read.** The page is publicly readable; the sign-in gate applies to downloading, not to the description.

**The selection rule, stated before the variant was named.**

> **R1′ — pin both releases.** Audit the original release *and* the 6 Nov 2017 `_v2` refresh, answering K6 separately for each and reporting both. Within each release, never mix a labelled set with behavioural files from the other.

**Why R1′ rather than R1.** The single-release rule considered first (**R1: audit the latest release the competition itself issued**) is defensible on the documentation — the 6 Nov update is the competition's last word on which data it wants used, `members_v3.csv` is described as an explicit replacement, and a downstream user taking the page at face value lands on the `_v2` set. It was rejected in favour of R1′ for two reasons:

1. **⚠️ Disclosure, recorded because it is a researcher degree of freedom.** Under the `_v2` release the label window sits harder against the stated `2017-03-31` data horizon than the original release does — so **R1 alone would have selected the more K6-exposed release.** R1 was proposed on the stated principle and would have been proposed the same way had that not been noticed; it is logged rather than left to be discovered later. R1′ removes the question entirely, because nothing is selected away.
2. **R1′ also covers both readings of the month-semantics ambiguity below.** The ambiguity is about which expiration window `train_v2.csv` labels. Pinning both releases means both candidate windows are audited whichever reading is correct, so the ambiguity cannot silently decide the answer.

**R1′ fills a gap the frozen plan left; it does not depart from it.** The frozen plan does not specify a release variant, which is why the choice had to be made and stated. **The "pin one, state it" instruction is in the line above — in this mutable execution log, not in `PRE-REGISTRATION.md`** — so widening it to two is a change to this log's own working note, not to anything under the hash. §§3–6 are untouched. **Logged all the same as `D-2` in `DEVIATIONS.md`**, because a gap filled after the freeze is still a researcher degree of freedom, and the log's standard is to record it when noticed rather than once it turns out to matter.

**File manifest as pinned.** Filenames exactly as listed in the page's Data Explorer; all data files are distributed as `.7z` archives.

| Release | Files |
|---|---|
| **Original** | `train.csv.7z` · `sample_submission_zero.csv.7z` · `transactions.csv.7z` · `user_logs.csv.7z` |
| **`_v2` refresh (6 Nov 2017)** | `train_v2.csv.7z` · `sample_submission_v2.csv.7z` · `transactions_v2.csv.7z` · `user_logs_v2.csv.7z` |
| **Shared / cross-release** | `members_v3.csv.7z` *(refreshed 13 Nov 2017; the page says it "replaces members.csv data with the expiration date data removed," and `members.csv` is no longer distributed)* · `WSDMChurnLabeller.scala` *(7.05 kB)* |

**Sizes — CLOSED 27 Aug 2026. Per-file sizes in bytes, as reported by the source.**

**Competition rules accepted by David on 27 Aug 2026, under his own Kaggle account.** Accepting the rules is a terms action taken by David personally, not by any assisting system.

**Source of these figures:** `kaggle competitions files -c kkbox-churn-prediction-challenge`, **run by David under his accepted account.** All ten entries carry the listing date **2019-12-12**.

| File | Release | Bytes |
|---|---|---|
| `train.csv.7z` | original | 33,563,098 |
| `sample_submission_zero.csv.7z` | original | 32,828,332 |
| `transactions.csv.7z` | original | 707,508,779 |
| `user_logs.csv.7z` | original | 7,136,060,375 |
| `train_v2.csv.7z` | `_v2` | 32,818,991 |
| `sample_submission_v2.csv.7z` | `_v2` | 30,666,957 |
| `transactions_v2.csv.7z` | `_v2` | 48,850,410 |
| `user_logs_v2.csv.7z` | `_v2` | 685,951,221 |
| `members_v3.csv.7z` | shared | 242,308,558 |
| `WSDMChurnLabeller.scala` | shared | 7,050 |

**Reconciliation check, run rather than assumed:** the ten figures sum to **8,950,563,771 bytes = 8.95 GB**, which **matches the aggregate stated on the Data tab exactly** (10 files, 8.95 GB). The manifest is internally consistent with the page it came from.

**No checksums are published for this competition.** Recorded as an absence, not an omission.

**On the `2019-12-12` date:** that is the date the CLI listing itself reports against every file, uniformly. **It is a listing date, not a release date** — the documented release history is the one on the Data tab (`_v2` refresh 6 Nov 2017, `members_v3` 13 Nov 2017). Recorded as reported; **no inference drawn about what happened in 2019.**

> **Why the CLI and not the web page — worth keeping, because it cost a round trip.** **The web Data tab does not expose per-file sizes even when signed in with acceptance in force.** Verified 27 Aug by querying the rendered page for every size-formatted string in the DOM: the only two matches were the `8.95 GB` aggregate and `WSDMChurnLabeller.scala (7.05 kB)`. Acceptance unlocks downloading, not size metadata. **The CLI was the only route**, and it supplies sizes without transferring any archive.

**Label windows covered — AMBIGUOUS AS DOCUMENTED. Both readings recorded; they differ.**

- **Original release, unambiguous.** The page: the train data is "users whose subscription expires within the month of **February 2017**," the test data "users whose subscription expires within the month of **March 2017**" — i.e. "churn or renewal roughly in the month of March 2017 for train set, and … roughly in the month of April 2017."
- **`_v2` release, ambiguous.** The page describes `train_v2.csv` as containing "the churn data for **March, 2017**" and `sample_submission_v2.csv` as "the test data for **April, 2017**," and states: "As of November 6, 2017, we have refreshed the test data to predict user churn in the month of April, 2017." **It does not state whether the named month is the expiration month or the churn-observation month.** The original release's own wording puts those one month apart.
  - **Reading (i):** `train_v2` labels expirations in **March 2017**, shifting both sets one month later.
  - **Reading (ii):** `train_v2` labels churn *observed* in March 2017, i.e. expirations in **February 2017** — the same window as `train.csv`, relabelled.
  - **These differ, and they differ on the axis K6 turns on.** Not resolvable from the data-description page, and not inferred. Under R1′ both windows are in scope regardless of which reading holds.

**Two further ambiguities on the same page, recorded rather than resolved.**

1. **Cumulative or incremental.** `transactions_v2.csv` and `user_logs_v2.csv` are described as containing data "until 3/31/2017," which reads cumulative, but the page never states whether they carry the pre-March history or only the increment over the originals. Not resolvable without opening a file. Not done.

   > **Observation recorded 27 Aug 2026, from the manifest sizes. Deliberately not resolved.** The `_v2` behavioural files are roughly **an order of magnitude smaller than their originals** — `transactions_v2.csv.7z` **48,850,410 B** against `transactions.csv.7z` **707,508,779 B** (≈14.5×), and `user_logs_v2.csv.7z` **685,951,221 B** against `user_logs.csv.7z` **7,136,060,375 B** (≈10.4×). **This bears on the cumulative-versus-incremental question and is left open for the read to resolve against the files.** It is recorded here **so that if it surfaces during the read it has clean provenance and does not read as an undocumented inference.** No conclusion is drawn from it now, and a size ratio is not evidence of file contents.
2. **Which release the private leaderboard scored is not stated.** The page's only leaderboard sentence — "Train and test sets are split by transaction date, as well as the public and private leaderboard data" — predates the 6 Nov update. That final scoring used the refreshed April test set is *implied* by the refresh of the submission file, not stated. Moot under R1′.

---

### Scope ruling — `WSDMChurnLabeller.scala` is **IN SCOPE** for the read

**Ruled by David, 27 Aug 2026, before the read began.**

`PRE-REGISTRATION.md:35` declares the competition's label-generation code unexamined **in the past tense, as prior knowledge** — the same construction `:37` uses for τ-bench's evaluation code, which the audit plainly must read. A §2 declaration records what had not been examined at freezing; it is not a standing prohibition. **The script is the implementation of the rule under audit** — the page states it is "the code we used to generate the label for the test data set" — so excluding it would mean auditing a labelling rule while refusing to look at the labeller.

**Solution notebooks and forum posts remain out of scope**, as §2 has them, and nothing here widens that.

**Not deliberately opened.** ⚠️ **But its full source entered the assisting model's context on 27 Aug 2026, incidentally and before the read was authorised to begin** — Kaggle's Data tab auto-renders the selected file's contents inline, so the script's body arrived in the page text captured while checking the file list for sizes. No click, no download, and the file is in scope by the ruling above, so no boundary was crossed — **but the sequencing was not the clean one the plan assumes, and a later finding drawing on the labeller must not appear to have come from a sequenced read.** Nothing has been analysed. **Logged as `D-3` in `DEVIATIONS.md` and ruled by David on 27 Aug: proceed with the exposure disclosed.** The exposure postdates the freeze by three days, so the registered claim about the state at freeze time is unaffected.

### Downloaded and examined — 27 Aug 2026

**Kept separate from the pinned manifest above on purpose.** *Pinned* is what the audit is defined over; *downloaded and examined* is what was actually fetched and read. They are not the same set, and conflating them would overstate the read.

**Downloaded: 7 of the 10 pinned files, 886,243,617 bytes of 8,950,563,771.** Fetched per-file with `kaggle competitions download -c kkbox-churn-prediction-challenge -f <file>` to `/Volumes/MULLETT_T7/kkbox-wsdm2017/`, never into this repository. **Every one verified byte-for-byte against the pinned manifest on arrival — all seven match.**

| Release | Downloaded | Examined |
|---|---|---|
| Original | `train.csv.7z` · `transactions.csv.7z` · `sample_submission_zero.csv.7z` | all three |
| `_v2` | `train_v2.csv.7z` · `transactions_v2.csv.7z` · `sample_submission_v2.csv.7z` | all three |
| Shared | `WSDMChurnLabeller.scala` | read as documentation of the rule; see D-3 |

**Not downloaded — 8,064,320,154 bytes (8.06 GB):** `user_logs.csv.7z` (7.14 GB), `user_logs_v2.csv.7z` (686 MB), `members_v3.csv.7z` (242 MB). Scoped out before the read on the ground that none of K1–K6 references listening behaviour or demographics, and the members file has had `expiration_date` removed. **Persistence was tested against transaction activity instead of listening activity** — the apposite signal for a pathology about subscription state. No K-answer turned out to hinge on the excluded files.

**Extraction:** `bsdtar` (libarchive, already present) reads the 7-Zip archives; no installation was needed. The `_v2` archives unpack under an internal `data/churn_comp_refresh/` path.

**Data handling, per §7.B.** No raw row ever entered a model context. Every script prints aggregates only — counts, shares, distributions, min/max — and no `msno` value is printed anywhere. Analysis ran locally; only aggregates were returned. Scripts are committed to `scripts/` under §8.B; the data stays on the external volume, and `.gitignore` blocks `*.7z`, `*.csv` and `data/` structurally rather than by convention.

**Answers:** `KKBOX-ANSWERS.md`. **No branch assigned** — that is made separately under §6 and published with its reasoning.

---

### Calibration — recorded before the verdict, not after

**The declared expectation, on record in §2 of the frozen plan before anything was read:** both instruments come back **negative**, and KKBox in particular **"may turn out to be window censoring rather than absorption."**

**The result is negative by a different mechanism.** What the read found is the unit **leaving the denominator** — out-of-window expiries excluded from the cohort outright, which is exclusion, not censoring. The window-edge case that would have been censoring is flat in the original release and undeterminable in `_v2`.

**Right branch family, wrong sub-mechanism.** The direction was called correctly; the route to it was not. That is worth logging as calibration data rather than rounded off to "expectation confirmed" — a prediction that names a mechanism and gets a different one is only partly right, and the partly is the informative half.

**Timing matters here and is the reason this note exists at this point in the file.** It is written **before** the §6 branch assignment. Recorded afterwards it would be unfalsifiable, because the verdict would already be visible.

---

### What R1′ actually bought — D-2's rationale partly superseded by evidence

**D-2 adopted R1′ to remove a researcher degree of freedom**, on the reasoning that pinning both releases meant no choice between candidate releases was being exercised, and that it covered both readings of the month-semantics ambiguity.

**The read shows that framing was partly wrong.** `train_v2.csv` is the original release's test cohort **exactly** — 970,960 users each, intersection 970,960, **100.00%, zero on either side** (Observation 1 in `KKBOX-ANSWERS.md`). The two releases are not alternatives between which a choice had to be neutralised. **They are sequential windows on one population.**

**So R1′ did not neutralise a choice. It supplied K3 its cross-window comparison** — the only way to answer "absorbing or delayed," which asks by construction about a *later window*. Under R1 alone, K3 would have been unanswerable and the release would have been chosen on a rationale that misdescribed what the alternatives were.

**Logged rather than corrected in place.** D-2 stands as written, because it records what was believed at the time and why, and the deviations log exists to preserve that. **This note records that the evidence has since moved part of its reasoning.** The decision was right; one of its stated reasons was not the operative one.

---

### Licence and data-handling position — KKBox

**Recorded 27 Aug 2026 from the competition rules page** (`kaggle.com/competitions/kkbox-churn-prediction-challenge/rules`), **WSDM 2018 Cup Official Competition Rules.** Every section below was read on the page and quoted from it, not summarised from memory.

**§7.A · Data Access and Use — permitted purposes.** After acceptance, the Data may be accessed and used *"only for the purposes of the Competition, participation on Kaggle Website forums, academic research and education."* **Commercial use is not on that list.**

> **This audit sits inside §7.A by construction.** KKBOX is a public instrument and this is academic research and education. **No KKBOX data has been or will be used for any purpose outside that clause**, and §8 of the frozen plan independently bars any use of an unpublished finding.
>
> **⟦ REDACTED FOR PUBLICATION — 31 Aug 2026 ⟧** *The paragraph originally here stated a commercial policy of the wider project and how it interacts with §7.A. It is business positioning, not audit provenance, and it does not belong in a scientific record. **The substantive licence conclusion is unchanged and stated above.** Removed deliberately and marked rather than deleted silently, because a record whose value is that it is not curated must show where it has been.*

**§7.B · Data Security — publication and redistribution prohibited.** *"You agree not to transmit, duplicate, publish, redistribute or otherwise provide or make available the Data to any party not participating in the Competition."*

> **Consequence for the write-up: findings are publishable, data is not.** Answers, counts, shares, denominators, thresholds and reasoning may all be published. **Rows, records, extracts and derived datasets may not.** **The pre-registration's commitment to publish every outcome is unaffected** — §0 commits to publishing the answers and the reasoning, not the data, and it was never a commitment to redistribute an instrument's contents.

**§7.B, second clause · the access obligation, and what it means for how the read is run.** *"You agree to use reasonable and suitable measures to prevent persons who have not formally agreed to these Rules from gaining access to the Competition Data."*

> **Consequence for the read: raw data must not enter a model context.** **Analysis runs locally; only aggregates return.** Pasting rows into a model context would put the Data in front of a party that has not accepted the Rules, which is the thing this clause forbids. This is an operational constraint on method, not a limit on what may be found.

**§8.B · Public Code Sharing — how reproducibility survives the data prohibition.** *"You are permitted to publicly share source or executable code developed in connection with or based upon the Competition Data … By so sharing, you are deemed to have licensed the shared code under any of the eligible Open Source licenses listed below."*

> **This is the mechanism that preserves reproducibility without publishing data:** the analysis code is published openly, and **anyone who accepts the Rules themselves can run it against their own copy.** Verification transfers; the data does not move.
>
> ⚠️ **Correction to the framing this entry was given.** The OSI-approved requirement is **§8.C, not §8.B**, and it governs *Open Source code used in the model* — requiring an *"Open Source Initiative-approved license"* that *"in no event limits commercial use."* §8.B is the permission to share plus deemed licensing under the competition's listed eligible licences. **The two were merged in the instruction; they are separate clauses with different subjects.** Recorded per the standing rule that corrections are logged rather than quietly absorbed — including corrections that run upward.

**§20 · Governing law.** *"All claims arising out of or relating to these Rules will be governed by law of Taiwan, excluding its conflict of laws rules, and will be litigated exclusively in Taiwan Taipei District Court."*

**Also noted, not asked for:** **§7.C External Data** permits the use of public data other than the Competition Data, subject to holding the rights to it. Relevant if the audit ever needs a comparison instrument alongside KKBox.

---

### ✅ τ-bench — PINNED 2026-08-27. Scope: **both repositories.** Rule: **R2′.**

**Nothing has been read.** Repositories were cloned and the pinned commits checked out. **No README body, no evaluation code, no scoring path, no release notes and no issue tracker were opened.** Scope and pinning were established from repository metadata only: `git tag`, `git log`, `git ls-tree --name-only`, GitHub repo metadata, and `gh release list` **titles**.

**Scope ruling — both repositories, pinned separately by SHA, distinguished at every point in the answers.**

Reasoning, recorded because the alternative was available and declined:

1. **The frozen plan names both.** §5a and the pinning field both contemplate τ-bench and τ²-bench.
2. **Narrowing after surveying the landscape would be a post-hoc degree of freedom.** The survey that revealed one repository to be dormant came *after* the freeze; using it to drop that repository would be selection dressed as scoping — the same move R1′ was adopted to avoid on KKBox.
3. **The dormant repository is cheap to audit and is the instrument much of the published literature used.** Auditing only the successor would answer a question about today's code and leave the corpus of published results unexamined.

**Selection rule — R2′, stated as a general rule rather than fitted to these repositories:**

> Pin the **latest tagged release** where the project tags; **where it does not tag, pin `main` at a recorded UTC date, by SHA.** **Additionally pin the immediately preceding release where there is documented reason to believe scoring behaviour changed between them**, answer each separately, and **report any divergence rather than selecting between them.**

**The trigger for the "additionally" limb, recorded explicitly:** `v1.0.1`'s own **release title** — *"banking_knowledge Grading Fixes"*. Grading is scoring, and scoring bears on Q1, Q2, Q3, Q5 and Q10. **Known from release titles only; the notes were not opened.** This satisfies §6's binding constraint that *"variation across versions is reported, never selected from"* — the preceding release is pinned so that any divergence becomes a reported result rather than an invisible one.

### The pins

| | Repository | Ref | **Commit SHA (full)** | Commit date | Working copy |
|---|---|---|---|---|---|
| **A** | `sierra-research/tau-bench` | `main` *(project does not tag)* | `59a200c6d575d595120f1cb70fea53cef0632f6b` | 2026-03-18T10:36:06-07:00 | `/Volumes/MULLETT_T7/tau-bench-audit/tau-bench` |
| **B** | `sierra-research/tau2-bench` | `v1.0.1` *(latest release)* | `fc0055dc4e0a316c3f83133267fbd6faaa770992` | 2026-07-16T15:24:56-07:00 | `…/tau2-bench-v1.0.1` |
| **C** | `sierra-research/tau2-bench` | `v1.0.0` *(preceding release)* | `17e07b1da2bbc0cadfddeea36412686e0604127b` | 2026-03-18T00:13:53-07:00 | `…/tau2-bench-v1.0.0` |

**Pinned on:** 2026-08-27. **Clones and worktrees live on the external volume, never in this repository** — `.gitignore` blocks `tau-bench/`, `tau2-bench/` and `tau-bench-audit/`, verified with `git check-ignore` against every tracked path. All three working copies verified checked out and clean at the SHAs above.

**⚠️ Tag-object versus commit, recorded to prevent a later misreading.** `v1.0.1` is an **annotated** tag: the tag object is `b711c1ead46f55111bf765cf44d5da8bacc2d28c`, which is **not a commit**; it points to commit `fc0055dc…`. `v1.0.0` is a **lightweight** tag, so its object and commit are the same, `17e07b1d…`. **The commit SHAs in the table are what govern.** The tag was created 2026-07-22, six days after the commit it marks.

### Licence position — MIT, both repositories

`tau-bench`: *"MIT License / Copyright (c) 2024 Sierra"*. `tau2-bench`: *"MIT License / Copyright (c) 2025 Sierra Research"*.

**What MIT permits, for this audit's purposes.** Use, copying, modification, publication, distribution and sublicensing, on the sole condition that the copyright notice and permission notice accompany substantial portions of the software. **Findings are publishable without restriction. Code excerpts may be quoted in the write-up**, with attribution, which is what a code-reading audit needs in order to cite.

> **⭐ This is materially different from the KKBox position and the difference should not be lost.** KKBox is governed by competition rules **§7.B**, which forbid publishing or redistributing the Data, and oblige measures preventing access by parties who have not accepted the rules — so that read returned aggregates only and no raw row entered a model context. **Neither constraint applies here.** τ-bench and τ²-bench are MIT-licensed public code, so the audit may quote the evaluation code directly, and the answers may cite file paths and line ranges. **The evidence standard rises accordingly: an answer that could be supported by a quotation and is not is a weaker answer here than it would have been on KKBox.**

### ⚠️ Naming instability, recorded at pinning

**"τ-bench" currently designates at least three distinct things:**

1. the **original repository**, `sierra-research/tau-bench`;
2. the **`tau2-bench` repository**, whose GitHub description reads *"τ-Bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"*;
3. **`v1.0.1` of `tau2-bench`**, whose release title is *"τ-bench 1.0.1 — banking_knowledge Grading Fixes"*.

**And `v1.0.0` of the same repository is titled *"τ³-bench 1.0.0 — Voice, Knowledge, Task Quality"***, so a third generation's name sits on a release inside the second generation's repository. **There is no `tau3-bench` repository** — checked; it does not resolve. The original repository's **final commit** is `59a200c`, *"Merge pull request #80 from sierra-research/update-readme-tau3-bench"* — its last act was to point readers at a successor.

**Resolvable by SHA, and therefore NOT an INDETERMINATE trigger.** §6 reserves INDETERMINATE for a finding that is *"configuration-dependent, undocumented, or version-variable beyond resolution."* Naming instability is resolved by pinning commits, which is what the table above does. **Recorded now, before the read, so that it cannot later be mistaken for something discovered and selected.**

**Flagged as a candidate OBSERVATION for `TAU-ANSWERS.md`:** it falls outside Q1–Q11, so under boundary 1 it belongs in the observations section and must not be folded into any answer. A benchmark whose name does not stably identify a version is a fact about the instrument that a reader comparing published results across papers would want.

---

## Hours

*(§7 requires this. Without it, the claim that the check is cheap to run is unsupported and gets dropped — not softened, dropped.)*

| Instrument | Task | Hours |
|---|---|---|
| KKBox | Scoping: brief and plan read, K1–K6 mapped to files, ignore rules and volume set up | 0.25 |
| KKBox | Download, byte-verification against the pinned manifest, extraction | 0.10 |
| KKBox | Scripts 01–02: file structure, release shape, cohort set relations | 0.20 |
| KKBox | Scripts 03–04: cohort-rule reconstruction (both readings), K2, reconstruction diagnostics | 0.35 |
| KKBox | Scripts 05–06: `_v2` in-release assessment, K3, window edge and the auto-renew confound test | 0.30 |
| KKBox | Writing `KKBOX-ANSWERS.md` | 0.25 |
| **KKBox** | **Total** | **1.45** |
| τ-bench | Brief verification against the frozen plan; boundary 9 added; D-6 annotated | 0.15 |
| τ-bench | B-versus-C diff: scoring path, error handling, pass^k, task definitions | 0.30 |
| τ-bench | Repository A read: runner, env, agent, user simulator, tools | 0.35 |
| τ-bench | Repository A static analysis: tool mutation classification, two corrections, task counts | 0.40 |
| τ-bench | Repository B read: evaluator, orchestrator, metrics, runner, retry path | 0.35 |
| τ-bench | Repository B task counts | 0.15 |
| τ-bench | Writing `TAU-ANSWERS.md` | 0.40 |
| **τ-bench** | **Total** | **2.10** |
| **BOTH INSTRUMENTS — THE AUDIT** | **Total** | **3.55** |
| *post-read* | Release-documentation sweep and F-1/F-2 revision (D-10) | *0.45* |
| *post-read* | Related-work read, arXiv:2607.00473 (D-11) | *0.30* |

> **The 3.55 is the number that supports the cheap-to-run claim, and the two rows below it are deliberately outside that total.** They are **publication work, not audit work** — done after both verdicts were assigned. Folding them in would inflate the cost of the check; hiding them would understate the cost of publishing one. Both are logged, and the line between them is stated rather than assumed.

**KKBox wall-clock from first download to last script: 26 minutes** (`08:29`–`08:55`, 27 Aug 2026). **Total machine time across all six scripts: under 4 minutes** on one laptop core, Python standard library only, no dependencies installed.

**τ-bench wall-clock: 35 minutes** (`12:30`–`13:05`, 27 Aug 2026). **No execution, no API calls, no cost** — a code read at three pinned commits.

> **This is the number that supports the cheap-to-run claim, so it is recorded plainly rather than favourably.** The 1.45 hours covers a read of one instrument by someone who already knew the plan; it excludes the pre-registration, the adversarial review rounds, and the pinning work logged above.

---

## Findings

*(answers with citations go here as they're produced; the branch assignment and reasoning go in the write-up)*

---

## Correspondence

*(maintainer and publisher contact, and their responses — published in full and unedited alongside the finding, per §8)*

### ✅ τ-bench maintainers — CONTACTED 2026-08-28

- **Channel:** public GitHub issue — **https://github.com/sierra-research/tau2-bench/issues/497**
- **Title:** *"Pre-registered audit: two documented conventions for pass^k, and a question about which governs published figures"*
- **Opened by:** `davidmullett`, 28 Aug 2026. **Status at filing: Open. No response yet.**
- **Text as sent:** `maintainer-notifications.md`, Email 1, synced to the posted body.

**Why a public issue rather than private email — recorded because the plan did not fix the channel.**

The repository publishes **no `SECURITY.md`** and **no maintainer contact address in `CONTRIBUTING.md`**; its **documented route for questions is GitHub Issues.** A private channel would have had to be invented. Using the project's own stated route is the correct reading of §8's *"contact the maintainers"* and has the side benefit that the contact is itself timestamped and public.

> ⚠️ **One consequence, disclosed.** Because the channel is public, the **contact and the correction window are now visible to third parties before publication.** §8 requires contact and a window; it does not require either to be private. **Nothing in §8 was relaxed** — the findings, the frozen plan and the scripts remain unpublished until the window closes.

**A drafting error caught before posting, recorded per the standing rule.** The draft carried the sentence *"which is the reason I'm sending this one privately rather than posting it"* — written when the channel was still undecided and **false once the channel became a public issue.** Caught at the submit step and corrected in both the posted body and `maintainer-notifications.md`. **Logged here rather than silently fixed** because it would have been a false statement inside the one document whose value rests on not overclaiming.

### ✅ KKBOX / WSDM Cup 2018 — SENT 2026-08-28

Email 2 in `maintainer-notifications.md`, sent by private email.

> ## ✅ §8 IS NOW SATISFIED FOR BOTH INSTRUMENTS.
>
> ⚠️ §8 — SATISFIED FOR τ-BENCH, PARTIALLY DISCHARGED FOR KKBOX. Corrected 9 September 2026.
>
> τ-bench: contacted 28 Aug via the channel the repository documents, followed up privately 31 Aug. No reply. Satisfied.
>
> KKBOX: the party §8 names was never reached. One address delivered and did not reply, one bounced, and the two KKBOX organisers had no findable address. The forwarding route the draft relied on failed with them. See the delivery table below and `correspondence/README.md`.
>
> **Both correction windows close 6 September 2026. Publication due 10 September.** The §8 no-commercial-use constraint runs until publication **and** the windows have both closed.

| Recipient | Address | Status |
|---|---|---|
| **Shou-De Lin** — NTU, CSIE | `sdlin@csie.ntu.edu.tw` | ✅ **verified** — `mailto:` on his own NTU page |
| **Xing Xie** — Microsoft Research Asia | `xingx@microsoft.com` | ⚠️ **probable, unverified** — inferred from his MSR profile slug; no page displayed it in full — SENT ANYWAY AND BOUNCED, 28 Aug: "the address couldn't be found, or is unable to receive mail." The unverified flag was correct. |
| **Yian Chen** — KKBOX | — | ❌ no public address; **the draft asks Lin and Xie to forward** |
| **Yuh-Ming Chiu** — KKBOX | — | ❌ no public address; same |

**Channel — RULED: private email, no Kaggle discussion board post.** Chosen by David on 28 Aug by directing the draft to Gmail. **This is the opposite ruling from Email 1 and the reason for the difference is on the record:** Sierra publishes no contact address and names GitHub Issues as its own channel, so a public issue was the project's documented route; the WSDM Cup organisers have no published addresses. Two were found by other means; one delivered, one bounced. The route to KKBOX itself was forwarding by Lin or Xie — and that route failed: Xie never received the email, and Lin did not reply. **Neither KKBOX organiser was reached. Recorded as a partial discharge of §8.**

> **Consequence, recorded because Email 1's opposite ruling has one too.** Email 2's sentence *"I'd rather fix an error in email than in public"* is **true as sent**, and remains true only while the board is not used. **If the Kaggle discussion board is ever used for this, that line must be rewritten first.**

**Also disclosed in the draft, matching `EXECUTION-LOG.md:141`:** that `user_logs`, `user_logs_v2` and `members_v3` were never opened. An earlier version of the email listed `members_v3` among the audited files; it was never downloaded. **Corrected before drafting.**

---

### ⏳ Correction window

**Opened 2026-08-28 (τ-bench). Closes 2026-09-06.** Publication due **2026-09-10** per §8.

**§8 binding constraint, in force until both have closed: no commercial use of any finding.**
