import sqlite3
from datetime import datetime, timedelta

import pytest


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def set_role(client, role):
    """Change the authenticated user's role for testing."""
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = role


def create_patient(app):
    """Insert a patient directly into the test database."""
    connection = sqlite3.connect(app.config["DATABASE"])

    cursor = connection.execute("""
        INSERT INTO patients (
            full_name,
            date_of_birth,
            gender,
            phone,
            email,
            address
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Test Patient",
        "1990-05-15",
        "Female",
        "9876543210",
        "test@example.com",
        "Test Address",
    ))

    patient_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return patient_id


def create_appointment(app, patient_id):
    """Insert a future appointment into the test database."""
    future_date = (datetime.now() + timedelta(days=3)).date()

    connection = sqlite3.connect(app.config["DATABASE"])

    cursor = connection.execute("""
        INSERT INTO appointments (
            patient_id,
            doctor_name,
            appointment_date,
            appointment_time,
            reason,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        "Dr. Test",
        future_date.isoformat(),
        "10:00",
        "General Checkup",
        "Scheduled",
    ))

    appointment_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return appointment_id


# =========================================================
# PATIENT PERMISSION TESTS
# =========================================================

@pytest.mark.parametrize(
    "role",
    ["Administrator", "Doctor", "Receptionist"],
)
def test_all_roles_can_view_patients(client, role):
    set_role(client, role)

    response = client.get("/patients")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "role",
    ["Administrator", "Receptionist"],
)
def test_admin_and_receptionist_can_register_patients(
    app, client, patient_data, role
):
    set_role(client, role)

    response = client.post(
        "/patients",
        data=patient_data,
        follow_redirects=True,
    )

    assert response.status_code == 200

    connection = sqlite3.connect(app.config["DATABASE"])
    count = connection.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]
    connection.close()

    assert count == 1


def test_doctor_cannot_register_patients(
    app, client, patient_data
):
    set_role(client, "Doctor")

    client.post("/patients", data=patient_data)

    connection = sqlite3.connect(app.config["DATABASE"])
    count = connection.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]
    connection.close()

    assert count == 0


@pytest.mark.parametrize(
    "role",
    ["Administrator", "Receptionist"],
)
def test_admin_and_receptionist_can_edit_patients(
    app, client, role
):
    patient_id = create_patient(app)
    set_role(client, role)

    response = client.get(
        f"/patients/{patient_id}/edit"
    )

    assert response.status_code == 200


def test_doctor_cannot_edit_patients(app, client):
    patient_id = create_patient(app)
    set_role(client, "Doctor")

    response = client.get(
        f"/patients/{patient_id}/edit"
    )

    assert response.status_code == 302


@pytest.mark.parametrize(
    "role",
    ["Doctor", "Receptionist"],
)
def test_non_admin_cannot_delete_patients(
    app, client, role
):
    patient_id = create_patient(app)
    set_role(client, role)

    response = client.post(
        f"/patients/{patient_id}/delete"
    )

    assert response.status_code == 302

    connection = sqlite3.connect(app.config["DATABASE"])
    patient = connection.execute(
        "SELECT id FROM patients WHERE id = ?",
        (patient_id,),
    ).fetchone()
    connection.close()

    assert patient is not None


def test_admin_can_delete_patients(app, client):
    patient_id = create_patient(app)
    set_role(client, "Administrator")

    response = client.post(
        f"/patients/{patient_id}/delete"
    )

    assert response.status_code == 302

    connection = sqlite3.connect(app.config["DATABASE"])
    patient = connection.execute(
        "SELECT id FROM patients WHERE id = ?",
        (patient_id,),
    ).fetchone()
    connection.close()

    assert patient is None


# =========================================================
# APPOINTMENT PERMISSION TESTS
# =========================================================

@pytest.mark.parametrize(
    "role",
    ["Administrator", "Doctor", "Receptionist"],
)
def test_all_roles_can_view_appointments(client, role):
    set_role(client, role)

    response = client.get("/appointments")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "role",
    ["Administrator", "Receptionist"],
)
def test_admin_and_receptionist_can_book_appointments(
    app, client, role
):
    patient_id = create_patient(app)
    set_role(client, role)

    future_date = (
        datetime.now() + timedelta(days=5)
    ).date().isoformat()

    response = client.post(
        "/appointments",
        data={
            "patient_id": str(patient_id),
            "doctor_name": "Dr. Test",
            "appointment_date": future_date,
            "appointment_time": "11:00",
            "reason": "General Checkup",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    connection = sqlite3.connect(app.config["DATABASE"])
    count = connection.execute(
        "SELECT COUNT(*) FROM appointments"
    ).fetchone()[0]
    connection.close()

    assert count == 1


def test_doctor_cannot_book_appointments(app, client):
    patient_id = create_patient(app)
    set_role(client, "Doctor")

    future_date = (
        datetime.now() + timedelta(days=5)
    ).date().isoformat()

    client.post(
        "/appointments",
        data={
            "patient_id": str(patient_id),
            "doctor_name": "Dr. Test",
            "appointment_date": future_date,
            "appointment_time": "11:00",
            "reason": "General Checkup",
        },
    )

    connection = sqlite3.connect(app.config["DATABASE"])
    count = connection.execute(
        "SELECT COUNT(*) FROM appointments"
    ).fetchone()[0]
    connection.close()

    assert count == 0


@pytest.mark.parametrize(
    "role",
    ["Administrator", "Receptionist"],
)
def test_admin_and_receptionist_can_reschedule(
    app, client, role
):
    patient_id = create_patient(app)
    appointment_id = create_appointment(app, patient_id)

    set_role(client, role)

    response = client.get(
        f"/appointments/{appointment_id}/edit"
    )

    assert response.status_code == 200


def test_doctor_cannot_reschedule_appointments(
    app, client
):
    patient_id = create_patient(app)
    appointment_id = create_appointment(app, patient_id)

    set_role(client, "Doctor")

    response = client.get(
        f"/appointments/{appointment_id}/edit"
    )

    assert response.status_code == 302


@pytest.mark.parametrize(
    "role",
    ["Administrator", "Receptionist"],
)
def test_admin_and_receptionist_can_cancel_appointments(
    app, client, role
):
    patient_id = create_patient(app)
    appointment_id = create_appointment(app, patient_id)

    set_role(client, role)

    response = client.post(
        f"/appointments/{appointment_id}/status",
        data={"status": "Cancelled"},
    )

    assert response.status_code == 302

    connection = sqlite3.connect(app.config["DATABASE"])
    status = connection.execute(
        "SELECT status FROM appointments WHERE id = ?",
        (appointment_id,),
    ).fetchone()[0]
    connection.close()

    assert status == "Cancelled"


def test_doctor_cannot_cancel_appointments(app, client):
    patient_id = create_patient(app)
    appointment_id = create_appointment(app, patient_id)

    set_role(client, "Doctor")

    client.post(
        f"/appointments/{appointment_id}/status",
        data={"status": "Cancelled"},
    )

    connection = sqlite3.connect(app.config["DATABASE"])
    status = connection.execute(
        "SELECT status FROM appointments WHERE id = ?",
        (appointment_id,),
    ).fetchone()[0]
    connection.close()

    assert status == "Scheduled"


# =========================================================
# STAFF MANAGEMENT PERMISSION TESTS
# =========================================================

@pytest.mark.parametrize(
    "role",
    ["Doctor", "Receptionist"],
)
def test_non_admin_cannot_manage_staff(client, role):
    set_role(client, role)

    response = client.get("/auth/manage-users")

    assert response.status_code == 302


def test_admin_can_access_staff_management(client):
    set_role(client, "Administrator")

    response = client.get("/auth/manage-users")

    assert response.status_code == 200