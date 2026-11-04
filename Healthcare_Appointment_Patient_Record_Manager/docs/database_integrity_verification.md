# Database Integrity Verification Report

**Project:** Healthcare Appointment and Patient Record Manager
**Jira Task:** HAPRM-28
**Module:** Medical History and Prescription Management
**Date:** November 4, 2026

## 1. Objective

Verify the database schema, primary keys, foreign keys, referential integrity and database constraints for the medical history and prescription modules.

## 2. Database Structure

### medical_history
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- patient_id: INTEGER NOT NULL
- diagnosis: TEXT NOT NULL
- symptoms: TEXT NOT NULL
- clinical_notes: TEXT NOT NULL
- created_at: TEXT NOT NULL

Foreign key: patient_id references patients(id), ON DELETE CASCADE.

### prescriptions
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- patient_id: INTEGER NOT NULL
- medical_history_id: INTEGER NOT NULL
- medication_name: TEXT NOT NULL
- dosage: TEXT NOT NULL
- frequency: TEXT NOT NULL
- duration: TEXT NOT NULL
- created_at: TEXT NOT NULL

Foreign keys:
- patient_id references patients(id), ON DELETE CASCADE.
- medical_history_id references medical_history(id), ON DELETE CASCADE.

## 3. Integrity Mechanisms Verified

- Primary-key definitions.
- Foreign-key definitions.
- SQLite foreign-key enforcement.
- Rejection of references to nonexistent patients.
- Rejection of references to nonexistent medical-history records.
- Prescription ownership validation during INSERT.
- Prescription ownership validation during UPDATE.
- Cascade deletion of prescriptions when their medical-history record is deleted.

## 4. Test Results

| Test suite | Passed | Failed |
|---|---:|---:|
| New database integrity tests | 10 | 0 |
| Existing medical-record tests | 9 | 0 |
| Combined execution | 19 | 0 |

## 5. Conclusion

All 10 newly added database integrity tests passed. All 9 existing medical-record tests also passed during combined execution.

The verification confirms that the tested primary-key, foreign-key, referential-integrity, prescription ownership and cascade-deletion mechanisms behave as expected in the isolated SQLite test database.

## 6. Scope

This report covers the medical-history and prescription database module. It does not claim verification of every database table or the entire application.
