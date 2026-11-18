
from hypothesis import given, strategies as st
from processor import (
    parse_vitals_summary,
    compute_patient_bmi,
    assign_ward_bed
)


@given(st.one_of(st.text(), st.none()))
def test_parse_vitals_summary_no_crash(s):
    try:
        parse_vitals_summary(s)
    except Exception as e:
        assert False, f"Vitals function crashed for input {s!r}: {e}"


@given(st.one_of(st.text(), st.none()))
def test_compute_patient_bmi_safe(s):
    try:
        compute_patient_bmi(s)
    except Exception as e:
        assert False, f"BMI function crashed for input {s!r}: {e}"


@given(st.one_of(st.text(), st.none()))
def test_assign_ward_bed_safe(s):
    try:
        assign_ward_bed(s)
    except Exception as e:
        assert False, f"Ward allocation function crashed for input {s!r}: {e}"

# --------------------------------------------------
# VALID INPUT PROPERTY-BASED TESTS
# --------------------------------------------------

@given(
    hr=st.floats(min_value=30, max_value=250, allow_nan=False, allow_infinity=False),
    spo2=st.floats(min_value=50, max_value=100, allow_nan=False, allow_infinity=False),
    temp=st.floats(min_value=30, max_value=45, allow_nan=False, allow_infinity=False)
)
def test_parse_vitals_valid_inputs(hr, spo2, temp):
    result = parse_vitals_summary(f"{hr},{spo2},{temp}")

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    expected_status = "CRITICAL" if critical else "STABLE"

    assert expected_status in result


@given(
    weight=st.floats(min_value=1, max_value=300, allow_nan=False, allow_infinity=False),
    height=st.floats(min_value=0.5, max_value=2.5, allow_nan=False, allow_infinity=False)
)
def test_compute_patient_bmi_valid_inputs(weight, height):
    result = compute_patient_bmi(f"{weight}/{height}")

    expected_bmi = round(weight / (height ** 2), 2)

    assert result == expected_bmi


@given(
    ward=st.sampled_from(["ER", "ICU", "GEN", "PED"]),
    bed=st.integers(min_value=1, max_value=9999)
)
def test_assign_ward_bed_valid_inputs(ward, bed):
    result = assign_ward_bed(f"{ward}-{bed:02d}")

    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }

    assert result == f"{ward_names[ward]} Bed #{bed}"

# --------------------------------------------------
# TARGETED EDGE-CASE TESTS
# --------------------------------------------------

import pytest


@given(hr=st.integers())
def test_vitals_missing_fields(hr):
    malformed_input = str(hr)

    with pytest.raises(IndexError):
        parse_vitals_summary(malformed_input)


@given(weight=st.floats(
    min_value=1,
    max_value=300,
    allow_nan=False,
    allow_infinity=False
))
def test_bmi_zero_height(weight):
    malformed_input = f"{weight}/0"

    with pytest.raises(ZeroDivisionError):
        compute_patient_bmi(malformed_input)


@given(bed=st.integers(min_value=1, max_value=9999))
def test_unknown_ward(bed):
    malformed_input = f"UNKNOWN-{bed}"

    with pytest.raises(KeyError):
        assign_ward_bed(malformed_input)
