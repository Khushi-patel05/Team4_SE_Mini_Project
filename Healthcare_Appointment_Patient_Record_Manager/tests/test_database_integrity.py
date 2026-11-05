
"""Database integrity tests for medical history and prescriptions."""

import sqlite3

import pytest

import app as app_module
from medical_records.models import initialize_medical_records_db


def register_patient(client, patient_data):
    """Register a patient and return the generated patient ID."""
    response = client.post(
        "/patients",
        data=patient_data,
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app_module.get_db_connection() as connection:
        row = connection.execute(
            "SELECT id FROM patients ORDER BY id DESC LIMIT 1"
        ).fetchone()

    return row["id"]


def create_history(patient_id):
    """Insert a medical-history record directly into SQLite."""
    with app_module.get_db_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO medical_history
                (patient_id, diagnosis, symptoms, clinical_notes)
            VALUES (?, ?, ?, ?)
            """,
            (
                patient_id,
                "Seasonal flu",
                "Fever and cough",
                "Rest advised",
            ),
        )
        return cursor.lastrowid


@pytest.fixture
def medical_db(app, client):
    """Initialize the medical-record schema in the isolated test DB."""
    initialize_medical_records_db(app.config["DATABASE"])
    return app.config["DATABASE"]


def test_medical_tables_have_primary_keys(medical_db):
    with app_module.get_db_connection() as connection:
        for table in ("medical_history", "prescriptions"):
            columns = connection.execute(
                f"PRAGMA table_info({table})"
            ).fetchall()

            primary_keys = [
                column["name"]
                for column in columns
                if column["pk"] == 1
            ]

            assert primary_keys == ["id"]


def test_medical_history_has_patient_foreign_key(medical_db):
    with app_module.get_db_connection() as connection:
        foreign_keys = connection.execute(
            "PRAGMA foreign_key_list(medical_history)"
        ).fetchall()

    assert any(
        fk["table"] == "patients"
        and fk["from"] == "patient_id"
        and fk["to"] == "id"
        and fk["on_delete"] == "CASCADE"
        for fk in foreign_keys
    )


def test_prescriptions_have_required_foreign_keys(medical_db):
    with app_module.get_db_connection() as connection:
        foreign_keys = connection.execute(
            "PRAGMA foreign_key_list(prescriptions)"
        ).fetchall()

    relationships = {
        (fk["table"], fk["from"], fk["to"])
        for fk in foreign_keys
    }

    assert ("patients", "patient_id", "id") in relationships
    assert (
        "medical_history",
        "medical_history_id",
        "id",
    ) in relationships


def test_foreign_key_enforcement_is_enabled(medical_db):
    with app_module.get_db_connection() as connection:
        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]

    assert result == 1


def test_medical_history_rejects_unknown_patient(
    medical_db,
):
    with app_module.get_db_connection() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO medical_history
                    (patient_id, diagnosis, symptoms, clinical_notes)
                VALUES (?, ?, ?, ?)
                """,
                (999999, "Test", "Test", "Test"),
            )


def test_prescription_rejects_unknown_patient(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(patient_id)

    with app_module.get_db_connection() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO prescriptions
                    (patient_id, medical_history_id,
                     medication_name, dosage, frequency, duration)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    999999,
                    history_id,
                    "Test medicine",
                    "1 tablet",
                    "Daily",
                    "3 days",
                ),
            )


def test_prescription_rejects_unknown_history(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)

    with app_module.get_db_connection() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO prescriptions
                    (patient_id, medical_history_id,
                     medication_name, dosage, frequency, duration)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    patient_id,
                    999999,
                    "Test medicine",
                    "1 tablet",
                    "Daily",
                    "3 days",
                ),
            )


def test_insert_trigger_rejects_mismatched_patient(
    medical_db, client, patient_data
):
    first_patient_id = register_patient(client, patient_data)

    second_data = {
        **patient_data,
        "phone": "9876543211",
        "email": "second.patient@example.com",
    }
    second_patient_id = register_patient(client, second_data)

    history_id = create_history(first_patient_id)

    with app_module.get_db_connection() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO prescriptions
                    (patient_id, medical_history_id,
                     medication_name, dosage, frequency, duration)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    second_patient_id,
                    history_id,
                    "Test medicine",
                    "1 tablet",
                    "Daily",
                    "3 days",
                ),
            )


def test_update_trigger_rejects_mismatched_patient(
    medical_db, client, patient_data
):
    first_patient_id = register_patient(client, patient_data)

    second_data = {
        **patient_data,
        "phone": "9876543212",
        "email": "third.patient@example.com",
    }
    second_patient_id = register_patient(client, second_data)

    history_id = create_history(first_patient_id)

    with app_module.get_db_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO prescriptions
                (patient_id, medical_history_id,
                 medication_name, dosage, frequency, duration)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                first_patient_id,
                history_id,
                "Paracetamol",
                "500 mg",
                "Twice daily",
                "3 days",
            ),
        )
        prescription_id = cursor.lastrowid

    with app_module.get_db_connection() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                UPDATE prescriptions
                SET patient_id = ?
                WHERE id = ?
                """,
                (second_patient_id, prescription_id),
            )


def test_deleting_history_cascades_to_prescriptions(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(patient_id)

    with app_module.get_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO prescriptions
                (patient_id, medical_history_id,
                 medication_name, dosage, frequency, duration)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                history_id,
                "Paracetamol",
                "500 mg",
                "Twice daily",
                "3 days",
            ),
        )

    with app_module.get_db_connection() as connection:
        connection.execute(
            "DELETE FROM medical_history WHERE id = ?",
            (history_id,),
        )

        remaining = connection.execute(
            """
            SELECT COUNT(*) FROM prescriptions
            WHERE medical_history_id = ?
            """,
            (history_id,),
        ).fetchone()[0]

    assert remaining == 0
def test_medical_history_rejects_null_required_fields(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)

    with app_module.get_db_connection() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO medical_history
                    (patient_id, diagnosis, symptoms, clinical_notes)
                VALUES (?, NULL, ?, ?)
                """,
                (patient_id, "Fever", "Rest advised"),
            )


def test_prescription_rejects_null_required_fields(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(patient_id)

    with app_module.get_db_connection() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO prescriptions (
                    patient_id, medical_history_id,
                    medication_name, dosage, frequency, duration
                )
                VALUES (?, ?, NULL, ?, ?, ?)
                """,
                (
                    patient_id, history_id,
                    "500 mg", "Daily", "3 days"
                ),
            )


def test_duplicate_medical_history_records_are_allowed(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)

    with app_module.get_db_connection() as connection:
        for _ in range(2):
            connection.execute(
                """
                INSERT INTO medical_history
                    (patient_id, diagnosis, symptoms, clinical_notes)
                VALUES (?, ?, ?, ?)
                """,
                (
                    patient_id,
                    "Seasonal flu",
                    "Fever and cough",
                    "Rest advised",
                ),
            )

        count = connection.execute(
            """
            SELECT COUNT(*) FROM medical_history
            WHERE patient_id = ? AND diagnosis = ?
            """,
            (patient_id, "Seasonal flu"),
        ).fetchone()[0]

    assert count == 2


def test_duplicate_prescriptions_are_allowed(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(patient_id)

    with app_module.get_db_connection() as connection:
        for _ in range(2):
            connection.execute(
                """
                INSERT INTO prescriptions (
                    patient_id, medical_history_id,
                    medication_name, dosage, frequency, duration
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    patient_id, history_id,
                    "Paracetamol", "500 mg",
                    "Twice daily", "3 days",
                ),
            )

        count = connection.execute(
            """
            SELECT COUNT(*) FROM prescriptions
            WHERE medical_history_id = ?
              AND medication_name = ?
            """,
            (history_id, "Paracetamol"),
        ).fetchone()[0]

    assert count == 2
def test_medical_history_rejects_whitespace_only_fields(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)

    response = client.post(
        f"/medical-records/patient/{patient_id}/history/new",
        data={
            "diagnosis": "   ",
            "symptoms": "Fever",
            "clinical_notes": "Rest advised",
        },
        follow_redirects=True,
    )

    assert b"Enter a diagnosis" in response.data


def test_medical_history_rejects_excessive_field_length(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)

    response = client.post(
        f"/medical-records/patient/{patient_id}/history/new",
        data={
            "diagnosis": "A" * 201,
            "symptoms": "Fever",
            "clinical_notes": "Rest advised",
        },
        follow_redirects=True,
    )

    assert b"Enter a diagnosis" in response.data


def test_prescription_rejects_whitespace_only_fields(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(patient_id)

    response = client.post(
        f"/medical-records/history/{history_id}/prescriptions/new",
        data={
            "medication_name": "   ",
            "dosage": "500 mg",
            "frequency": "Daily",
            "duration": "3 days",
        },
        follow_redirects=True,
    )

    assert b"valid medication name" in response.data


def test_prescription_rejects_excessive_field_length(
    medical_db, client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(patient_id)

    response = client.post(
        f"/medical-records/history/{history_id}/prescriptions/new",
        data={
            "medication_name": "A" * 121,
            "dosage": "500 mg",
            "frequency": "Daily",
            "duration": "3 days",
        },
        follow_redirects=True,
    )

    assert b"valid medication name" in response.data