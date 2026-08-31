"""02 - Shape of each release, and how the cohorts relate.

Two things:
  (a) monthly histogram of transaction_date in each transactions file, which
      bears on the cumulative-vs-incremental question recorded as ambiguity #2
      in EXECUTION-LOG.md;
  (b) set relations between the four label/submission cohorts, by count only.

(b) compares MEMBERSHIP OF LABEL FILES ACROSS RELEASES. It never computes a
label or a behavioural quantity for one release from another release's files,
which is what boundary 6 forbids. Flagged as a judgement call in the report.

Prints aggregates only. msno values are hashed into sets and counted; none is
ever printed.

Run:  python3 02_release_shape.py
"""

import collections

from common import RELEASES, emit, guard_no_values, path, pct, rows


def month_histogram(release):
    p = path(release, "transactions")
    by_month = collections.Counter()
    n = 0
    for r in rows(p):
        n += 1
        by_month[r["transaction_date"][:6]] += 1
    print(f"  {RELEASES[release]['transactions']}  ({n:,} rows)")
    for m in sorted(by_month):
        share = pct(by_month[m], n)
        bar = "#" * int(share / 2)
        print(f"    {m}  {by_month[m]:>10,}  {share:6.2f}%  {bar}")
    return by_month, n


def user_set(release, kind):
    return {r["msno"] for r in rows(path(release, kind))}


def relate(name_a, a, name_b, b):
    inter = len(a & b)
    print(f"    {name_a:<28} n={len(a):>9,}")
    print(f"    {name_b:<28} n={len(b):>9,}")
    print(f"      intersection              {inter:>9,}"
          f"   ({pct(inter, len(a)):.2f}% of first, {pct(inter, len(b)):.2f}% of second)")
    print(f"      in first only             {len(a - b):>9,}")
    print(f"      in second only            {len(b - a):>9,}")
    print()


def main():
    guard_no_values()

    emit("TRANSACTION_DATE BY MONTH, PER RELEASE (ambiguity #2 evidence)")
    for rel in ("original", "v2"):
        month_histogram(rel)
        print()

    emit("COHORT SET RELATIONS (membership only, counts only)")
    sets = {
        ("original", "train"): None,
        ("original", "submission"): None,
        ("v2", "train"): None,
        ("v2", "submission"): None,
    }
    for key in list(sets):
        sets[key] = user_set(*key)

    print("  Within the original release:")
    relate("original train", sets[("original", "train")],
           "original submission (test)", sets[("original", "submission")])

    print("  Within the _v2 release:")
    relate("v2 train", sets[("v2", "train")],
           "v2 submission (test)", sets[("v2", "submission")])

    print("  ACROSS releases -- does the _v2 train cohort correspond to the")
    print("  original test cohort? This is what K3 (absorbing vs delayed) turns on:")
    relate("original submission (test)", sets[("original", "submission")],
           "v2 train (labelled)", sets[("v2", "train")])

    print("  And the two labelled cohorts against each other:")
    relate("original train", sets[("original", "train")],
           "v2 train", sets[("v2", "train")])


if __name__ == "__main__":
    main()
