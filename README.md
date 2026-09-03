# Audit record — KKBOX and τ-bench, 2026

The full record behind a pre-registered audit of two public instruments: the
**KKBOX / WSDM Cup 2018** churn dataset and the **τ-bench / τ²-bench**
evaluation harnesses.

The plan was written, hashed, and publicly registered **before either
instrument was opened**. Both came back negative for the mechanism the plan
went looking for. Seven other findings are reported, each carrying an evidence
grade.

**Write-up:** *[URL — added on publication]*

**Registration:** [osf.io/ksm3n](https://osf.io/ksm3n) · DOI
[10.17605/OSF.IO/KSM3N](https://doi.org/10.17605/OSF.IO/KSM3N) · timestamped
`2026-08-24T15:33:01Z`

---

## Verify the frozen plan

`PRE-REGISTRATION.md` is the plan as registered. It has not been modified since
the freeze. Its SHA-256 is the registered artifact:

```
b15f472ef72994970957eda1e1ebc53f5480b759eb6ab71e076496145a7fda0e
```

Check it:

```bash
shasum -a 256 PRE-REGISTRATION.md
```

or against the sidecar:

```bash
shasum -a 256 -c PRE-REGISTRATION.sha256
```

`PRE-REGISTRATION.sha256` carries construction notes after the hash line, so
`-c` reports the notes as unformatted lines. The line that matters is
`PRE-REGISTRATION.md: OK`.

Then check the timestamp on the registration. The hash is recorded in a
separate file rather than inside the plan, because writing a document's hash
into that document changes the hash.

## The three pinned commits

The τ-bench work was a code read at three pinned commits. No model was called,
no benchmark was run.

| | Repository | Ref | Commit |
|---|---|---|---|
| **A** | `sierra-research/tau-bench` | `main` *(project does not tag)* | `59a200c6d575d595120f1cb70fea53cef0632f6b` |
| **B** | `sierra-research/tau2-bench` | `v1.0.1` | `fc0055dc4e0a316c3f83133267fbd6faaa770992` |
| **C** | `sierra-research/tau2-bench` | `v1.0.0` | `17e07b1da2bbc0cadfddeea36412686e0604127b` |

`v1.0.1` is an annotated tag: the tag object `b711c1ead46f55111bf765cf44d5da8bacc2d28c`
is **not** a commit — it points to `fc0055dc`. The commit SHAs above govern.

Both repositories are MIT-licensed, so code is quoted directly and every claim
cites a path and line range at a pinned SHA.

## No KKBOX data is published

None. No rows, no extracts, no derived datasets, no sample files. §7.A of the
WSDM Cup 2018 competition rules permits use of the Competition Data for
academic research and education and for nothing else; §7.B requires
participants not to transmit, duplicate, publish or redistribute it.

The analysis scripts are publishable under §8.B, which permits public sharing
of code developed in connection with the Competition Data and deems anything
so shared licensed under an eligible open-source licence. These are MIT.
Anyone who has accepted the rules can obtain their own copy and point the
scripts at it with the `KKBOX_DATA` environment variable. The scripts print
aggregates only; no user identifier is printed under any code path.

**Verification transfers; the data does not move.**

## What is here

| Path | |
|---|---|
| `PRE-REGISTRATION.md` | the frozen plan, byte-identical to the registered artifact |
| `PRE-REGISTRATION.sha256` | its hash, with construction notes |
| `KKBOX-ANSWERS.md`, `TAU-ANSWERS.md` | every question, with citations and an evidence grade on each claim |
| `KKBOX-VERDICT.md`, `TAU-VERDICT.md` | branch assignments, with the reasoning for each condition |
| `DEVIATIONS.md` | all eleven deviations, including the four that reduced what could be claimed |
| `EXECUTION-LOG.md` | pinning, timings, and the order things happened in |
| `RELATED-WORK.md` | prior work |
| `correspondence/` | what was sent to the maintainers, to whom, and when |
| `scripts/` | the analysis scripts, MIT |

## Provenance

The code reading and the analysis were performed by an AI coding agent working
to a brief fixed before the read. **This is not expert review, not peer review,
and confers no warrant.** The reasoning is set out in §11 of the frozen plan and
in `DEVIATIONS.md`.

---

*Any reader can apply the stated rule to the published evidence and see whether
they reach the same branch. Disagreement is invited.*
