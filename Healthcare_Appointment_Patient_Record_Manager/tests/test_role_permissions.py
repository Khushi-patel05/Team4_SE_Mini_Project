
"""Tests for role-based access to medical records."""

import app as app_module


def set_role(client, role):
    """Change the authenticated user's role."""
    with client.session_transaction() as session:
        session["role"] = role


def register_patient(client, patient_data):
    """Register a patient using the Administrator account."""
    response = client.post(
        "/patients",
        data=patient_data,
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app_module.get_db_connection() as connection:
        patient = connection.execute(
            "SELECT id FROM patients ORDER BY id DESC LIMIT 1"
        ).fetchone()

    return patient["id"]


def create_history(client, patient_id):
    """Create medical history using the Administrator account."""
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

    with app_module.get_db_connection() as connection:
        history = connection.execute(
            """
            SELECT id FROM medical_history
            WHERE patient_id = ?
            ORDER BY id DESC LIMIT 1
            """,
            (patient_id,),
        ).fetchone()

    return history["id"]


def test_all_roles_can_view_medical_records_patient_list(
    client, patient_data
):
    register_patient(client, patient_data)

    for role in ("Administrator", "Doctor", "Receptionist"):
        set_role(client, role)

        response = client.get("/medical-records/")

        assert response.status_code == 200


def test_administrator_can_view_medical_history(
    client, patient_data
):
    patient_id = register_patient(client, patient_data)
    create_history(client, patient_id)

    set_role(client, "Administrator")

    response = client.get(
        f"/medical-records/patient/{patient_id}"
    )

    assert response.status_code == 200
    assert b"Seasonal flu" in response.data


def test_doctor_can_view_medical_history(
    client, patient_data
):
    patient_id = register_patient(client, patient_data)
    create_history(client, patient_id)

    set_role(client, "Doctor")

    response = client.get(
        f"/medical-records/patient/{patient_id}"
    )

    assert response.status_code == 200
    assert b"Seasonal flu" in response.data


def test_receptionist_cannot_view_medical_history(
    client, patient_data
):
    patient_id = register_patient(client, patient_data)

    set_role(client, "Receptionist")

    response = client.get(
        f"/medical-records/patient/{patient_id}"
    )

    assert response.status_code == 302


def test_receptionist_cannot_add_medical_history(
    client, patient_data
):
    patient_id = register_patient(client, patient_data)

    set_role(client, "Receptionist")

    response = client.post(
        f"/medical-records/patient/{patient_id}/history/new",
        data={
            "diagnosis": "Test diagnosis",
            "symptoms": "Test symptoms",
            "clinical_notes": "Test notes",
        },
    )

    assert response.status_code == 302

    with app_module.get_db_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM medical_history"
        ).fetchone()[0]

    assert count == 0


def test_doctor_can_add_medical_history(
    client, patient_data
):
    patient_id = register_patient(client, patient_data)

    set_role(client, "Doctor")

    response = client.post(
        f"/medical-records/patient/{patient_id}/history/new",
        data={
            "diagnosis": "Seasonal flu",
            "symptoms": "Fever",
            "clinical_notes": "Rest advised.",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app_module.get_db_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM medical_history"
        ).fetchone()[0]

    assert count == 1


def test_receptionist_cannot_create_prescription(
    client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(client, patient_id)

    set_role(client, "Receptionist")

    response = client.post(
        f"/medical-records/history/{history_id}/prescriptions/new",
        data={
            "medication_name": "Paracetamol",
            "dosage": "500 mg",
            "frequency": "Twice daily",
            "duration": "3 days",
        },
    )

    assert response.status_code == 302

    with app_module.get_db_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM prescriptions"
        ).fetchone()[0]

    assert count == 0


def test_doctor_can_create_prescription(
    client, patient_data
):
    patient_id = register_patient(client, patient_data)
    history_id = create_history(client, patient_id)

    set_role(client, "Doctor")

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

    with app_module.get_db_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM prescriptions"
        ).fetchone()[0]

    assert count == 1
