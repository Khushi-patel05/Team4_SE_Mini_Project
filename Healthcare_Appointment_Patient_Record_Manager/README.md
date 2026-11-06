# Healthcare Appointment and Patient Record Manager

A Flask-based healthcare management application designed to help small clinics manage patient information, appointments, medical histories, and prescriptions through a centralized system.

## Project Overview

The Healthcare Appointment and Patient Record Manager (HAPRM) provides a centralized platform for managing essential clinic operations.

The application supports patient registration and record management, appointment scheduling, medical history documentation, prescription management, and user authentication.

The project demonstrates CRUD operations, database management, input validation, role-based access control, and software engineering practices.

## Key Features

### 1. Patient Management
- Register new patients with validated details.
- Generate unique patient codes automatically.
- Search patients using their name, patient code, or phone number.
- View, update, and delete patient records.

### 2. Appointment Management
- Schedule appointments for registered patients.
- View and filter appointment records.
- Reschedule scheduled appointments.
- Update appointment status to Completed or Cancelled.
- Prevent double-booking of a doctor's scheduled time slot.

### 3. Medical History Management
- Maintain patient medical histories.
- Record diagnosis, symptoms, and clinical notes.
- View, edit, and delete medical history records.

### 4. Prescription Management
- Create prescriptions linked to patients and their medical history.
- Store medication name, dosage, frequency, and duration.
- Maintain relationships between patients, medical histories, and prescriptions.

### 5. Authentication and Access Control
- User login and logout.
- Password hashing for secure password storage.
- Role-based access control for Administrator, Doctor, and Receptionist.
- Administrator-only staff account management.
- Session-based authentication.

### 6. Data Validation and Integrity
- Validate patient and appointment inputs.
- Use parameterized SQL queries.
- Enforce database foreign key relationships.
- Prevent conflicting scheduled appointments using a unique database index.
- Use database triggers to validate prescription and medical history relationships.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Backend | Python, Flask |
| Database | SQLite |
| Database Access | Python SQLite3 |
| Authentication | Flask Sessions, Werkzeug Security |
| Testing | Pytest |
| Version Control | Git and GitHub |
| Development Environment | Visual Studio Code |

## Project Modules

1. **Patient Management** – Patient registration, validation, searching, and record management.
2. **Appointment Management** – Appointment scheduling, listing, rescheduling, and status management.
3. **Medical History and Prescription Management** – Clinical history and prescription records.
4. **Authentication, Dashboard, and Integration** – Login, role-based access, staff management, and application integration.

## Database

The application uses SQLite for persistent data storage.

The main database tables include:

- `users` – Stores user accounts, password hashes, and roles.
- `patients` – Stores patient information.
- `appointments` – Stores appointment details and status.
- `medical_history` – Stores diagnoses, symptoms, and clinical notes.
- `prescriptions` – Stores medication and prescription details.

The database uses primary keys, foreign keys, constraints, indexes, and triggers to maintain data integrity.

## Project Structure

```text
Healthcare_Appointment_Patient_Record_Manager/
│
├── app.py
├── auth.py
├── config.py
├── requirements.txt
├── installation.md
├── README.md
│
├── medical_records/
│   ├── models.py
│   └── routes.py
│
├── templates/
│   ├── auth/
│   ├── ...
│
├── static/
├── tests/
├── docs/
│   └── FEATURES_AND_MODULES.md
│
└── instance/
    └── healthcare.db
```

## Installation and Execution

Refer to [installation.md](installation.md) for complete setup instructions, dependencies, database initialization, application execution, and troubleshooting.

To run the application after completing the setup:

```bash
python app.py
```

Open the application at:

```text
http://127.0.0.1:5000/
```

Health check endpoint:

```text
http://127.0.0.1:5000/health
```

## Testing

The project uses Pytest for automated testing.

Run the test suite using:

```bash
python -m pytest -q
```

The project test suite recorded **107 passing tests** during the November 2026 verification.

## Software Engineering Deliverables

- Software Requirements Specification (SRS)
- Software Architecture and Design Specification (SAD)
- Software Test Plan (STP)
- UML diagrams and requirements traceability
- Test cases and test results
- Project setup and installation documentation
- Application features and modules documentation

## Additional Documentation

- [Project Installation Guide](installation.md)
- [Application Features and Modules](docs/FEATURES_AND_MODULES.md)

## Team Collaboration

The project is developed collaboratively using Git and GitHub. Team members work on assigned modules using feature branches and pull requests for integration.

## Disclaimer

This project is intended for academic purposes. Use fictional patient data during development and testing. It is not intended to replace a clinically validated healthcare information system.

## Team Members

1. KARANAM SREEHITHA - PES1UG24AM129
2. KHUSHI PATEL - PES1UG24AM134
3. KIRTHANA S - PES1UG24AM136
4. PORLA NEHA - PES1UG25AM808
