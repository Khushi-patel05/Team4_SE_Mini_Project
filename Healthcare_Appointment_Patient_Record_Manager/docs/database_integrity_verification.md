# Database Integrity and Constraint Testing Report

**Project:** Healthcare Appointment and Patient Record Manager  
**Jira Tasks:** HAPRM-28, HAPRM-30  
**Module:** Medical History and Prescription Management  
**Date:** November 5, 2026

## 1. Objective

Verify the database schema, primary keys, foreign keys, referential integrity, database constraints, input validation and CRUD-related behaviour of the medical history and prescription modules.

## 2. Database Structure

### medical_history

- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `patient_id`: INTEGER NOT NULL
- `diagnosis`: TEXT NOT NULL
- `symptoms`: TEXT NOT NULL
- `clinical_notes`: TEXT NOT NULL
- `created_at`: TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

**Foreign key:** `patient_id` references `patients(id)` with ON DELETE CASCADE.

### prescriptions

- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `patient_id`: INTEGER NOT NULL
- `medical_history_id`: INTEGER NOT NULL
- `medication_name`: TEXT NOT NULL
- `dosage`: TEXT NOT NULL
- `frequency`: TEXT NOT NULL
- `duration`: TEXT NOT NULL
- `created_at`: TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

**Foreign keys:**
- `patient_id` references `patients(id)` with ON DELETE CASCADE.
- `medical_history_id` references `medical_history(id)` with ON DELETE CASCADE.

## 3. Integrity Mechanisms Verified

- Primary-key definitions for both tables.
- Foreign-key definitions and relationships.
- SQLite foreign-key enforcement.
- Rejection of references to nonexistent patients.
- Rejection of references to nonexistent medical-history records.
- Prescription ownership validation during INSERT.
- Prescription ownership validation during UPDATE.
- Cascade deletion of prescriptions when their medical-history record is deleted.
- NOT NULL constraints on required database fields.

## 4. Constraint and Validation Testing

The following application-level validations were tested:

| Validation | Expected behaviour |
|---|---|
| Empty diagnosis | Rejected |
| Whitespace-only diagnosis | Rejected |
| Diagnosis exceeding 200 characters | Rejected |
| Empty symptoms | Rejected |
| Empty clinical notes | Rejected |
| Empty medication name | Rejected |
| Whitespace-only medication name | Rejected |
| Medication name exceeding 120 characters | Rejected |
| Empty dosage, frequency or duration | Rejected |

Additional observations:

- Duplicate medical-history records are currently permitted.
- Duplicate prescriptions are currently permitted.
- No uniqueness constraint is defined for these records.

These observations document the current implementation rather than treating duplicate records as rejected.

## 5. Test Results

| Test suite | Passed | Failed |
|---|---:|---:|
| Database integrity and constraint tests | 18 | 0 |
| Existing medical-record tests | 9 | 0 |
| Other application tests | 31 | 0 |
| **Complete application test suite** | **58** | **0** |

All 58 tests passed during complete application test execution.

## 6. Conclusion

The verification confirms that the tested primary keys, foreign keys, referential-integrity mechanisms, prescription ownership rules, cascade deletion and input-validation rules behave as expected.

The application also permits duplicate medical-history and prescription records under the current schema.

No test failures were observed during the complete application test run.

## 7. Scope

This report focuses on the medical-history and prescription database module. The complete application test suite was executed to check for regressions, but this does not constitute exhaustive verification of every database table or business rule.

## 8. Testing Issues and Observations

| ID | Observation | Impact | Status |
|---|---|---|---|
| DB-01 | Duplicate medical-history records are permitted. | May create repeated clinical entries. | Documented |
| DB-02 | Duplicate prescriptions are permitted. | May create repeated medication entries. | Documented |
| DB-03 | No uniqueness constraints are defined for these records. | Duplicate prevention is not enforced at database level. | Documented |

These observations reflect the current database design. No changes
were made to duplicate-record behaviour because a uniqueness
requirement was not specified.

## 9. Test Execution

**Testing framework:** pytest  
**Database:** SQLite  
**Commands executed:**

- `python -m pytest tests/test_database_integrity.py -v`
- `python -m pytest -v`

**Final result:** 58 tests passed, 0 failed.

## 10. Final Assessment

The medical-history and prescription modules passed the implemented
database integrity, constraint and validation tests.

The identified duplicate-record behaviour has been documented for
future consideration. No unresolved test failures were observed.