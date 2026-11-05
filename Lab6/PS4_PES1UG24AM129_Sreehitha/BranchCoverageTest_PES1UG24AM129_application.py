import pytest

from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


# Input validation branches
def test_non_list_wards():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)


def test_negative_acuity_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_empty_wards_list():
    result = process_triage_wards([], 10)
    assert result["status"] == "NO_URGENT_CASES"


# Ward acceptance and iteration branches
def test_ward_not_accepting():
    result = process_triage_wards(
        [{"is_accepting": False}],
        10
    )
    assert result["acuity_score"] == 0


def test_ward_accepting_with_missing_defaults():
    result = process_triage_wards(
        [{"is_accepting": True}],
        10
    )
    assert result["acuity_score"] == 0


# Patient iteration and vital validation branches
def test_empty_patient_list():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": []}],
        10
    )
    assert result["status"] == "NO_URGENT_CASES"


def test_spo2_invalid():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 0, "hr": 75}]
        }],
        10
    )
    assert result["acuity_score"] == 0


def test_heart_rate_invalid():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 98, "hr": 0}]
        }],
        10
    )
    assert result["acuity_score"] == 0


def test_valid_vitals():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 95, "hr": 75}]
        }],
        10
    )
    assert result["acuity_score"] == 10


# Consciousness and ward tier branches
def test_unconscious_general_ward():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "tier": "general",
            "patients": [{"unconscious": True}]
        }],
        10
    )
    assert result["acuity_score"] == 100


def test_unconscious_outpatient_ward():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [{"unconscious": True}]
        }],
        10
    )
    assert result["status"] == "NO_URGENT_CASES"


def test_outpatient_break_stops_remaining_patients():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [
                {"unconscious": True},
                {"spo2": 80, "hr": 130}
            ]
        }],
        10
    )
    assert result["acuity_score"] == 0


# Critical patient branches
def test_low_spo2_branch():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 89, "hr": 75}]
        }],
        10
    )
    assert result["acuity_score"] == 60


def test_high_heart_rate_branch():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 95, "hr": 121}]
        }],
        10
    )
    assert result["acuity_score"] == 60


def test_normal_patient_branch():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 95, "hr": 120}]
        }],
        10
    )
    assert result["acuity_score"] == 10


# ICU standby branches
def test_icu_standby_enabled():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "icu_standby": True,
            "patients": []
        }],
        10
    )
    assert result["acuity_score"] == 25


def test_icu_standby_disabled():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "icu_standby": False,
            "patients": []
        }],
        10
    )
    assert result["acuity_score"] == 0


# Final status branches
def test_ward_alert_threshold_exceeded():
    patients = [{"spo2": 0} for _ in range(5)]
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": patients
        }],
        10
    )
    assert result["status"] == "WARD_ALERT"


def test_flagged_entries_at_threshold():
    patients = [{"spo2": 0} for _ in range(4)]
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": patients
        }],
        10
    )
    assert result["status"] == "NO_URGENT_CASES"


def test_triage_stable_status():
    result = process_triage_wards(
        [{
            "is_accepting": True,
            "patients": [{"spo2": 98, "hr": 75}]
        }],
        10
    )
    assert result["status"] == "TRIAGE_STABLE"


# Oxygen manifold branches
def test_no_sensor_streams():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_empty_sensor_manifold():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"


def test_normal_pressure():
    assert monitor_oxygen_manifolds(
        [[5.0, 4.5, 4.0]]
    ) == "PRESSURE_NORMAL"


def test_one_low_pressure_reading():
    assert monitor_oxygen_manifolds(
        [[3.5, 4.5]]
    ) == "PRESSURE_NORMAL"


def test_two_consecutive_low_readings():
    assert monitor_oxygen_manifolds(
        [[3.5, 3.8]]
    ) == "PRESSURE_FAILURE"


def test_pressure_recovery_resets_streak():
    assert monitor_oxygen_manifolds(
        [[3.5, 4.5, 3.8, 3.9]]
    ) == "PRESSURE_FAILURE"


def test_failure_in_later_manifold():
    assert monitor_oxygen_manifolds(
        [[3.5, 4.5], [3.0, 3.5]]
    ) == "PRESSURE_FAILURE"
