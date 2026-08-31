"""06 - K6, the window edge. ORIGINAL RELEASE ONLY.

For each expiry day inside the Feb-2017 window, cross-tabulates:
  - cohort size and churn rate
  - days of post-expiry observation available inside THIS release's file
  - auto-renew share and cancelled share at the selected history transaction

The auto-renew and cancel columns are there to test the obvious confound before
any correspondence is reported: month-end expiries are heavily concentrated, and
if they were also disproportionately auto-renewing, a lower churn rate at the
edge would have a mundane explanation. Testing it is cheaper than being wrong.

transactions.csv with train.csv. No mixing across releases.
Prints aggregates only.

Run:  python3 06_window_edge.py
"""

import collections

from common import day_gap, emit, guard_no_values, path, pct, rows

CUTOFF = "20170131"
WIN_LO, WIN_HI = 20170201, 20170228
HORIZON = "20170228"


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
    keep = {}
    for r in rows(path("original", "transactions")):
        if r["transaction_date"] <= CUTOFF:
            m = r["msno"]
            prev = keep.get(m)
            if prev is None or comes_after(r, prev):
                keep[m] = {k: r[k] for k in
                           ("transaction_date", "membership_expire_date", "is_cancel",
                            "payment_method_id", "payment_plan_days", "plan_list_price",
                            "is_auto_renew")}

    cohort = [m for m, row in keep.items()
              if WIN_LO <= int(row["membership_expire_date"]) <= WIN_HI and m in labelled]

    emit("K6 -- EXPIRY DAY vs OBSERVABILITY vs LABEL (original release)")
    print(f"  cohort (reconstructed and labelled): {len(cohort):,}")
    print(f"  this release's transactions end    : {HORIZON}\n")
    print("   day   obs_days     users    churn=1   churn_rate   auto_renew   cancelled")
    stat = collections.defaultdict(lambda: [0, 0, 0, 0])
    for m in cohort:
        row = keep[m]
        d = int(row["membership_expire_date"]) % 100
        s = stat[d]
        s[0] += 1
        if labelled[m] == "1":
            s[1] += 1
        if row["is_auto_renew"] == "1":
            s[2] += 1
        if row["is_cancel"] == "1":
            s[3] += 1
    for d in sorted(stat):
        tot, ch, ar, cx = stat[d]
        obs = day_gap(f"201702{d:02d}", HORIZON)
        print(f"   {d:>3}   {obs:>8}   {tot:>7,}   {ch:>8,}    {pct(ch, tot):7.2f}%"
              f"     {pct(ar, tot):7.2f}%   {pct(cx, tot):7.2f}%")

    emit("K6 -- GROUPED BY WHETHER THE 30-DAY TEST FITS INSIDE THE FILE")
    groups = collections.defaultdict(lambda: [0, 0, 0])
    for m in cohort:
        row = keep[m]
        obs = day_gap(row["membership_expire_date"], HORIZON)
        key = ("30+ days observable" if obs is not None and obs >= 30 else
               "15-29 days observable" if obs is not None and obs >= 15 else
               "1-14 days observable" if obs is not None and obs >= 1 else
               "0 days observable (expiry on or after file end)")
        g = groups[key]
        g[0] += 1
        if labelled[m] == "1":
            g[1] += 1
        if row["is_auto_renew"] == "1":
            g[2] += 1
    order = ["30+ days observable", "15-29 days observable", "1-14 days observable",
             "0 days observable (expiry on or after file end)"]
    print("   group                                             users   churn_rate  auto_renew")
    for k in order:
        if k in groups:
            tot, ch, ar = groups[k]
            print(f"   {k:<46} {tot:>8,}    {pct(ch, tot):7.2f}%    {pct(ar, tot):6.2f}%")

    emit("K6 -- THE LAST DAY OF THE WINDOW, ISOLATED")
    last = [m for m in cohort if int(keep[m]["membership_expire_date"]) == WIN_HI]
    rest = [m for m in cohort if int(keep[m]["membership_expire_date"]) != WIN_HI]
    for name, grp in (("expiry == 20170228 (window close)", last),
                      ("expiry 20170201-20170227", rest)):
        tot = len(grp)
        ch = sum(1 for m in grp if labelled[m] == "1")
        ar = sum(1 for m in grp if keep[m]["is_auto_renew"] == "1")
        cx = sum(1 for m in grp if keep[m]["is_cancel"] == "1")
        print(f"  {name}")
        print(f"    users        {tot:>9,}   ({pct(tot, len(cohort)):.2f}% of the cohort)")
        print(f"    churn=1      {ch:>9,}   rate {pct(ch, tot):.2f}%")
        print(f"    auto_renew   {ar:>9,}   {pct(ar, tot):.2f}%")
        print(f"    cancelled    {cx:>9,}   {pct(cx, tot):.2f}%")
    print("\n  Materiality reference: the frozen plan fixes 5% of labelled users in")
    print("  the observation window as the threshold. Denominator here is the")
    print(f"  labelled cohort, {len(labelled):,} users in train.csv.")
    print(f"  expiry-on-window-close as a share of that denominator: "
          f"{pct(len(last), len(labelled)):.2f}%")


if __name__ == "__main__":
    main()
