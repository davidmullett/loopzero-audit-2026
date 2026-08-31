"""03 - Reconstruct the cohort-selection rule, ORIGINAL RELEASE ONLY.

Implements the ordering and selection in WSDMChurnLabeller.scala (in scope per
the 27 Aug ruling; provenance caveat in DEVIATIONS.md D-3):

    historyData        = transactions up to the cutoff
    last_expire        = membership_expire_date of the LAST history transaction
                         under the script's comparator
    predictionCandidate= 20170201 <= last_expire <= 20170228
    futureData         = transaction_date > 20170131
    label              : no future transaction        -> churn
                         first non-cancel txn gap <30 -> not churn
                         gap >= 30                    -> churn

TWO READINGS OF "historyData", run side by side and reported both ways.
The script as distributed filters history to transaction_date >= 20170101. But
the data page states: "Note that the date values in the script is modified so it
is easier to run on personal laptops." So the January-only bound is a
laptop-friendly modification, not necessarily the production rule. Reading A
applies the literal script; Reading B uses all history up to the cutoff. Each is
checked against the actual train.csv membership rather than assumed.

Uses transactions.csv with train.csv -- one release, no mixing.
Prints aggregates only.

Run:  python3 03_cohort_rule.py
"""

import collections

from common import day_gap, emit, guard_no_values, path, pct, rows

CUTOFF = "20170131"
WIN_LO, WIN_HI = 20170201, 20170228
HORIZON = "20170228"          # last transaction_date in this release's own file


def sig(row):
    return row["plan_list_price"] + row["payment_plan_days"] + row["payment_method_id"]


def comes_after(a, b):
    """True if `a` sorts after `b` under calculateLastday's comparator."""
    if a["transaction_date"] != b["transaction_date"]:
        return a["transaction_date"] > b["transaction_date"]
    sa, sb = sig(a), sig(b)
    if sa != sb:
        return sa < sb                      # descending by signature
    ac, bc = a["is_cancel"], b["is_cancel"]
    if ac == "1" and bc == "1":
        return a["membership_expire_date"] < b["membership_expire_date"]
    if ac == "0" and bc == "0":
        return a["membership_expire_date"] > b["membership_expire_date"]
    return ac > bc                          # subscription precedes cancellation


def scan(history_from):
    """One pass. history_from=None means 'all history up to CUTOFF'."""
    keep, future = {}, {}
    for r in rows(path("original", "transactions")):
        td = r["transaction_date"]
        m = r["msno"]
        if td <= CUTOFF and (history_from is None or td >= history_from):
            prev = keep.get(m)
            if prev is None or comes_after(r, prev):
                keep[m] = {k: r[k] for k in
                           ("transaction_date", "membership_expire_date", "is_cancel",
                            "payment_method_id", "payment_plan_days", "plan_list_price",
                            "is_auto_renew")}
        elif td > CUTOFF:
            rec = future.setdefault(m, {"any": 0, "first_renewal": None})
            rec["any"] += 1
            if r["is_cancel"] == "0":
                cur = rec["first_renewal"]
                if cur is None or td < cur:
                    rec["first_renewal"] = td
    return keep, future


def main():
    guard_no_values()

    labelled = {r["msno"]: r["is_churn"] for r in rows(path("original", "train"))}
    lab_set = set(labelled)

    results = {}
    for name, hf in (("A - literal script (history >= 20170101)", "20170101"),
                     ("B - all history up to cutoff", None)):
        keep, future = scan(hf)
        cand = {m for m, row in keep.items()
                if WIN_LO <= int(row["membership_expire_date"]) <= WIN_HI}
        inter = cand & lab_set
        emit(f"READING {name}")
        print(f"  users with qualifying history       : {len(keep):,}")
        print(f"  last_expire inside Feb-2017 window  : {len(cand):,}")
        print(f"  train.csv (the denominator)         : {len(lab_set):,}")
        print(f"  CHECK vs actual label file:")
        print(f"    matched                           : {len(inter):,}"
              f"   ({pct(len(inter), len(lab_set)):.2f}% of train.csv)")
        print(f"    reconstructed but not labelled    : {len(cand - lab_set):,}")
        print(f"    labelled but not reconstructed    : {len(lab_set - cand):,}")
        results[name] = (keep, future, cand, inter)

    # everything downstream uses the better-matching reading
    best = max(results, key=lambda k: len(results[k][3]))
    keep, future, cand, inter = results[best]
    emit(f"DOWNSTREAM COUNTS USE READING: {best}")

    emit("K4 -- OUT-OF-WINDOW EXPIRATIONS: EXCLUDED, OR RETAINED AS NON-CHURNED?")
    everyone = set(keep)
    out_of_window = everyone - cand
    print(f"  users with history up to the cutoff   : {len(everyone):,}")
    print(f"    last_expire INSIDE  the window      : {len(cand):,}"
          f"   ({pct(len(cand), len(everyone)):.2f}%)")
    print(f"    last_expire OUTSIDE the window      : {len(out_of_window):,}"
          f"   ({pct(len(out_of_window), len(everyone)):.2f}%)")
    print(f"  do the OUTSIDE users appear in the denominator (train.csv)?")
    inside_denom = out_of_window & lab_set
    print(f"    present in train.csv                : {len(inside_denom):,}"
          f"   ({pct(len(inside_denom), len(out_of_window)):.4f}%)")
    print(f"    absent from train.csv               : {len(out_of_window - lab_set):,}"
          f"   ({pct(len(out_of_window - lab_set), len(out_of_window)):.4f}%)")
    if inside_denom:
        ch = sum(1 for m in inside_denom if labelled[m] == "1")
        print(f"    of those present, labelled churn=1  : {ch:,}"
              f"   ({pct(ch, len(inside_denom)):.2f}%)")
    buck = collections.Counter()
    for m in out_of_window:
        e = int(keep[m]["membership_expire_date"])
        buck["before window (<20170201)" if e < WIN_LO else "after window (>20170228)"] += 1
    print("  where the out-of-window expiries fall:")
    for k in sorted(buck):
        print(f"    {k:<32} {buck[k]:>9,}   ({pct(buck[k], len(out_of_window)):.2f}%)")

    emit("K6 -- CHURN RATE BY EXPIRY DAY WITHIN THE WINDOW")
    print(f"  This release's own transactions file ends {HORIZON}. A 30-day")
    print("  non-renewal test on a February expiry needs data through 20170330.\n")
    print("   expiry_day   labelled    churn=1    churn rate")
    by_day = collections.defaultdict(lambda: [0, 0])
    for m in inter:
        d = int(keep[m]["membership_expire_date"]) % 100
        by_day[d][0] += 1
        if labelled[m] == "1":
            by_day[d][1] += 1
    for d in sorted(by_day):
        tot, ch = by_day[d]
        print(f"   {d:>10}   {tot:>8,}   {ch:>8,}    {pct(ch, tot):6.2f}%")

    emit("K1 / K6 -- CAN THE 30-DAY TEST BE OBSERVED INSIDE THIS RELEASE?")
    fully = sum(1 for m in inter
                if (g := day_gap(keep[m]["membership_expire_date"], HORIZON)) is not None
                and g >= 30)
    no_future = sum(1 for m in inter if future.get(m) is None)
    tot = len(inter)
    print(f"  labelled users in cohort                    : {tot:,}")
    print(f"    30-day window fully inside this file       : {fully:,}"
          f"   ({pct(fully, tot):.2f}%)")
    print(f"    30-day window extends past {HORIZON}        : {tot - fully:,}"
          f"   ({pct(tot - fully, tot):.2f}%)")
    print(f"    no transaction at all after the cutoff     : {no_future:,}"
          f"   ({pct(no_future, tot):.2f}%)")

    emit("K1 -- PERSISTENCE: DO USERS KEEP TRANSACTING AFTER THE CUTOFF?")
    print("  Tested against transactions, not listening logs: the pathology is")
    print("  about subscription state, so continued transacting is the apposite")
    print("  signal. Counts are within this release's own file only.\n")
    for lab in ("0", "1"):
        grp = [m for m in inter if labelled[m] == lab]
        with_txn = sum(1 for m in grp if future.get(m))
        print(f"    labelled is_churn={lab}: {len(grp):>9,} users, "
              f"{with_txn:>9,} with a post-cutoff transaction "
              f"({pct(with_txn, len(grp)):.2f}%)")


if __name__ == "__main__":
    main()
