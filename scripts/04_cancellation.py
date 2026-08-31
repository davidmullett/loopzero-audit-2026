"""04 - K2 (the cancellation clause) and a diagnostic on the reconstruction gap.

ORIGINAL RELEASE ONLY. transactions.csv with train.csv; no mixing.

Part 1 characterises the 111,454 users who carry a label in train.csv but whom
the reconstruction in 03 does not select. The reconstruction matched 88.78%, and
a count that rests on a model is only as good as the account of where the model
misses. This is that account.

Part 2 answers K2: a user who has actively cancelled but whose membership has
not yet expired -- counted as retained, and for how long?

Prints aggregates only.

Run:  python3 04_cancellation.py
"""

import collections

from common import day_gap, emit, guard_no_values, path, pct, rows

CUTOFF = "20170131"
WIN_LO, WIN_HI = 20170201, 20170228


def sig(row):
    return row["plan_list_price"] + row["payment_plan_days"] + row["payment_method_id"]


def comes_after(a, b):
    if a["transaction_date"] != b["transaction_date"]:
        return a["transaction_date"] > b["transaction_date"]
    sa, sb = sig(a), sig(b)
    if sa != sb:
        return sa < sb
    ac, bc = a["is_cancel"], b["is_cancel"]
    if ac == "1" and bc == "1":
        return a["membership_expire_date"] < b["membership_expire_date"]
    if ac == "0" and bc == "0":
        return a["membership_expire_date"] > b["membership_expire_date"]
    return ac > bc


def main():
    guard_no_values()

    labelled = {r["msno"]: r["is_churn"] for r in rows(path("original", "train"))}
    lab_set = set(labelled)

    keep = {}
    cancel_gap = collections.Counter()      # days from cancel txn to its expiry
    cancel_future_dated = 0
    cancel_rows = 0
    cancel_users = set()
    seen_any = set()

    for r in rows(path("original", "transactions")):
        m = r["msno"]
        td = r["transaction_date"]
        seen_any.add(m)
        if r["is_cancel"] == "1":
            cancel_rows += 1
            cancel_users.add(m)
            g = day_gap(td, r["membership_expire_date"])
            if g is not None:
                if g > 0:
                    cancel_future_dated += 1
                bucket = ("negative (expiry moved before the cancel txn)" if g < 0 else
                          "same day" if g == 0 else
                          "1-7 days" if g <= 7 else
                          "8-30 days" if g <= 30 else
                          "31-90 days" if g <= 90 else
                          "over 90 days")
                cancel_gap[bucket] += 1
        if td <= CUTOFF:
            prev = keep.get(m)
            if prev is None or comes_after(r, prev):
                keep[m] = {k: r[k] for k in
                           ("transaction_date", "membership_expire_date", "is_cancel",
                            "payment_method_id", "payment_plan_days", "plan_list_price",
                            "is_auto_renew")}

    cand = {m for m, row in keep.items()
            if WIN_LO <= int(row["membership_expire_date"]) <= WIN_HI}
    missed = lab_set - cand

    emit("PART 1 -- WHERE THE RECONSTRUCTION MISSES (diagnostic, not a finding)")
    print(f"  labelled users                        : {len(lab_set):,}")
    print(f"  reconstructed as candidates           : {len(cand):,}")
    print(f"  labelled but NOT reconstructed        : {len(missed):,}"
          f"   ({pct(len(missed), len(lab_set)):.2f}% of the denominator)")
    no_history = sum(1 for m in missed if m not in keep)
    print(f"    of those, no transaction <= {CUTOFF} : {no_history:,}"
          f"   ({pct(no_history, len(missed)):.2f}%)")
    where = collections.Counter()
    for m in missed:
        row = keep.get(m)
        if row is None:
            where["no history before cutoff"] += 1
            continue
        e = int(row["membership_expire_date"])
        where["expiry before the window" if e < WIN_LO else
              "expiry after the window" if e > WIN_HI else
              "in window (should not occur)"] += 1
    for k, v in where.most_common():
        print(f"    {k:<34} {v:>8,}   ({pct(v, len(missed)):.2f}%)")
    ch = sum(1 for m in missed if labelled[m] == "1")
    print(f"  churn rate among the missed users      : {pct(ch, len(missed)):.2f}%"
          f"   (vs {pct(sum(1 for m in lab_set if labelled[m] == '1'), len(lab_set)):.2f}% overall)")

    emit("PART 2 -- K2: THE CANCELLATION CLAUSE")
    print(f"  transactions with is_cancel=1          : {cancel_rows:,}")
    print(f"  distinct users ever cancelling         : {len(cancel_users):,}"
          f"   ({pct(len(cancel_users), len(seen_any)):.2f}% of all users in the file)")
    print(f"  cancel rows whose expiry is LATER than the cancel transaction:")
    print(f"    {cancel_future_dated:,}   ({pct(cancel_future_dated, cancel_rows):.2f}% of cancel rows)")
    print("\n  gap from the cancel transaction to the membership expiry it records:")
    order = ["negative (expiry moved before the cancel txn)", "same day", "1-7 days",
             "8-30 days", "31-90 days", "over 90 days"]
    for k in order:
        if k in cancel_gap:
            print(f"    {k:<46} {cancel_gap[k]:>9,}   ({pct(cancel_gap[k], cancel_rows):.2f}%)")

    emit("K2 -- COHORT USERS WHOSE SELECTED HISTORY TRANSACTION IS A CANCELLATION")
    inter = cand & lab_set
    cancel_state = [m for m in inter if keep[m]["is_cancel"] == "1"]
    active_state = [m for m in inter if keep[m]["is_cancel"] == "0"]
    print(f"  cohort users (reconstructed & labelled) : {len(inter):,}")
    for name, grp in (("last state = CANCELLED", cancel_state),
                      ("last state = active", active_state)):
        if not grp:
            continue
        ch = sum(1 for m in grp if labelled[m] == "1")
        print(f"    {name:<26} {len(grp):>8,}  churn={ch:>7,}  rate {pct(ch, len(grp)):6.2f}%")
    print("\n  For the cancelled group, how long does membership still run past the")
    print("  cancellation? (days from the cancel transaction to the recorded expiry)")
    dist = collections.Counter()
    for m in cancel_state:
        g = day_gap(keep[m]["transaction_date"], keep[m]["membership_expire_date"])
        if g is None:
            dist["unparseable"] += 1
        else:
            dist["negative" if g < 0 else "0" if g == 0 else "1-7" if g <= 7 else
                 "8-30" if g <= 30 else "31+"] += 1
    for k in ("negative", "0", "1-7", "8-30", "31+", "unparseable"):
        if k in dist:
            print(f"    {k:<12} {dist[k]:>8,}   ({pct(dist[k], len(cancel_state)):.2f}%)")


if __name__ == "__main__":
    main()
