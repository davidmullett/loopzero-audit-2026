"""01 - Structure of the pinned files, per release.

Establishes what is in each file before any question is asked of it:
column names, row counts, date ranges, flag cardinalities, label distribution.

Prints aggregates only. No row values, no msno, ever.

Run:  python3 01_structure.py
"""

import collections

from common import RELEASES, TXN_FIELDS, day_gap, emit, guard_no_values, header, path, pct, rows, to_int


def label_file(release, kind):
    p = path(release, kind)
    cols = header(p)
    n = 0
    dist = collections.Counter()
    for r in rows(p):
        n += 1
        dist[r["is_churn"]] += 1
    print(f"  {RELEASES[release][kind]}")
    print(f"    columns          : {cols}")
    print(f"    rows (excl head) : {n:,}")
    for k in sorted(dist):
        print(f"    is_churn={k:<3}      : {dist[k]:>9,}   ({pct(dist[k], n):.3f}%)")
    return n


def transactions_file(release):
    p = path(release, "transactions")
    cols = header(p)
    n = 0
    users = set()
    txn_min = txn_max = None
    exp_min = exp_max = None
    cancel = collections.Counter()
    autorenew = collections.Counter()
    bad_txn_date = 0
    bad_exp_date = 0
    plan_days = collections.Counter()

    for r in rows(p):
        n += 1
        users.add(r["msno"])
        t = to_int(r["transaction_date"])
        e = to_int(r["membership_expire_date"])
        if t is None:
            bad_txn_date += 1
        else:
            txn_min = t if txn_min is None or t < txn_min else txn_min
            txn_max = t if txn_max is None or t > txn_max else txn_max
        if e is None:
            bad_exp_date += 1
        else:
            exp_min = e if exp_min is None or e < exp_min else exp_min
            exp_max = e if exp_max is None or e > exp_max else exp_max
        cancel[r["is_cancel"]] += 1
        autorenew[r["is_auto_renew"]] += 1
        plan_days[r["payment_plan_days"]] += 1

    print(f"  {RELEASES[release]['transactions']}")
    print(f"    columns              : {cols}")
    print(f"    matches documented   : {cols == TXN_FIELDS}")
    print(f"    rows (excl head)     : {n:,}")
    print(f"    distinct msno        : {len(users):,}")
    print(f"    transaction_date     : {txn_min} .. {txn_max}")
    print(f"    membership_expire    : {exp_min} .. {exp_max}")
    print(f"    unparseable txn_date : {bad_txn_date:,}")
    print(f"    unparseable exp_date : {bad_exp_date:,}")
    for k in sorted(cancel):
        print(f"    is_cancel={k:<3}         : {cancel[k]:>10,}  ({pct(cancel[k], n):.3f}%)")
    for k in sorted(autorenew):
        print(f"    is_auto_renew={k:<3}     : {autorenew[k]:>10,}  ({pct(autorenew[k], n):.3f}%)")
    top = plan_days.most_common(6)
    print(f"    payment_plan_days top6: {[(d, f'{c:,}') for d, c in top]}")
    return {"rows": n, "users": len(users), "txn_max": txn_max, "txn_min": txn_min}


def main():
    guard_no_values()
    summary = {}
    for rel in ("original", "v2"):
        emit(f"RELEASE: {RELEASES[rel]['label']}")
        print("\n LABEL / SUBMISSION FILES")
        n_train = label_file(rel, "train")
        n_sub = label_file(rel, "submission")
        print("\n TRANSACTIONS FILE")
        t = transactions_file(rel)
        summary[rel] = dict(train=n_train, submission=n_sub, **t)

    emit("HORIZON ARITHMETIC (per release, within its own files only)")
    for rel in ("original", "v2"):
        s = summary[rel]
        print(f"  {RELEASES[rel]['label']}")
        print(f"    last transaction_date observed : {s['txn_max']}")
        print(f"    labelled users in cohort       : {s['train']:,}")
        print(f"    users appearing in transactions: {s['users']:,}")
    print("\n  A churn label requires 30 days of observed non-renewal after expiry.")
    print("  The last expiry that can be fully observed within a release's own")
    print("  transactions file is therefore max(transaction_date) - 30 days:")
    for rel in ("original", "v2"):
        s = summary[rel]
        tm = s["txn_max"]
        # walk back 30 days from the last observed transaction date
        from datetime import date, timedelta
        d = date(int(str(tm)[0:4]), int(str(tm)[4:6]), int(str(tm)[6:8])) - timedelta(days=30)
        print(f"    {RELEASES[rel]['label']:<28} : {d.strftime('%Y%m%d')}")


if __name__ == "__main__":
    main()
