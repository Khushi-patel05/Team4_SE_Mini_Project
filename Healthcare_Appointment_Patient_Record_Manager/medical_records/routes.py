"""Flask routes for Part 3: medical history and prescriptions."""

import sqlite3

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session
)

from . import medical_records_bp
from .models import get_medical_db_connection, initialize_medical_records_db


def _connection():
    """Use the database configured by the main Flask application."""
    return get_medical_db_connection(current_app.config["DATABASE"])


def _ensure_schema():
    """Support the app's isolated temporary database during tests."""
    initialize_medical_records_db(current_app.config["DATABASE"])


def _clean(value):
    return (value or "").strip()


@medical_records_bp.before_request
def ensure_medical_records_schema():
    if "user_id" not in session:
        flash("Please log in to access medical records.", "warning")
        return redirect(url_for("auth.login"))

    _ensure_schema()



@medical_records_bp.get("/")
def index():
    """List registered patients and open their clinical records."""
    with _connection() as connection:
        patients = connection.execute("""
            SELECT id, patient_code, full_name, phone
            FROM patients
            ORDER BY full_name COLLATE NOCASE
        """).fetchall()

    return render_template("medical_records/index.html", patients=patients)


@medical_records_bp.get("/patient/<int:patient_id>")
def patient_records(patient_id):
    """Display a patient's medical history and prescriptions."""
    with _connection() as connection:
        patient = connection.execute(
            "SELECT * FROM patients WHERE id = ?", (patient_id,)
        ).fetchone()

        if patient is None:
            flash("Patient record not found.", "danger")
            return redirect(url_for("medical_records.index"))

        history = connection.execute("""
            SELECT *
            FROM medical_history
            WHERE patient_id = ?
            ORDER BY created_at DESC, id DESC
        """, (patient_id,)).fetchall()

        prescriptions = connection.execute("""
            SELECT p.*, mh.diagnosis
            FROM prescriptions AS p
            JOIN medical_history AS mh
              ON mh.id = p.medical_history_id
             AND mh.patient_id = p.patient_id
            WHERE p.patient_id = ?
            ORDER BY p.created_at DESC, p.id DESC
        """, (patient_id,)).fetchall()

    return render_template(
        "medical_records/patient_records.html",
        patient=patient,
        history=history,
        prescriptions=prescriptions,
    )


@medical_records_bp.route(
    "/patient/<int:patient_id>/history/new",
    methods=["GET", "POST"],
)
def add_medical_history(patient_id):
    """Record diagnosis, symptoms and clinical notes for a patient."""
    with _connection() as connection:
        patient = connection.execute(
            "SELECT id, patient_code, full_name FROM patients WHERE id = ?",
            (patient_id,),
        ).fetchone()

    if patient is None:
        flash("Select an existing registered patient.", "danger")
        return redirect(url_for("medical_records.index"))

    if request.method == "POST":
        diagnosis = _clean(request.form.get("diagnosis"))
        symptoms = _clean(request.form.get("symptoms"))
        clinical_notes = _clean(request.form.get("clinical_notes"))

        errors = []
        if not diagnosis or len(diagnosis) > 200:
            errors.append("Enter a diagnosis of 1–200 characters.")
        if not symptoms or len(symptoms) > 2000:
            errors.append("Enter symptoms of 1–2000 characters.")
        if not clinical_notes or len(clinical_notes) > 5000:
            errors.append("Enter clinical notes of 1–5000 characters.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "medical_records/add_history.html",
                patient=patient,
                form=request.form,
            )

        with _connection() as connection:
            connection.execute("""
                INSERT INTO medical_history
                    (patient_id, diagnosis, symptoms, clinical_notes)
                VALUES (?, ?, ?, ?)
            """, (patient_id, diagnosis, symptoms, clinical_notes))

        flash("Medical history recorded successfully.", "success")
        return redirect(
            url_for("medical_records.patient_records", patient_id=patient_id)
        )

    return render_template(
        "medical_records/add_history.html", patient=patient, form={}
    )


@medical_records_bp.route(
    "/history/<int:history_id>/prescriptions/new",
    methods=["GET", "POST"],
)
def add_prescription(history_id):
    """Create a prescription linked to the selected clinical record."""
    with _connection() as connection:
        history = connection.execute("""
            SELECT mh.*, patients.full_name, patients.patient_code
            FROM medical_history AS mh
            JOIN patients ON patients.id = mh.patient_id
            WHERE mh.id = ?
        """, (history_id,)).fetchone()

    if history is None:
        flash("Medical history record not found.", "danger")
        return redirect(url_for("medical_records.index"))

    if request.method == "POST":
        medication_name = _clean(request.form.get("medication_name"))
        dosage = _clean(request.form.get("dosage"))
        frequency = _clean(request.form.get("frequency"))
        duration = _clean(request.form.get("duration"))

        fields = {
            "Medication name": (medication_name, 120),
            "Dosage": (dosage, 100),
            "Frequency": (frequency, 100),
            "Duration": (duration, 100),
        }
        errors = [
            f"Enter a valid {label.lower()} (maximum {limit} characters)."
            for label, (value, limit) in fields.items()
            if not value or len(value) > limit
        ]

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "medical_records/add_prescription.html",
                history=history,
                form=request.form,
            )

        try:
            with _connection() as connection:
                connection.execute("""
                    INSERT INTO prescriptions (
                        patient_id, medical_history_id,
                        medication_name, dosage, frequency, duration
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    history["patient_id"],
                    history_id,
                    medication_name,
                    dosage,
                    frequency,
                    duration,
                ))
        except sqlite3.IntegrityError:
            current_app.logger.exception("Prescription integrity error")
            flash("Could not link the prescription to this clinical record.", "danger")
            return redirect(
                url_for(
                    "medical_records.patient_records",
                    patient_id=history["patient_id"],
                )
            )

        flash("Prescription created successfully.", "success")
        return redirect(
            url_for(
                "medical_records.patient_records",
                patient_id=history["patient_id"],
            )
        )

    return render_template(
        "medical_records/add_prescription.html",
        history=history,
        form={},
    )
