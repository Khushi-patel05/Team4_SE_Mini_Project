# Healthcare Appointment and Patient Record Manager

A Flask-based healthcare management application designed to help small clinics manage patient information, appointments, medical histories, and prescriptions.

## 1. Project Overview

The Healthcare Appointment and Patient Record Manager provides a centralized application for managing routine clinic operations.

The project focuses on CRUD (Create, Read, Update, Delete) operations, authentication, data validation, database management, modular design, and software engineering practices.

## 2. Key Features

- **Patient Management:** Register patients, view patient details, update information, and search records.
- **Appointment Management:** Schedule, view, reschedule, and cancel appointments.
- **Medical Records:** Maintain patient medical histories and clinical records.
- **Prescription Management:** Create and manage prescriptions associated with medical records.
- **Authentication and Access Control:** Support login and role-based user accounts.
- **Data Validation:** Validate user inputs and handle invalid operations.
- **Database Management:** Store application data using SQLite.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS |
| Backend | Python, Flask |
| Database | SQLite |
| Testing | Pytest |
| Version Control | Git, GitHub |
| CI | GitHub Actions |
| Development Environment | Visual Studio Code |

## 4. Project Structure

```text
Team4_SE_Mini_Project/
│
├── .github/
│   └── workflows/
│       └── healthcare-tests.yml
│
├── docs/
│   ├── Team4_SRS.pdf
│   ├── Team4_SAD.pdf
│   └── Team4_STP.pdf
│
├── Healthcare_Appointment_Patient_Record_Manager/
│   ├── app.py
│   ├── auth.py
│   ├── config.py
│   ├── create_admin.py
│   ├── create_staff.py
│   ├── requirements.txt
│   ├── medical_records/
│   ├── templates/
│   ├── static/
│   ├── tests/
│   └── instance/
│
├── Lab1/
├── Lab2/
├── Lab3/
├── Lab4/
├── Lab5/
│
└── README.md
```

*The structure above highlights the main project directories and files.*

## 5. Installation and Setup

### Prerequisites

- Python 3.11 or a compatible Python version
- Git
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/Khushi-patel05/Team4_SE_Mini_Project.git
cd Team4_SE_Mini_Project
```

### Step 2: Navigate to the application directory

```bash
cd Healthcare_Appointment_Patient_Record_Manager
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install the testing dependency:

```bash
pip install pytest
```

## 6. Configuration

The application uses `config.py` to configure its database location and secret key.

The SQLite database is stored at:

```text
instance/healthcare.db
```

The application reads its secret key from the `SECRET_KEY` environment variable. If it is not provided, the development fallback key in `config.py` is used.

For local development on Windows PowerShell, generate a secret key:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Set the generated value:

```powershell
$env:SECRET_KEY = "paste-your-generated-secret-here"
```

For deployment, configure a secure secret key through the deployment environment rather than relying on the development fallback.

## 7. Creating User Accounts

### Create an Administrator account

Run:

```bash
python create_admin.py
```

Enter the administrator username, password, and password confirmation when prompted.

### Create a Doctor or Receptionist account

Run:

```bash
python create_staff.py
```

Choose the appropriate role when prompted:

1. Doctor
2. Receptionist

The account creation process validates the provided details before creating the user.

## 8. Running the Application

From the application directory, run:

```bash
python app.py
```

Open the local address displayed by Flask in your browser. The default Flask development server typically uses:

```text
http://127.0.0.1:5000/
```

Log in using an account created through the account creation scripts.

**Note:** The built-in Flask development server is intended for local development and testing, not production deployment.

## 9. Running Tests

From the application directory, activate the virtual environment and execute:

```bash
python -m pytest -q
```

The tests cover application functionality, including authentication, patient management, appointments, medical records, and end-to-end workflows.

## 10. Continuous Integration

The repository includes a GitHub Actions workflow:

```text
.github/workflows/healthcare-tests.yml
```

The workflow:

- Runs on pushes to `main`.
- Runs on pull requests targeting `main`.
- Uses Python 3.11.
- Installs application dependencies and Pytest.
- Executes the automated test suite.

This helps verify application functionality during collaborative development.

## 11. Software Engineering Deliverables

The project includes the following documentation and engineering activities:

- Software Requirements Specification (SRS)
- Software Architecture Document (SAD)
- Software Test Plan (STP)
- UML diagrams and requirements documentation
- Test cases and automated testing
- GitHub-based version control and collaboration
- Continuous integration using GitHub Actions

## 12. Team Collaboration

The project is developed collaboratively by Team 4 using Git and GitHub.

Team members:

1. **KARANAM SREEHITHA** – PES1UG24AM129
2. **KHUSHI PATEL** – PES1UG24AM134
3. **KIRTHANA S** – PES1UG24AM136
4. **PORLA NEHA** – PES1UG25AM808

Development tasks are divided among team members, with changes integrated through branches and pull requests.

## 13. Project Disclaimer

This application is developed for academic purposes. Use fictional patient information during development and testing. It is not intended to replace a clinically validated healthcare information system.