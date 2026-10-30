"""Database operations for medical history and prescriptions."""

import sqlite3
from pathlib import Path


def get_medical_db_connection(database_path):
    """Open a SQLite connection with foreign-key enforcement."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_medical_records_db(database_path):
    """Create Part 3 tables without changing existing project tables."""
    with get_medical_db_connection(database_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS medical_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                diagnosis TEXT NOT NULL,
                symptoms TEXT NOT NULL,
                clinical_notes TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id)
                    REFERENCES patients(id)
                    ON DELETE CASCADE
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                medical_history_id INTEGER NOT NULL,
                medication_name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                frequency TEXT NOT NULL,
                duration TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id)
                    REFERENCES patients(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (medical_history_id)
                    REFERENCES medical_history(id)
                    ON DELETE CASCADE
            )
        """)

        # Ensure a prescription can only reference a history record
        # belonging to the same patient.
        connection.execute("""
            CREATE TRIGGER IF NOT EXISTS validate_prescription_patient
            BEFORE INSERT ON prescriptions
            FOR EACH ROW
            WHEN NOT EXISTS (
                SELECT 1
                FROM medical_history
                WHERE id = NEW.medical_history_id
                  AND patient_id = NEW.patient_id
            )
            BEGIN
                SELECT RAISE(ABORT,
                    'Prescription patient must match medical history patient');
            END
        """)

        connection.execute("""
            CREATE TRIGGER IF NOT EXISTS validate_prescription_patient_update
            BEFORE UPDATE OF patient_id, medical_history_id ON prescriptions
            FOR EACH ROW
            WHEN NOT EXISTS (
                SELECT 1
                FROM medical_history
                WHERE id = NEW.medical_history_id
                  AND patient_id = NEW.patient_id
            )
            BEGIN
                SELECT RAISE(ABORT,
                    'Prescription patient must match medical history patient');
            END
        """)
