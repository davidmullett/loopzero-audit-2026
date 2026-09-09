# Correspondence

**§8 of the frozen plan:** *"Maintainers (τ-bench) and the dataset's publishers (KKBox) receive the finding before public write-up, with a reasonable correction window; their reply is published verbatim alongside."*

This directory holds **what was sent, when, and to whom**, so that the window can be checked rather than taken on trust — and, in `replies/`, whatever came back, **unedited**.

---

## What was sent

| | Instrument | Channel | Sent | Window closes |
|---|---|---|---|---|
| **1** | **τ-bench / τ²-bench** — Sierra | **Public GitHub issue** [#497](https://github.com/sierra-research/tau2-bench/issues/497) | 28 Aug 2026 | 6 Sep 2026 |
| **2** | **KKBOX / WSDM Cup 2018** — competition organisers | Private email | 28 Aug 2026 | 6 Sep 2026 |
| **1b** | τ-bench — direct follow-up | Private email to two named authors | 31 Aug 2026 | — |

**Files:** `tau-bench-issue-497.md` · `wsdm-cup-2018-email.md` · `tau-bench-followup-2026-08-31.md`

---

## Why the two channels differ, since it is visible and would otherwise look inconsistent

**Sierra received a public issue.** The repository publishes no `SECURITY.md` and no contact address in `CONTRIBUTING.md`; it names **GitHub Issues as its own route for questions**. Using a project's documented channel is the correct reading of §8, and a public issue timestamps the contact independently.

> ## 🔴 CORRECTION — 8 September 2026. ~~"The WSDM Cup organisers received a private email, because they have working addresses."~~
>
> **That sentence was wrong on both halves, and it stood in this file for eleven days.**
>
> **One of the two addresses did not work.** `xingx@microsoft.com` returned a hard bounce — *"the address couldn't be found, or is unable to receive mail"* — **twelve seconds after sending, on 28 August.** The notice landed in the same inbox that logged the send. **It was not noticed until 8 September, publication day.**
>
> **And "the organisers" overstates who was reached.** WSDM Cup 2018 had four: Shou-De Lin (NTU), Xing Xie (Microsoft), and **Yian Chen and Yuh-Ming Chiu, both of KKBOX**. The competition site names all four and publishes no addresses. **§8 names *"the dataset's publishers (KKBox)"* — and neither KKBOX organiser had a findable address, so neither was contacted at all.**
>
> | Recipient | Outcome |
> |---|---|
> | **Shou-De Lin** · `sdlin@csie.ntu.edu.tw` | delivered · **no reply** |
> | **Xing Xie** · `xingx@microsoft.com` | 🔴 **bounced, 28 Aug** |
> | **Yian Chen**, KKBOX | no public address · **not contacted** |
> | **Yuh-Ming Chiu**, KKBOX | no public address · **not contacted** |
>
> **Recorded as a PARTIAL discharge of §8.** The effort was genuine — all four identified, both findable addresses used — but the party the plan names was not reached, and the write-up says so in those words.
>
> ### ⚠️ §13 INSTANCE 11 — and it is the closest to home yet
>
> **The correspondence record reported a successful notification while one of its two channels had failed**, and the evidence of failure was delivered to the same mailbox on the same day. **A record that logs sends and not deliveries cannot distinguish "notified" from "attempted."**
>
> **Rule: a notification is discharged on delivery, not on send.** Check for a bounce before recording contact as made — and where a party cannot be reached at all, record *that*, rather than describing the people you did reach as though they were the ones named.

> **One consequence of the public channel, disclosed rather than left to be noticed:** the τ-bench contact and its correction window have been visible to third parties since 28 August. §8 requires contact and a window; it does not require either to be private. **Nothing in §8 was relaxed** — the findings, the frozen plan and the scripts stayed unpublished until the window closed.

## The follow-up, and why it was sent

**Five days after the issue was opened it had no reply, no labels and no assignee**, on a repository carrying roughly 90 open issues and 97 open pull requests. Silence there is the base rate rather than a signal — but the documented channel was chosen *because* it was documented, not because it was likely to reach a person.

A short note therefore went directly to two named authors of the τ²-Bench paper, pointing at the issue, restating the closing date, and asking **one** question with a one-line answer. **No new claims were made.**

> **It also removed the deadline as pressure on them:** *"If a reply arrives after I publish, I'll add it unedited and note when it came — the commitment is to publish your response, not to a deadline for you."* **The window was offered for their benefit and should not function as a reason not to bother.** A late reply publishes here as a dated update.

---

## Replies

`replies/` holds everything received, **in full and unedited**, per §8 — including anything arriving after publication, marked with the date it came.

**Where no reply was received, that is stated plainly rather than omitted.**

---

## Thread state, verified 3 September 2026

**Neither instrument's maintainers have replied.** Issue #497 is open, unlabelled, unassigned, with zero comments six days after the direct follow-up to two named authors. No reply from the WSDM Cup organisers either.

> ### But the τ-bench thread is no longer inert, and the reason is not Sierra
>
> On **3 September** a third party, **YangzeLiu**, filed [#502](https://github.com/sierra-research/tau2-bench/issues/502) — an **executed** re-grading study of the same harness — and cross-referenced #497 from it. That cross-reference is the only activity #497 has received.
>
> **This is not a §8 reply and must not be recorded as one.** §8 obliges publication of the *maintainers'* response. Liu is not a maintainer, has no connection to this audit, and neither of us contacted the other. **It is third-party context, filed in `RELATED-WORK.md` §2, and it goes in the write-up on that footing.**
>
> **Nothing about the correction window changes.** It still closes 6 September; a late reply from Sierra still publishes as a dated update.

**⚠️ On 8 September the write-up must say what is true on that date, not what was true on 31 August.** If Sierra has still not replied, say so plainly — *"contacted 28 August via the channel the repository documents, followed up privately 31 August, no response"* — and note that an independent report on the same instrument arrived on 3 September and was not solicited.
