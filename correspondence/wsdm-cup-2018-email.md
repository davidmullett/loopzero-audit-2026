# KKBOX / WSDM Cup 2018 — as sent

**Channel:** private email to the competition organisers
**Sent:** 28 August 2026 · **Correction window closes:** 6 September 2026
**Subject:** *Pre-registered audit of the WSDM Cup 2018 churn label — findings ahead of publication, correction window to 6 September*

> **It is WSDM Cup *2018*, not 2017.** The data covers 2017; the Cup ran at WSDM 2018. An earlier draft said 2017 in the heading and subject while citing a 2018 paper three paragraphs later. Corrected before sending.

---
Hello,

I've completed a pre-registered audit of the churn label rule in the WSDM Cup 2018 dataset and I'm sending you the findings before writing them up publicly, with a correction window. Any reply you send will be published verbatim and unedited alongside. If you'd rather not reply, I'll note that I contacted you and had no response.

**What this was.** I fixed six questions about the label rule, hashed the document, and registered the hash publicly before opening any file — OSF `osf.io/ksm3n`, DOI `10.17605/OSF.IO/KSM3N`, timestamped 24 August. The questions came from a paper of mine about a defect I found in my own benchmark, where an eligibility clause silently moved the worst-affected units into the healthy class.

**I did not find that defect here.** The rule handles out-of-window users by excluding them from the labelled cohort, which the documentation states plainly and the data confirms. That's the correct treatment, and it's the finding.

Three other things came up that I think are worth your attention.

**Releases audited:** the original release and the 6 November 2017 `_v2` refresh. Specifically: `train.csv`, `transactions.csv`, `sample_submission_zero.csv`, their three `_v2` counterparts, and `WSDMChurnLabeller.scala`. **I did not open `user_logs`, `user_logs_v2` or `members_v3`** — none of my six questions referenced listening behaviour or demographics, so I tested persistence against transaction activity instead. I worked only from the competition's public data-description page and the distributed files, under the competition rules I accepted. No data is reproduced here or in the write-up — findings and aggregate counts only.

---

**1 · The labels can't be verified against the files shipped with them.**

`transactions.csv` ends at `20170228`. The February expiries it's meant to explain need observation through 30 March under the stated 30-day rule. So none of the 992,931 labels in `train.csv` can be checked against the transactions file distributed alongside it. The same holds for `_v2`: its transactions end `20170331` and its March expiries need April.

**For the original release, I think this is a publishing artefact rather than a labelling one.** The data description states your log history runs to 2017-03-31. A February expiry plus 30 days ends 30 March at the latest, so the labeller had what the rule requires even though the distributed transactions file does not. The truncation is in what was published.

**For `_v2` I can't say the same, and this is the part I'd most like corrected.** Its window is March 2017 expiries, so a `20170331` expiry needs observation to `20170430` — beyond the 2017-03-31 end of the history the data description says you used. **Of the 31 expiry days in that window, only 20170301 has a full 30 days available inside that stated history.** Either the production labeller ran on history extending past 2017-03-31, or the later-expiring users in `train_v2.csv` were labelled on partial observation. The distributed material doesn't distinguish these, and the difference matters to anyone using those labels.

Either way, a downstream user reproducing the rule from the distributed files alone cannot check either release's labels.

**2 · The cohort rule doesn't reproduce exactly.**

My best reconstruction matches 881,477 of 992,931 labelled users — **88.78%**. Of the misses, 81% have a standing expiry *after* the window under my reconstruction, which is consistent with post-cutoff cancellations pulling expiry dates back into it. The data description notes that `WSDMChurnLabeller.scala` has its dates modified for local running, so the distributed script isn't the production configuration — which likely explains the gap. I mention it because every count I report inherits it, and I've marked them accordingly.

**3 · The churn rate moves 41% between adjacent months.**

6.392% for February (n = 992,931) against 8.994% for March (n = 970,960). Nothing in the distributed material establishes whether that's seasonality, a change in cohort composition, or a difference in how the two label sets were produced. If you know which, I'd genuinely like to include it.

---

**What I'd value from you.** Whether I've misread the label rule, whether the two releases were produced the same way, and anything on the month-over-month difference.

**And one direct question, which may resolve #2 entirely:** does *"WSDM Cup 2018: Music Recommendation and Churn Prediction"* (ACM DL, 10.1145/3159652.3160605) document the production labeller configuration? I could not access it. If the paper specifies the history window the labeller actually used, my 88.78% gap probably has a mundane explanation and I'd rather report that than the gap.

**Corrections are what this window is for** — I'd rather fix an error in email than in public.

**Correction window closes 6 September.** After that I publish the findings, the frozen plan in full, and the analysis scripts — which anyone who has accepted the competition rules can run against their own copy. **No data will be published**, per §7.B of the competition rules.

Nothing here has been used commercially and won't be until publication and the window have closed.

Best,
David Mullett
Independent researcher · ORCID 0009-0004-2543-1664
d@loopzero.org
