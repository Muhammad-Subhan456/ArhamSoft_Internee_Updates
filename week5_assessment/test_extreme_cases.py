# test_extreme_cases.py
#
# Run with: pytest test_extreme_cases.py -v
#
# This goes well beyond the visible "test_friday_sample.py" (which only
# checks shape/structure). It recomputes the ACTUAL ground truth from the
# exact generation code in the assessment (seed=7 is deterministic), then
# checks your submitted files against that ground truth, plus a set of
# edge cases the hidden suite is likely to probe given what was planted
# in the data:
#   - missing agent_id / channel
#   - exact duplicate rows
#   - negative resolution_hours
#   - the planted 999.0 outliers
#   - inconsistent category casing ("High" vs "high")
#   - dtype correctness in findings.json (plain int, not numpy int64/bool)
#   - whether your "clean" file actually removed the problems
#   - chart file sanity (real images, not empty/corrupt/placeholder)
#
# NOTE on "outliers": the assessment never defines what counts as an
# outlier. Two reasonable readings exist:
#   (a) the 15 rows explicitly forced to 999.0 (the "planted" outliers)
#   (b) anything outside a statistical rule, e.g. IQR fences
# This file checks against (a) as the strict/minimum expectation, and
# also reports (b) as an FYI so you can judge whether your chosen
# definition is defensible. Pick one, state your definition in your
# markdown cell, and be consistent between findings.json and your cleaning.

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


# ---------------------------------------------------------------------------
# Rebuild the exact ground-truth dataset (same code as the assessment spec)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def raw_ground_truth():
    rng = np.random.default_rng(seed=7)
    n = 4000

    tickets = pd.DataFrame({
        "ticket_id": np.arange(1, n + 1),
        "created_at": pd.date_range("2024-03-01", periods=n, freq="30min"),
        "agent_id": rng.integers(200, 260, size=n),
        "priority": rng.choice(["Low", "Medium", "High", "high"], size=n),
        "resolution_hours": rng.gamma(shape=2.0, scale=6.0, size=n).round(2),
        "channel": rng.choice(["Email", "Chat", "Phone", None], size=n, p=[0.35, 0.35, 0.25, 0.05]),
    })

    tickets.loc[rng.choice(n, 120, replace=False), "agent_id"] = None
    tickets.loc[rng.choice(n, 25, replace=False), "resolution_hours"] *= -1
    tickets.loc[rng.choice(n, 15, replace=False), "resolution_hours"] = 999.0
    tickets = pd.concat([tickets, tickets.sample(12, random_state=3)])
    return tickets


@pytest.fixture(scope="module")
def ground_truth_findings(raw_ground_truth):
    df = raw_ground_truth
    return {
        "missing_agent_id": int(df["agent_id"].isna().sum()),
        "missing_channel": int(df["channel"].isna().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "negative_resolution_hours": int((df["resolution_hours"] < 0).sum()),
        # strict/planted definition:
        "outlier_resolution_hours_planted": int((df["resolution_hours"] == 999.0).sum()),
    }


# ---------------------------------------------------------------------------
# Structural sanity on YOUR generated raw data (catches "I edited the setup
# code" or "I ran it with a different seed/pandas version" problems early)
# ---------------------------------------------------------------------------

def test_raw_shape_matches_spec(raw_ground_truth):
    assert raw_ground_truth.shape == (4012, 6)


def test_raw_columns_match_spec(raw_ground_truth):
    assert list(raw_ground_truth.columns) == [
        "ticket_id", "created_at", "agent_id", "priority",
        "resolution_hours", "channel",
    ]


# ---------------------------------------------------------------------------
# findings.json — existence, keys, TYPES, and correctness vs ground truth
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def findings():
    p = Path("findings.json")
    assert p.exists(), "findings.json is missing"
    return json.loads(p.read_text())


REQUIRED_KEYS = {
    "missing_agent_id", "missing_channel", "duplicate_rows",
    "negative_resolution_hours", "outlier_resolution_hours",
}


def test_findings_has_all_required_keys(findings):
    missing = REQUIRED_KEYS - findings.keys()
    assert not missing, f"findings.json missing keys: {missing}"


def test_findings_values_are_strict_python_int(findings):
    # json.load never produces numpy types, but this catches the common
    # mistake of someone hand-editing the file with floats like 120.0,
    # or booleans, or strings like "120".
    for k in REQUIRED_KEYS:
        v = findings[k]
        assert isinstance(v, int) and not isinstance(v, bool), (
            f"{k} = {v!r} ({type(v).__name__}) is not a plain int"
        )


def test_findings_values_are_non_negative(findings):
    for k in REQUIRED_KEYS:
        assert findings[k] >= 0, f"{k} is negative: {findings[k]}"


@pytest.mark.parametrize("key,truth_key", [
    ("missing_agent_id", "missing_agent_id"),
    ("missing_channel", "missing_channel"),
    ("duplicate_rows", "duplicate_rows"),
    ("negative_resolution_hours", "negative_resolution_hours"),
])
def test_findings_matches_ground_truth(findings, ground_truth_findings, key, truth_key):
    assert findings[key] == ground_truth_findings[truth_key], (
        f"{key}: you reported {findings[key]}, actual is {ground_truth_findings[truth_key]}"
    )


def test_outlier_count_is_at_least_the_planted_ones(findings, ground_truth_findings):
    # We can't force one single "correct" outlier definition, but whatever
    # method you used should catch AT LEAST the 15 rows deliberately set
    # to 999.0 -- if your number is smaller than that, your detection
    # logic missed the planted outliers.
    planted = ground_truth_findings["outlier_resolution_hours_planted"]
    assert findings["outlier_resolution_hours"] >= planted, (
        f"outlier_resolution_hours = {findings['outlier_resolution_hours']} is less than "
        f"the {planted} rows deliberately forced to 999.0 -- your outlier logic likely "
        f"missed some of the planted extreme values"
    )


# ---------------------------------------------------------------------------
# tickets_clean.csv — did cleaning actually fix what findings.json diagnosed?
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def clean_df():
    p = Path("tickets_clean.csv")
    assert p.exists(), "tickets_clean.csv is missing"
    return pd.read_csv(p)


def test_clean_has_required_columns(clean_df):
    required = {"ticket_id", "created_at", "agent_id", "priority", "resolution_hours", "channel"}
    assert required <= set(clean_df.columns)


def test_clean_is_not_empty(clean_df):
    assert len(clean_df) > 0
    # sanity: dropping everything is not "cleaning"
    assert len(clean_df) > 100


def test_clean_has_no_exact_duplicate_rows(clean_df):
    dupes = clean_df.duplicated().sum()
    assert dupes == 0, f"{dupes} exact duplicate rows remain in tickets_clean.csv"


def test_clean_has_no_negative_resolution_hours(clean_df):
    neg = (clean_df["resolution_hours"] < 0).sum()
    assert neg == 0, f"{neg} negative resolution_hours remain in tickets_clean.csv"


def test_clean_has_no_999_outliers(clean_df):
    # If your strategy was "cap/winsorize" instead of "drop", this specific
    # check will fail even though your approach may be defensible -- that's
    # fine, just make sure your markdown justification says so explicitly
    # and that no *unexplained* 999.0 values remain.
    n999 = (clean_df["resolution_hours"] == 999.0).sum()
    assert n999 == 0, (
        f"{n999} rows still have resolution_hours == 999.0. If you intentionally "
        f"capped rather than removed them, make sure this is justified in your "
        f"notebook and that the capped value isn't still literally 999.0."
    )


def test_clean_resolution_hours_are_finite(clean_df):
    bad = (~np.isfinite(clean_df["resolution_hours"])).sum()
    assert bad == 0, f"{bad} non-finite (NaN/inf) resolution_hours values remain"


def test_clean_priority_categories_are_consistent(clean_df):
    # The raw data has both "High" and "high" as separate category strings.
    # A properly cleaned categorical column should not have case-variant
    # duplicates of the same logical category.
    cats = set(clean_df["priority"].dropna().astype(str))
    lowered = {c.lower() for c in cats}
    collisions = {c for c in cats if sum(1 for o in cats if o.lower() == c.lower()) > 1}
    assert not collisions, (
        f"priority column still has case-inconsistent duplicate categories: {collisions} "
        f"(e.g. both 'High' and 'high' present) -- these should be normalized to one form"
    )


def test_clean_agent_id_missing_handled(clean_df):
    # Either they were dropped (no NaNs remain) or filled (no NaNs remain
    # but a real fill value does) -- either way, no NaNs should remain
    # UNLESS the notebook's justification explicitly argues for leaving
    # them as a legitimate missing-data category. We treat unhandled NaNs
    # as a likely miss since agent_id is an ID field.
    remaining = clean_df["agent_id"].isna().sum()
    assert remaining == 0, (
        f"{remaining} missing agent_id values remain unhandled in tickets_clean.csv"
    )


def test_clean_row_count_is_plausible(clean_df, ground_truth_findings):
    # Loose sanity check: you shouldn't have MORE rows than the raw data
    # (4012), and you shouldn't have dropped so much that you removed
    # far more than the planted problems could account for.
    assert len(clean_df) <= 4012, "tickets_clean.csv has more rows than the raw dataset -- did dedup logic go wrong?"
    max_reasonable_drop = (
        ground_truth_findings["duplicate_rows"]
        + ground_truth_findings["negative_resolution_hours"]
        + ground_truth_findings["outlier_resolution_hours_planted"]
        + ground_truth_findings["missing_agent_id"]
    )
    min_expected_rows = 4012 - max_reasonable_drop
    assert len(clean_df) >= min_expected_rows - 5, (  # small slack for edge overlap
        f"tickets_clean.csv has only {len(clean_df)} rows -- that's more aggressive "
        f"dropping than the planted problems account for ({min_expected_rows} expected "
        f"as a floor). Did dropna() get called without a subset= and wipe out rows "
        f"for unrelated missing 'channel' values too?"
    )


# ---------------------------------------------------------------------------
# Chart files — existence, non-triviality, actually-an-image checks
# ---------------------------------------------------------------------------

CHART_FILES = ["chart_distribution.png", "chart_category_comparison.png", "chart_relationship.png"]


@pytest.mark.parametrize("filename", CHART_FILES)
def test_chart_exists_and_nontrivial_size(filename):
    p = Path(filename)
    assert p.exists(), f"{filename} is missing"
    size = p.stat().st_size
    assert size > 1000, f"{filename} is only {size} bytes -- likely a blank/empty figure"


@pytest.mark.parametrize("filename", CHART_FILES)
def test_chart_is_valid_png_with_real_dimensions(filename):
    p = Path(filename)
    if not p.exists():
        pytest.skip(f"{filename} missing, covered by other test")
    with open(p, "rb") as f:
        header = f.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n", f"{filename} does not have a valid PNG signature"
    # Width/height are big-endian uint32 at bytes 16-20 / 20-24 in an IHDR-first PNG
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    assert width >= 200 and height >= 150, (
        f"{filename} dimensions look too small ({width}x{height}) -- "
        f"check figsize and that savefig wasn't called on an empty/default Figure"
    )


def test_chart_files_are_distinct(tmp_path=None):
    # Catches the classic mistake of saving the same figure three times
    # under different filenames (e.g. forgetting to call plt.subplots()
    # again, or saving 'fig' before it was updated).
    hashes = set()
    import hashlib
    for filename in CHART_FILES:
        p = Path(filename)
        if not p.exists():
            continue
        h = hashlib.md5(p.read_bytes()).hexdigest()
        assert h not in hashes, (
            f"{filename} is byte-identical to another chart file -- "
            f"looks like the same figure was saved twice instead of three distinct charts"
        )
        hashes.add(h)


# ---------------------------------------------------------------------------
# Cross-file consistency
# ---------------------------------------------------------------------------

def test_findings_and_clean_csv_are_mutually_consistent(findings, clean_df, ground_truth_findings):
    # If findings.json says N duplicate rows and M negative-hour rows were
    # diagnosed, tickets_clean.csv should reflect having addressed at
    # least that many problem rows (loose check, not exact, since fillna
    # vs dropna change the arithmetic differently).
    if findings["duplicate_rows"] > 0:
        assert clean_df.duplicated().sum() == 0, (
            "findings.json diagnosed duplicate rows but tickets_clean.csv still has some"
        )
    if findings["negative_resolution_hours"] > 0:
        assert (clean_df["resolution_hours"] < 0).sum() == 0, (
            "findings.json diagnosed negative resolution_hours but tickets_clean.csv still has some"
        )


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
