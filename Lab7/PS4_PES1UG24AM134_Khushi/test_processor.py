
from hypothesis import given, strategies as st

from processor import (
    parse_storage_quota,
    compute_compression_ratio,
    lookup_bandwidth_tier_rate
)


# ==================================================
# 1. FUZZ TESTING - STORAGE QUOTA
# ==================================================

@given(s=st.one_of(st.text(), st.none()))
def test_parse_storage_quota_no_crash(s):
    try:
        result = parse_storage_quota(s)

        assert isinstance(result, str)
        assert result.startswith("Quota:")

    except (ValueError, TypeError, AttributeError):
        pass


# ==================================================
# 2. FUZZ TESTING - COMPRESSION RATIO
# ==================================================

@given(s=st.one_of(st.text(), st.none()))
def test_compute_compression_ratio_safe(s):
    try:
        result = compute_compression_ratio(s)

        assert isinstance(result, float)
        assert result >= 0

    except (ValueError, TypeError, AttributeError,
            ZeroDivisionError, OverflowError):
        pass


# ==================================================
# 3. FUZZ TESTING - BANDWIDTH TIER
# ==================================================

@given(s=st.one_of(st.text(), st.none()))
def test_lookup_bandwidth_tier_rate_safe(s):
    try:
        result = lookup_bandwidth_tier_rate(s)

        assert result in (0.08, 0.05, 0.02)

    except (ValueError, TypeError, AttributeError):
        pass


# ==================================================
# 4. PROPERTY TESTING - STORAGE QUOTA
# ==================================================

@given(
    value=st.integers(min_value=0, max_value=100000),
    unit=st.sampled_from(["MB", "GB", "TB"])
)
def test_storage_quota_valid_values(value, unit):

    result = parse_storage_quota(f"{value}{unit}")

    multipliers = {
        "MB": 0.001,
        "GB": 1.0,
        "TB": 1000.0
    }

    expected = value * multipliers[unit]

    assert result == f"Quota: {expected:.2f} GB"


# ==================================================
# 5. PROPERTY TESTING - COMPRESSION RATIO
# ==================================================

@given(
    raw=st.floats(
        min_value=0,
        max_value=1000000,
        allow_nan=False,
        allow_infinity=False
    ),
    compressed=st.floats(
        min_value=0.01,
        max_value=1000000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_compression_ratio_valid_values(raw, compressed):

    result = compute_compression_ratio(
        f"{raw}:{compressed}"
    )

    expected = round(raw / compressed, 2)

    assert result == expected


# ==================================================
# 6. PROPERTY TESTING - BANDWIDTH TIER
# ==================================================

@given(
    tier=st.sampled_from([
        "HOT",
        "HOT_TIER",
        "hot",
        "COLD",
        "COLD_TIER",
        "cold",
        "ARCHIVE",
        "ARCHIVE_TIER",
        "archive"
    ])
)
def test_bandwidth_tier_valid_values(tier):

    result = lookup_bandwidth_tier_rate(tier)

    expected = {
        "HOT": 0.08,
        "COL": 0.05,
        "ARC": 0.02
    }

    prefix = tier.strip().upper()[:3]

    assert result == expected[prefix]
