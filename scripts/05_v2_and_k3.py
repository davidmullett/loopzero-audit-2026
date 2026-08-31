"""05 - The _v2 release on its own terms, and K3 across releases.

Part 1: what can and cannot be established INSIDE the _v2 release, using only
        transactions_v2.csv and train_v2.csv. The answer to "can this release
        reconstruct its own cohort" is itself a result, and it is measured here
        rather than asserted.

Part 2: K3 (absorbing or delayed?). Compares LABEL FILE MEMBERSHIP AND LABELS
        across the two releases. It computes nothing behavioural across
        variants -- no label is derived for one release from another release's
        transactions. Flagged as a judgement call in KKBOX-ANSWERS.md.

Prints aggregates only.

Run:  python3 05_v2_and_k3.py
"""

import collections

from common import day_gap, emit, guard_no_values, path, pct, rows

V2_CUTOFF = "20170228"
V2_WIN_LO, V2_WIN_HI = 20170301, 20170331
V2_HORIZON = "20170331"


def main():
    guard_no_values()

    emit("PART 1 -- CAN THE _v2 RELEASE RECONSTRUCT ITS OWN COHORT?")
    v2_lab = {r["msno"]: r["is_churn"] for r in rows(path("v2", "train"))}
    v2_set = set(v2_lab)
    print(f"  labelled users in train_v2.csv        : {len(v2_set):,}")

    pre_cutoff_users = set()
    pre_cutoff_rows = 0
    in_window_expiry = set()
    total_rows = 0
    for r in rows(path("v2", "transactions")):
        total_rows += 1
        if r["transaction_date"] <= V2_CUTOFF:
            pre_cutoff_rows += 1
            pre_cutoff_users.add(r["msno"])
            e = int(r["membership_expire_date"])
            if V2_WIN_LO <= e <= V2_WIN_HI:
                in_window_expiry.add(r["msno"])

    print(f"  rows in transactions_v2.csv           : {total_rows:,}")
    print(f"  rows dated <= {V2_CUTOFF} (the history) : {pre_cutoff_rows:,}"
          f"   ({pct(pre_cutoff_rows, total_rows):.2f}%)")
    print(f"  distinct users in that history        : {len(pre_cutoff_users):,}")
    have = len(v2_set & pre_cutoff_users)
    print("\n  Of the labelled cohort, how many have ANY pre-window transaction")
    print("  inside this release's own transactions file?")
    print(f"    present  : {have:,}   ({pct(have, len(v2_set)):.2f}%)")
    print(f"    ABSENT   : {len(v2_set) - have:,}"
          f"   ({pct(len(v2_set) - have, len(v2_set)):.2f}%)")
    print("\n  A user's cohort entry is decided by the expiry standing before the")
    print("  window opens. Without a pre-window transaction that expiry cannot be")
    print("  established from this file, so cohort selection is not reproducible")
    print("  in-release for the absent group.")

    emit("_v2 -- CAN THE 30-DAY TEST BE OBSERVED INSIDE THIS RELEASE?")
    print(f"  this release's transactions end        : {V2_HORIZON}")
    print(f"  window of labelled expiries            : {V2_WIN_LO} .. {V2_WIN_HI}")
    last_fully = day_gap(str(V2_WIN_LO), V2_HORIZON)
    print(f"  days from window open to file end      : {last_fully}")
    print("  A 30-day non-renewal test on an expiry of 20170301 needs data through")
    print("  20170331; on 20170331 it needs data through 20170430.")
    determinable = 1 if last_fully is not None and last_fully >= 30 else 0
    print(f"  expiry days in the window with a full 30-day observation available:"
          f" {'20170301 only' if determinable else 'NONE'}")

    emit("_v2 -- THE REPORTED METRIC")
    ch = sum(1 for v in v2_lab.values() if v == "1")
    print(f"  labelled users : {len(v2_set):,}")
    print(f"  is_churn=1     : {ch:,}   ({pct(ch, len(v2_set)):.3f}%)")

    emit("PART 2 -- K3: ABSORBING OR DELAYED? (label files only, both releases)")
    o_lab = {r["msno"]: r["is_churn"] for r in rows(path("original", "train"))}
    o_set = set(o_lab)
    o_sub = {r["msno"] for r in rows(path("original", "submission"))}
    v2_sub = {r["msno"] for r in rows(path("v2", "submission"))}

    both = o_set & v2_set
    print(f"  labelled in the Feb-2017 cohort        : {len(o_set):,}")
    print(f"  labelled in the Mar-2017 cohort        : {len(v2_set):,}")
    print(f"  labelled in BOTH                       : {len(both):,}"
          f"   ({pct(len(both), len(o_set)):.2f}% of the Feb cohort)")

    print("\n  Label transition for users labelled in both windows:")
    trans = collections.Counter()
    for m in both:
        trans[(o_lab[m], v2_lab[m])] += 1
    print("    Feb -> Mar        users        share of Feb cohort labelled in both")
    for k in sorted(trans):
        print(f"      {k[0]} -> {k[1]}        {trans[k]:>9,}        {pct(trans[k], len(both)):6.2f}%")

    print("\n  Feb-cohort users NOT labelled again in the Mar cohort:")
    gone = o_set - v2_set
    gone_ch = sum(1 for m in gone if o_lab[m] == "1")
    print(f"    count                                : {len(gone):,}"
          f"   ({pct(len(gone), len(o_set)):.2f}% of the Feb cohort)")
    print(f"    of those, labelled churn=1 in Feb    : {gone_ch:,}"
          f"   ({pct(gone_ch, len(gone)):.2f}%)")
    print(f"    of those, labelled churn=0 in Feb    : {len(gone) - gone_ch:,}"
          f"   ({pct(len(gone) - gone_ch, len(gone)):.2f}%)")
    print("    do any of them appear in the NEXT cohort (Apr test set)?")
    print(f"      in Apr test cohort                 : {len(gone & v2_sub):,}")

    print("\n  Of Feb users labelled NOT-churned (is_churn=0), what happens next?")
    zero = {m for m in o_set if o_lab[m] == "0"}
    z_both = zero & v2_set
    z_ch = sum(1 for m in z_both if v2_lab[m] == "1")
    print(f"    labelled 0 in Feb                    : {len(zero):,}")
    print(f"      re-labelled in the Mar cohort      : {len(z_both):,}"
          f"   ({pct(len(z_both), len(zero)):.2f}%)")
    print(f"        of those, churn=1 in Mar         : {z_ch:,}"
          f"   ({pct(z_ch, len(z_both)):.2f}%)")
    print(f"      NOT re-labelled in Mar             : {len(zero - v2_set):,}"
          f"   ({pct(len(zero - v2_set), len(zero)):.2f}%)")
    print(f"        of those, in the Apr test cohort : {len((zero - v2_set) & v2_sub):,}")

    print("\n  Of Feb users labelled CHURNED (is_churn=1), what happens next?")
    ones = {m for m in o_set if o_lab[m] == "1"}
    o_both = ones & v2_set
    o_ch = sum(1 for m in o_both if v2_lab[m] == "1")
    print(f"    labelled 1 in Feb                    : {len(ones):,}")
    print(f"      re-labelled in the Mar cohort      : {len(o_both):,}"
          f"   ({pct(len(o_both), len(ones)):.2f}%)")
    print(f"        of those, churn=1 again in Mar   : {o_ch:,}"
          f"   ({pct(o_ch, len(o_both)):.2f}%)")

    emit("COHORT SUCCESSION (membership counts only)")
    print(f"  Feb labelled  {len(o_set):>9,}")
    print(f"  Mar labelled  {len(v2_set):>9,}   (== Feb-release test cohort: {len(v2_set & o_sub) == len(o_sub)})")
    print(f"  Apr test      {len(v2_sub):>9,}")


if __name__ == "__main__":
    main()
