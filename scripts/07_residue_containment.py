"""07 - Confirmatory set intersection on the K4 residue. ORIGINAL RELEASE ONLY.

Two sets:
  A = labelled users whose RECONSTRUCTED standing expiry falls outside the
      February window      (the K4 residue, reported as 109,357)
  B = labelled users the reconstruction failed to place in the cohort
      (the reconstruction miss, reported as 111,454)

Interpretation was pre-committed before this ran; see DEVIATIONS.md D-5.

Part 2 splits the intersection before/after the window and compares that split
against the overall out-of-window population. That comparison IS informative
where the containment check may not be, and it tests Observation 4's stated
cancellation hypothesis independently.

transactions.csv with train.csv. Aggregates only, no identifiers.

Run:  python3 07_residue_containment.py
"""

import collections

from common import emit, guard_no_values, path, pct, rows

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
    for r in rows(path("original", "transactions")):
        if r["transaction_date"] <= CUTOFF:
            m = r["msno"]
            prev = keep.get(m)
            if prev is None or comes_after(r, prev):
                keep[m] = {k: r[k] for k in
                           ("transaction_date", "membership_expire_date", "is_cancel",
                            "payment_method_id", "payment_plan_days", "plan_list_price",
                            "is_auto_renew")}

    cand = {m for m, row in keep.items()
            if WIN_LO <= int(row["membership_expire_date"]) <= WIN_HI}
    out_of_window = set(keep) - cand

    A = out_of_window & lab_set          # K4 residue
    B = lab_set - cand                   # reconstruction miss
    inter = A & B

    emit("PART 1 -- CONTAINMENT")
    print(f"  A  K4 residue (labelled, reconstructed expiry outside window) : {len(A):,}")
    print(f"  B  reconstruction miss (labelled, not placed in cohort)       : {len(B):,}")
    print(f"  A n B                                                         : {len(inter):,}")
    print(f"    containment of A in B : {pct(len(inter), len(A)):.4f}%")
    print(f"    containment of B in A : {pct(len(inter), len(B)):.4f}%")
    print(f"    in A only             : {len(A - B):,}")
    print(f"    in B only             : {len(B - A):,}")

    no_history = {m for m in lab_set if m not in keep}
    print(f"\n  B \\ A decomposition:")
    print(f"    labelled users with NO transaction <= {CUTOFF} : {len(no_history):,}")
    print(f"    accounts for B \\ A entirely                    : {no_history == (B - A)}")

    emit("IS THIS TEST CAPABLE OF DISCRIMINATING?")
    print("  A is defined as: labelled AND reconstructed-expiry-outside-window.")
    print("  B is defined as: labelled AND NOT reconstructed-into-cohort.")
    print("  'Not reconstructed into cohort' = expiry outside window OR no history.")
    print("  So A is a subset of B by construction, and B \\ A is exactly the")
    print("  no-history group. Containment of A in B is therefore an IDENTITY,")
    print("  not an empirical result. Verified above rather than assumed:")
    print(f"    A subset of B : {A <= B}")
    print(f"    B \\ A == no-history group : {(B - A) == no_history}")

    emit("PART 2 -- BEFORE/AFTER SPLIT (this comparison IS informative)")
    def split(users, label):
        c = collections.Counter()
        for m in users:
            e = int(keep[m]["membership_expire_date"])
            c["before" if e < WIN_LO else "after"] += 1
        tot = sum(c.values())
        print(f"  {label}  (n={tot:,})")
        for k in ("before", "after"):
            print(f"    expiry {k:<6} the window : {c[k]:>9,}   ({pct(c[k], tot):6.2f}%)")
        return c, tot

    c_all, n_all = split(out_of_window, "ALL out-of-window users (labelled or not)")
    print()
    c_int, n_int = split(inter, "THE INTERSECTION (labelled, out-of-window)")

    print("\n  Enrichment of 'after the window' in the intersection vs the overall")
    print("  out-of-window population:")
    a_all = pct(c_all["after"], n_all)
    a_int = pct(c_int["after"], n_int)
    print(f"    overall      : {a_all:.2f}%")
    print(f"    intersection : {a_int:.2f}%")
    print(f"    ratio        : {a_int / a_all:.2f}x" if a_all else "    ratio: n/a")

    emit("CANCELLATION-STATE OF THE INTERSECTION (Observation 4's hypothesis)")
    cx = sum(1 for m in inter if keep[m]["is_cancel"] == "1")
    print(f"  intersection users whose selected pre-cutoff transaction is a cancel:")
    print(f"    {cx:,}   ({pct(cx, len(inter)):.2f}%)")
    print("  Note: a cancellation occurring AFTER the cutoff cannot appear here,")
    print("  because the selected transaction is drawn from history only. The")
    print("  hypothesis concerns post-cutoff cancellations and is NOT tested by")
    print("  this figure.")

    emit("AGAINST THE NAMED DENOMINATOR")
    print(f"  train.csv denominator            : {len(lab_set):,}")
    print(f"  intersection                     : {len(inter):,}"
          f"   ({pct(len(inter), len(lab_set)):.2f}%)")
    print(f"  non-contained portion of A       : {len(A - B):,}"
          f"   ({pct(len(A - B), len(lab_set)):.4f}%)")
    ch = sum(1 for m in inter if labelled[m] == "1")
    print(f"  of the intersection, labelled churn=1 : {ch:,}   ({pct(ch, len(inter)):.2f}%)")


if __name__ == "__main__":
    main()
