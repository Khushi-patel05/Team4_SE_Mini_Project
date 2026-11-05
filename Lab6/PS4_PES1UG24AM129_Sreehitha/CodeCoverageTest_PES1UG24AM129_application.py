import pytest

from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


def test_invalid_wards_input():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)


def test_negative_default_acuity():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_non_accepting_ward_is_skipped():
    result = process_triage_wards(
        [{"is_accepting": False, "patients": [{"spo2": 50}]}],
        10
    )
    assert result == {
        "acuity_score": 0,
        "status": "NO_URGENT_CASES"
    }


def test_default_patient_values():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [{}]}],
        10
    )
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


@pytest.mark.parametrize("patient", [
    {"spo2": 0, "hr": 75},
    {"spo2": 98, "hr": 0},
])
def test_invalid_patient_vitals(patient):
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [patient]}],
        10
    )
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_patient_in_general_ward():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "tier": "general",
            "patients": [{"unconscious": True}]
        }],
        10
    )
    assert result["acuity_score"] == 100
    assert result["status"] == "TRIAGE_STABLE"


def test_unconscious_patient_in_outpatient_ward():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [{"unconscious": True}]
        }],
        10
    )
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_critical_low_oxygen_saturation():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 85, "hr": 75}]
        }],
        10
    )
    assert result["acuity_score"] == 60


def test_critical_high_heart_rate():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 98, "hr": 130}]
        }],
        10
    )
    assert result["acuity_score"] == 60


def test_icu_standby_adds_acuity():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "icu_standby": True,
            "patients": [{"spo2": 98, "hr": 75}]
        }],
        10
    )
    assert result["acuity_score"] == 35


def test_ward_alert_after_more_than_four_flagged_entries():
    patients = [{"spo2": 0, "hr": 75} for _ in range(5)]

    result = process_triage_wards(
        [{"is_accepting": True, "patients": patients}],
        10
    )

    assert result["acuity_score"] == 0
    assert result["status"] == "WARD_ALERT"


def test_empty_patient_list():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": []}],
        10
    )
    assert result["status"] == "NO_URGENT_CASES"


def test_no_oxygen_sensor_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_two_consecutive_low_pressure_readings():
    assert monitor_oxygen_manifolds(
        [[4.5, 3.8, 3.5]]
    ) == "PRESSURE_FAILURE"


def test_single_low_pressure_reading_is_not_failure():
    assert monitor_oxygen_manifolds(
        [[3.5, 4.5, 3.6]]
    ) == "PRESSURE_NORMAL"


def test_pressure_streak_resets_after_recovery():
    assert monitor_oxygen_manifolds(
        [[3.5, 4.2, 3.8, 3.7]]
    ) == "PRESSURE_FAILURE"


def test_multiple_manifolds():
    assert monitor_oxygen_manifolds(
        [[3.5, 4.5], [4.5, 4.6]]
    ) == "PRESSURE_NORMAL"


def test_empty_manifold():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"
