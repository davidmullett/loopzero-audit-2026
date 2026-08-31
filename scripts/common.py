"""Shared helpers for the KKBox read.

Published under the terms of Kaggle competition rules 8.B (public code sharing).
The DATA is not published and never enters this repository: rules 7.B forbids
redistribution, and 7.B further obliges reasonable measures preventing access by
parties who have not accepted the rules.

Operational consequence, and the reason these helpers exist in this shape:
NOTHING IN HERE MAY PRINT A ROW. Every function returns or prints aggregates
only -- counts, shares, distributions, min/max of a column. Column names and
dtypes may be shown; values may not. `msno` is never printed under any
circumstance.

Anyone who has accepted the competition rules can point DATA_ROOT at their own
copy and reproduce every number in KKBOX-ANSWERS.md. That is how reproducibility
survives a licence that forbids publishing the data.

Python 3 standard library only, by design -- no dependency stack to install.
"""

import csv
import os
import sys

# The data lives on an external volume, never in the repository.
DATA_ROOT = os.environ.get("KKBOX_DATA", "/Volumes/MULLETT_T7/kkbox-wsdm2017")

# The two pinned releases, per R1' in EXECUTION-LOG.md.
# Files are never mixed across releases within a single answer.
RELEASES = {
    "original": {
        "label": "original release (Sep 2017)",
        "train": "train.csv",
        "submission": "sample_submission_zero.csv",
        "transactions": "transactions.csv",
    },
    "v2": {
        "label": "_v2 refresh (6 Nov 2017)",
        "train": "data/churn_comp_refresh/train_v2.csv",
        "submission": "data/churn_comp_refresh/sample_submission_v2.csv",
        "transactions": "data/churn_comp_refresh/transactions_v2.csv",
    },
}

# Field order in the transactions files, per the competition data description.
TXN_FIELDS = [
    "msno",
    "payment_method_id",
    "payment_plan_days",
    "plan_list_price",
    "actual_amount_paid",
    "is_auto_renew",
    "transaction_date",
    "membership_expire_date",
    "is_cancel",
]


def path(release, kind):
    return os.path.join(DATA_ROOT, RELEASES[release][kind])


def rows(filepath):
    """Stream a CSV as dicts. Constant memory; nothing is accumulated here."""
    with open(filepath, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            yield row


def header(filepath):
    with open(filepath, newline="") as fh:
        return next(csv.reader(fh))


def to_int(value):
    """Dates and flags arrive as strings. Returns None on anything unparseable,
    so malformed values are counted rather than silently coerced."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def day_gap(from_yyyymmdd, to_yyyymmdd):
    """Whole days between two %Y%m%d integers, via the proleptic Gregorian
    ordinal. Returns None if either date is unparseable or out of range."""
    from datetime import date

    def parse(n):
        try:
            s = str(n)
            return date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
        except (ValueError, IndexError):
            return None

    a, b = parse(from_yyyymmdd), parse(to_yyyymmdd)
    if a is None or b is None:
        return None
    return (b - a).days


def pct(numerator, denominator):
    return 0.0 if not denominator else 100.0 * numerator / denominator


def emit(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def guard_no_values():
    """Standing reminder at the top of every script's output."""
    print("(aggregates only -- no row values are printed by these scripts)",
          file=sys.stderr)
