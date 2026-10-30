"""Tests for Part 3: medical history and prescription management."""

import app as app_module


def register_patient(client, patient_data):
    response = client.post("/patients", data=patient_data, follow_redirects=True)
    assert response.status_code == 200
    with app_module.get_db_connection() as connection:
        row = connection.execute(
            "SELECT id FROM patients ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return row["id"]


def create_history(client, patient_id):
    response = client.post(
        f"/medical-records/patient/{patient_id}/history/new",
        data={
            "diagnosis": "Seasonal flu",
            "symptoms": "Fever and cough",
            "clinical_notes": "Patient advised rest and fluids.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app_module.get_db_connection() as connection:
        row = connection.execute(
            "SELECT id FROM medical_history WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()
    return row["id"]


def test_medical_records_tables_created(client, app):
    # The blueprint initializes its tables against the active test database.
    client.get("/medical-records")
    with app_module.get_db_connection() as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    assert "medical_history" in tables
    assert "prescriptions" in tables


def test_add_medical_history_for_registered_patient(client, app, patient_data):
    patient_id = register_patient(client, patient_data)
    response = client.post(
        f"/medical-records/patient/{patient_id}/history/new",
        data={
            "diagnosis": "Seasonal flu",
            "symptoms": "Fever and cough",
            "clinical_notes": "Rest and hydration advised.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Medical history recorded successfully." in response.data
    with app_module.get_db_connection() as connection:
        row = connection.execute(
            "SELECT * FROM medical_history WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()
    assert row["diagnosis"] == "Seasonal flu"
    assert row["symptoms"] == "Fever and cough"


def test_reject_medical_history_for_unknown_patient(client):
    response = client.post(
        "/medical-records/patient/99999/history/new",
        data={
            "diagnosis": "Test",
            "symptoms": "Test",
            "clinical_notes": "Test",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Select an existing registered patient." in response.data


def test_reject_empty_medical_history_fields(client, app, patient_data):
    patient_id = register_patient(client, patient_data)
    response = client.post(
        f"/medical-records/patient/{patient_id}/history/new",
        data={"diagnosis": "", "symptoms": "", "clinical_notes": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Enter a diagnosis" in response.data
    with app_module.get_db_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM medical_history"
        ).fetchone()[0]
    assert count == 0


def test_create_prescription_linked_to_history(client, app, patient_data):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(client, patient_id)
    response = client.post(
        f"/medical-records/history/{history_id}/prescriptions/new",
        data={
            "medication_name": "Paracetamol",
            "dosage": "500 mg",
            "frequency": "Twice daily",
            "duration": "3 days",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Prescription created successfully." in response.data
    with app_module.get_db_connection() as connection:
        row = connection.execute(
            "SELECT * FROM prescriptions WHERE medical_history_id = ?",
            (history_id,),
        ).fetchone()
    assert row["patient_id"] == patient_id
    assert row["medication_name"] == "Paracetamol"
    assert row["dosage"] == "500 mg"
    assert row["frequency"] == "Twice daily"
    assert row["duration"] == "3 days"


def test_reject_empty_prescription_fields(client, app, patient_data):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(client, patient_id)
    response = client.post(
        f"/medical-records/history/{history_id}/prescriptions/new",
        data={
            "medication_name": "",
            "dosage": "",
            "frequency": "",
            "duration": "",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Enter a valid medication name" in response.data
    with app_module.get_db_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM prescriptions"
        ).fetchone()[0]
    assert count == 0


def test_patient_records_page_shows_history_and_prescription(
    client, app, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(client, patient_id)
    client.post(
        f"/medical-records/history/{history_id}/prescriptions/new",
        data={
            "medication_name": "Paracetamol",
            "dosage": "500 mg",
            "frequency": "Twice daily",
            "duration": "3 days",
        },
    )
    response = client.get(f"/medical-records/patient/{patient_id}")
    assert response.status_code == 200
    assert b"Seasonal flu" in response.data
    assert b"Paracetamol" in response.data


def test_prescription_cannot_be_linked_to_another_patients_history(
    client, app, patient_data
):
    first_patient_id = register_patient(client, patient_data)
    second_data = {**patient_data, "phone": "9876543211",
                   "email": "second.patient@example.com"}
    second_patient_id = register_patient(client, second_data)
    history_id = create_history(client, first_patient_id)

    # The route derives patient_id from the history record; clients cannot
    # submit a different patient ID to misassociate the prescription.
    response = client.post(
        f"/medical-records/history/{history_id}/prescriptions/new",
        data={
            "patient_id": str(second_patient_id),
            "medication_name": "Test medicine",
            "dosage": "1 tablet",
            "frequency": "Daily",
            "duration": "5 days",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app_module.get_db_connection() as connection:
        row = connection.execute(
            "SELECT patient_id FROM prescriptions WHERE medical_history_id = ?",
            (history_id,),
        ).fetchone()
    assert row["patient_id"] == first_patient_id


def test_medical_records_page_handles_missing_patient(client):
    response = client.get(
        "/medical-records/patient/99999",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Patient record not found." in response.data
