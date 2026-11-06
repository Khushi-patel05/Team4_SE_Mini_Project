# Healthcare Appointment and Patient Record Manager
# Application Features and Modules

## 1. Introduction

The Healthcare Appointment and Patient Record Manager (HAPRM) is a web-based application developed using Python Flask and SQLite. It is designed to support the day-to-day operations of small clinics by managing patient information, appointments, medical histories, prescriptions, and staff access.

The application follows a modular structure, separating authentication, patient and appointment operations, and medical record management.

## 2. System Architecture

The application follows a Flask-based web architecture.

### Architecture Components

1. **Presentation Layer:** HTML templates, CSS, JavaScript, Bootstrap and Jinja2.
2. **Application Layer:** Python Flask routes handle requests, validation, authentication and business logic.
3. **Database Layer:** SQLite stores patient details, appointments, user accounts, medical histories and prescriptions.

### Application Structure

- `app.py` – Main Flask application, patient management, appointment management and database initialization.
- `auth.py` – Authentication, user management and role-based access control.
- `config.py` – Database path and secret key configuration.
- `medical_records/` – Medical history and prescription functionality.
- `templates/` – HTML templates rendered by Flask.
- `static/` – Static assets such as CSS, JavaScript and images.
- `tests/` – Automated application tests.
- `instance/` – Local SQLite database storage.

## 3. Module 1 – Patient Management

### Purpose

The Patient Management module maintains patient information in a centralized database and allows authorized staff to register, search, view, update and manage patient records.

### Features

**Patient Registration**
- Register new patients through a form.
- Capture full name, date of birth, gender, phone number, email and address.
- Generate a unique patient code automatically after registration.

**Patient Search**
- Search existing patients using patient code, full name or phone number.
- Display matching patient records.

**View Patient Details**
- Display the registered patient's information.
- Retrieve a patient using the unique database ID.

**Edit Patient Details**
- Update existing patient information.
- Validate the submitted details before saving changes.

**Delete Patient**
- Delete patient records using a POST request.
- Prevent deletion when linked appointments violate database constraints.

### Input Validation

The application validates:
- Name format and maximum length.
- Date of birth format and future-date restrictions.
- Gender selection.
- Phone number format.
- Email format.
- Address length.

### Patient Identifier

A unique patient code is generated using the patient's database ID.

Example: `P-00001`

## 4. Module 2 – Appointment Management

### Purpose

The Appointment Management module allows clinic staff to schedule and manage patient appointments with doctors.

### Features

**Appointment Booking**
- Select an existing registered patient.
- Enter the doctor's name.
- Select appointment date and time.
- Provide the reason for the appointment.
- Save the appointment with the default status `Scheduled`.

**Appointment Listing**
- Display appointments along with patient name, patient code and phone number.
- Sort appointments by date and time.
- Filter appointments using their status.

**Appointment Rescheduling**
- Modify the patient, doctor, date, time and reason of a scheduled appointment.
- Only appointments with status `Scheduled` can be rescheduled.

**Appointment Status Management**
- Mark an appointment as `Completed`.
- Mark an appointment as `Cancelled`.
- Only scheduled appointments can transition through this operation.

### Appointment Validation

The system checks:
- The patient is registered.
- The doctor name is valid.
- The appointment date and time are valid.
- The appointment is scheduled for a future date and time.
- The reason is not empty and does not exceed the permitted length.

### Double-Booking Prevention

A unique partial database index is created for:

- Doctor name.
- Appointment date.
- Appointment time.

The index applies to appointments whose status is `Scheduled`.

This prevents two scheduled appointments from occupying the same doctor's time slot. Cancelled or completed appointments do not occupy that scheduled slot.

## 5. Module 3 – Medical History and Prescription Management

### Purpose

The Medical Records module maintains clinical information associated with registered patients and organizes prescriptions according to their medical history.

### Medical History Management

The system supports:
- Recording a patient's diagnosis.
- Recording symptoms.
- Maintaining clinical notes.
- Viewing medical history associated with a patient.
- Editing existing medical history.
- Deleting medical history records.

### Prescription Management

The system supports:
- Creating prescriptions linked to medical history.
- Recording medication name.
- Recording dosage.
- Recording frequency.
- Recording duration.
- Viewing prescriptions associated with a patient.
- Editing existing prescriptions.
- Deleting prescriptions.

### Database Integrity

The medical records database uses foreign keys to connect medical records with patients.

Prescriptions reference both:
- The patient record.
- The corresponding medical history record.

Database triggers validate that the patient ID stored in a prescription matches the patient ID of its linked medical history record.

This prevents a prescription from being linked to another patient's medical history.

## 6. Module 4 – Authentication, Dashboard and Integration

### Purpose

This module provides authentication and role-based access control for staff members using the application.

### Login

- Staff members log in using their username and password.
- Passwords are stored as secure password hashes.
- Password verification is performed using Werkzeug's password hashing utilities.
- Successful authentication creates a session containing the user ID, username and role.

### Logout

- The logout operation clears the current session.
- The user is redirected to the login page.

### User Management

Administrators can create staff accounts by specifying:
- Username.
- Password.
- Role.

The system validates username and password input, enforces a minimum password length of eight characters and restricts roles to the supported role values.

### Supported Roles

| Role | Description |
|---|---|
| Administrator | Manages staff accounts and has access to administrative functionality. |
| Doctor | Uses patient, appointment and clinical record functionality. |
| Receptionist | Handles patient registration and appointment-related operations. |

The application uses two authorization decorators:

- `login_required` – Restricts access to authenticated users.
- `role_required` – Restricts access to users with specified roles.

### Dashboard

After successful login, users are redirected to the dashboard, which provides the application navigation interface.

## 7. Database Design

The application uses SQLite as its relational database.

### Main Tables

| Table | Purpose |
|---|---|
| `users` | Stores staff usernames, password hashes and roles. |
| `patients` | Stores patient demographic and contact information. |
| `appointments` | Stores appointment details and status. |
| `medical_history` | Stores diagnoses, symptoms and clinical notes. |
| `prescriptions` | Stores medication and prescription details. |

### Main Relationships

1. One patient can have multiple appointments.
2. One patient can have multiple medical history records.
3. One patient can have multiple prescriptions.
4. One medical history record can have multiple prescriptions.
5. Each prescription references the patient and the associated medical history record.

Foreign-key constraints and database triggers help maintain referential integrity.

## 8. Security and Validation

The application implements several security and data-integrity measures:

- Password hashing using Werkzeug.
- Session-based authentication.
- Role-based authorization decorators.
- Server-side form validation.
- Parameterized SQL queries to reduce SQL injection risk.
- SQLite foreign-key enforcement.
- Database triggers for prescription-to-history consistency.
- Unique constraints and indexes to prevent duplicate usernames and scheduled doctor-slot conflicts.
- POST requests for state-changing operations such as deletion and appointment status updates.

## 9. Technology Stack

| Technology | Usage |
|---|---|
| Python | Backend programming language |
| Flask | Web application framework |
| SQLite | Relational database |
| HTML | Page structure |
| CSS | Interface styling |
| JavaScript | Client-side functionality |
| Bootstrap | Responsive user interface |
| Jinja2 | Server-side HTML templating |
| Werkzeug | Password hashing and verification |
| Git and GitHub | Version control and collaboration |
| Pytest | Automated testing |

## 10. Application Workflows

### Patient Registration Workflow

1. Staff member opens the patient management page.
2. Patient details are entered.
3. The server validates the submitted data.
4. Patient details are inserted into SQLite.
5. A unique patient code is generated.
6. A success message is displayed.

### Appointment Booking Workflow

1. Staff member opens appointment management.
2. An existing patient is selected.
3. Doctor, date, time and appointment reason are entered.
4. The server validates the appointment.
5. SQLite checks the scheduled doctor time-slot constraint.
6. The appointment is saved if no conflict exists.

### Medical Record Workflow

1. An authorized user selects a patient.
2. Medical history details are recorded.
3. A prescription can be created against the corresponding history record.
4. Database foreign keys and triggers maintain patient-record consistency.
5. Authorized users can view and edit records.

### Authentication Workflow

1. Staff member opens the login page.
2. Username and password are submitted.
3. The stored password hash is verified.
4. A valid user receives an authenticated session.
5. The user is redirected to the dashboard.
6. Protected operations verify authentication and role permissions.

## 11. Testing

The project includes automated tests for application functionality and access permissions.

The test suite is executed using:

```powershell
python -m pytest -q
```

The test suite passed with **107 tests** during the November 6, 2026 integration verification.

Testing covers application behavior and permission-related functionality. The test suite should be executed again after subsequent code changes.

## 12. Limitations and Future Enhancements

Potential future improvements include:

- More granular role-based restrictions for all patient and appointment operations.
- Enhanced audit logging for changes to sensitive records.
- Automated appointment reminders.
- Improved reporting and analytics.
- Production-grade deployment configuration.
- Stronger session and CSRF protections.

## 13. Conclusion

The Healthcare Appointment and Patient Record Manager integrates patient registration, appointment scheduling, medical record management and staff authentication into a single Flask application.

Its modular organization, relational database constraints, input validation and automated tests support maintainability and data consistency. The project is developed for academic purposes and is not intended to replace a clinically validated healthcare information system.
