
from datetime import date, timedelta

import app as app_module


def register_patient(client, patient_data):
    response = client.post("/patients", data=patient_data)
    assert response.status_code == 302

    with app_module.get_db_connection() as connection:
        patient = connection.execute(
            "SELECT id FROM patients WHERE email = ?",
            (patient_data["email"],),
        ).fetchone()

    assert patient is not None
    return patient["id"]


def create_appointment(
    client, patient_id, days=2, time="10:30",
    reason="Routine checkup"
):
    return client.post(
        "/appointments",
        data={
            "patient_id": str(patient_id),
            "doctor_name": "Dr. Sharma",
            "appointment_date": (
                date.today() + timedelta(days=days)
            ).isoformat(),
            "appointment_time": time,
            "reason": reason,
        },
    )


def test_complete_patient_appointment_workflow(
    client, app, patient_data
):
    # Register a patient
    patient_id = register_patient(client, patient_data)

    # Book an appointment
    booking_response = create_appointment(
        client, patient_id, days=2
    )
    assert booking_response.status_code == 302

    with app_module.get_db_connection() as connection:
        appointment = connection.execute(
            "SELECT * FROM appointments WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()

    assert appointment is not None
    appointment_id = appointment["id"]
    assert appointment["status"] == "Scheduled"

    # Reschedule the appointment
    updated_date = (
        date.today() + timedelta(days=3)
    ).isoformat()

    edit_response = client.post(
        f"/appointments/{appointment_id}/edit",
        data={
            "patient_id": str(patient_id),
            "doctor_name": "Dr. Sharma",
            "appointment_date": updated_date,
            "appointment_time": "11:30",
            "reason": "Updated consultation",
        },
        follow_redirects=True,
    )

    assert edit_response.status_code == 200
    assert b"Appointment updated successfully." in edit_response.data

    # Complete the appointment
    status_response = client.post(
        f"/appointments/{appointment_id}/status",
        data={"status": "Completed"},
        follow_redirects=True,
    )

    assert status_response.status_code == 200
    assert b"Appointment marked as completed." in status_response.data

    # Verify final database state
    with app_module.get_db_connection() as connection:
        final_appointment = connection.execute(
            "SELECT * FROM appointments WHERE id = ?",
            (appointment_id,),
        ).fetchone()

    assert final_appointment["patient_id"] == patient_id
    assert final_appointment["appointment_date"] == updated_date
    assert final_appointment["appointment_time"] == "11:30"
    assert final_appointment["reason"] == "Updated consultation"
    assert final_appointment["status"] == "Completed"


def test_rescheduling_rejects_occupied_doctor_slot(
    client, app, patient_data
):
    first_patient_id = register_patient(client, patient_data)

    second_patient_data = {
        **patient_data,
        "full_name": "Second Test Patient",
        "email": "second.patient@example.com",
        "phone": "9876543211",
    }
    second_patient_id = register_patient(
        client, second_patient_data
    )

    appointment_date = (
        date.today() + timedelta(days=5)
    ).isoformat()

    first_booking = create_appointment(
        client, first_patient_id, days=5, time="10:30"
    )
    assert first_booking.status_code == 302

    second_booking = create_appointment(
        client, second_patient_id, days=5, time="11:30"
    )
    assert second_booking.status_code == 302

    with app_module.get_db_connection() as connection:
        appointments = connection.execute(
            "SELECT id FROM appointments ORDER BY id"
        ).fetchall()

    first_id = appointments[0]["id"]
    second_id = appointments[1]["id"]

    # Attempt to reschedule into an occupied slot
    conflict_response = client.post(
        f"/appointments/{second_id}/edit",
        data={
            "patient_id": str(second_patient_id),
            "doctor_name": "Dr. Sharma",
            "appointment_date": appointment_date,
            "appointment_time": "10:30",
            "reason": "Rescheduled consultation",
        },
        follow_redirects=True,
    )

    assert conflict_response.status_code == 200
    assert (
        b"That doctor already has a scheduled appointment"
        in conflict_response.data
    )

    # Verify that neither appointment was incorrectly modified
    with app_module.get_db_connection() as connection:
        first = connection.execute(
            "SELECT * FROM appointments WHERE id = ?",
            (first_id,),
        ).fetchone()

        second = connection.execute(
            "SELECT * FROM appointments WHERE id = ?",
            (second_id,),
        ).fetchone()

    assert first["appointment_time"] == "10:30"
    assert second["appointment_time"] == "11:30"
    assert second["reason"] == "Routine checkup"
    assert second["status"] == "Scheduled"


def test_reassign_appointment_to_another_patient(
    client, app, patient_data
):
    first_patient_id = register_patient(client, patient_data)

    second_patient_data = {
        **patient_data,
        "full_name": "Second Test Patient",
        "email": "second.patient@example.com",
        "phone": "9876543211",
    }
    second_patient_id = register_patient(
        client, second_patient_data
    )

    booking_response = create_appointment(
        client, first_patient_id, days=6
    )
    assert booking_response.status_code == 302

    with app_module.get_db_connection() as connection:
        appointment = connection.execute(
            "SELECT id FROM appointments"
        ).fetchone()

    appointment_id = appointment["id"]

    # Reassign the appointment to the second patient
    edit_response = client.post(
        f"/appointments/{appointment_id}/edit",
        data={
            "patient_id": str(second_patient_id),
            "doctor_name": "Dr. Sharma",
            "appointment_date": (
                date.today() + timedelta(days=6)
            ).isoformat(),
            "appointment_time": "11:30",
            "reason": "Updated consultation",
        },
        follow_redirects=True,
    )

    assert edit_response.status_code == 200
    assert b"Appointment updated successfully." in edit_response.data

    with app_module.get_db_connection() as connection:
        updated = connection.execute(
            "SELECT * FROM appointments WHERE id = ?",
            (appointment_id,),
        ).fetchone()

    assert updated["patient_id"] == second_patient_id
    assert updated["reason"] == "Updated consultation"
    assert updated["status"] == "Scheduled"


def test_cancelled_appointment_cannot_be_completed(
    client, app, patient_data
):
    patient_id = register_patient(client, patient_data)

    booking_response = create_appointment(
        client, patient_id, days=7
    )
    assert booking_response.status_code == 302

    with app_module.get_db_connection() as connection:
        appointment = connection.execute(
            "SELECT id FROM appointments"
        ).fetchone()

    appointment_id = appointment["id"]

    # Cancel the appointment
    cancel_response = client.post(
        f"/appointments/{appointment_id}/status",
        data={"status": "Cancelled"},
        follow_redirects=True,
    )
    assert cancel_response.status_code == 200

    # Try to complete the cancelled appointment
    complete_response = client.post(
        f"/appointments/{appointment_id}/status",
        data={"status": "Completed"},
        follow_redirects=True,
    )

    assert complete_response.status_code == 200
    assert (
        b"Appointment not found or is no longer scheduled."
        in complete_response.data
    )

    with app_module.get_db_connection() as connection:
        final_appointment = connection.execute(
            "SELECT status FROM appointments WHERE id = ?",
            (appointment_id,),
        ).fetchone()

    assert final_appointment["status"] == "Cancelled"


def test_cancelled_appointment_cannot_be_edited(
    client, app, patient_data
):
    patient_id = register_patient(client, patient_data)

    booking_response = create_appointment(
        client, patient_id, days=8
    )
    assert booking_response.status_code == 302

    with app_module.get_db_connection() as connection:
        appointment = connection.execute(
            "SELECT id, appointment_date FROM appointments"
        ).fetchone()

    appointment_id = appointment["id"]
    original_date = appointment["appointment_date"]

    # Cancel the appointment
    cancel_response = client.post(
        f"/appointments/{appointment_id}/status",
        data={"status": "Cancelled"},
        follow_redirects=True,
    )
    assert cancel_response.status_code == 200

    # Attempt to edit the cancelled appointment
    edit_response = client.post(
        f"/appointments/{appointment_id}/edit",
        data={
            "patient_id": str(patient_id),
            "doctor_name": "Dr. Sharma",
            "appointment_date": (
                date.today() + timedelta(days=9)
            ).isoformat(),
            "appointment_time": "12:30",
            "reason": "Attempted edit",
        },
        follow_redirects=True,
    )

    assert edit_response.status_code == 200
    assert (
        b"Only scheduled appointments can be rescheduled."
        in edit_response.data
    )

    # Verify the original cancelled record remains unchanged
    with app_module.get_db_connection() as connection:
        final_appointment = connection.execute(
            "SELECT * FROM appointments WHERE id = ?",
            (appointment_id,),
        ).fetchone()

    assert final_appointment["status"] == "Cancelled"
    assert final_appointment["appointment_date"] == original_date
    assert final_appointment["appointment_time"] == "10:30"
    assert final_appointment["reason"] == "Routine checkup"


def test_appointment_status_filter_shows_correct_patient_details(
    client, app, patient_data
):
    first_patient_id = register_patient(client, patient_data)

    second_patient_data = {
        **patient_data,
        "full_name": "Second Test Patient",
        "email": "second.patient@example.com",
        "phone": "9876543211",
    }
    second_patient_id = register_patient(
        client, second_patient_data
    )

    # Create two appointments with distinct reasons
    first_booking = create_appointment(
        client,
        first_patient_id,
        days=10,
        time="10:30",
        reason="Completed visit for first patient",
    )
    assert first_booking.status_code == 302

    second_booking = create_appointment(
        client,
        second_patient_id,
        days=10,
        time="11:30",
        reason="Upcoming visit for second patient",
    )
    assert second_booking.status_code == 302

    with app_module.get_db_connection() as connection:
        appointments = connection.execute(
            "SELECT id FROM appointments ORDER BY id"
        ).fetchall()

    first_appointment_id = appointments[0]["id"]

    # Mark the first appointment as completed
    completion_response = client.post(
        f"/appointments/{first_appointment_id}/status",
        data={"status": "Completed"},
    )
    assert completion_response.status_code == 302

    # Filter completed appointments
    completed_response = client.get(
        "/appointments?status=Completed"
    )

    assert completed_response.status_code == 200
    assert b"Completed visit for first patient" in completed_response.data
    assert b"Test Patient" in completed_response.data
    assert b"Upcoming visit for second patient" not in completed_response.data

    # Filter scheduled appointments
    scheduled_response = client.get(
        "/appointments?status=Scheduled"
    )

    assert scheduled_response.status_code == 200
    assert b"Upcoming visit for second patient" in scheduled_response.data
    assert b"Second Test Patient" in scheduled_response.data
    assert b"Completed visit for first patient" not in scheduled_response.data
