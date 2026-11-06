# Healthcare Appointment and Patient Record Manager
# Installation and Setup Guide

## 1. Project Overview

The Healthcare Appointment and Patient Record Manager is a Flask-based web application designed to help clinics manage patient information, appointments, medical histories, and prescriptions.

This guide explains how to install dependencies, configure the environment, initialize the database, run the application, and execute automated tests.

## 2. Prerequisites

Install the following software before setting up the project:

| Software | Requirement |
|---|---|
| Python | 3.9 or newer |
| Git | Required |
| Visual Studio Code | Recommended |
| Web browser | Chrome, Firefox, or Edge |

SQLite is included with Python and does not require a separate database server installation.

## 3. Clone the Repository

Open PowerShell or a terminal and execute:

```powershell
git clone https://github.com/Khushi-patel05/Team4_SE_Mini_Project.git
```

Navigate to the project directory:

```powershell
cd Team4_SE_Mini_Project/Healthcare_Appointment_Patient_Record_Manager
```

## 4. Create a Virtual Environment

Create an isolated Python environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run the following command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

## 5. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the application dependencies:

```powershell
python -m pip install -r requirements.txt
```

The current requirements file specifies Flask 3.1 or newer, below version 4.0.

For running the automated test suite, install pytest separately:

```powershell
python -m pip install pytest
```

## 6. Environment Configuration

The project uses `config.py` to manage application configuration.

The database configuration is:

- Database directory: `instance/`
- Database filename: `healthcare.db`
- Database path: `instance/healthcare.db`

The application automatically creates the `instance` directory if it does not exist.

The Flask secret key is read from the `SECRET_KEY` environment variable. If it is not provided, the project currently uses a development fallback key.

For local development, a secret key can be configured in PowerShell:

```powershell
$env:SECRET_KEY = "replace-with-a-long-random-secret"
```

Use a secure, private secret key and never commit production secrets to GitHub.

## 7. Database Initialization

The application uses SQLite for persistent data storage.

Database initialization is handled by the application code:

1. Authentication database initialization is performed during application setup.
2. Patient and appointment tables are created if they do not already exist.
3. A unique index prevents duplicate scheduled appointments for the same doctor, date, and time.
4. Medical history and prescription database initialization is handled by the medical records module.
5. SQLite foreign-key enforcement is enabled when database connections are created.

The database is initialized automatically when the application starts. No separate database server or manual database creation command is required.

## 8. Run the Application

Make sure the virtual environment is activated.

Start the Flask application:

```powershell
python app.py
```

The development server will start.

Open the following address in your web browser:

```text
http://127.0.0.1:5000/
```

The application redirects authenticated users to the patient management section.

## 9. Application Health Check

The application provides a health-check endpoint.

Open:

```text
http://127.0.0.1:5000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

## 10. Run Automated Tests

To execute the project's automated tests, make sure pytest is installed and the virtual environment is active.

Run:

```powershell
python -m pytest -q
```

The command executes the available test suite and displays a summary of passed and failed tests.

## 11. Common Installation Issues

### Issue 1: Python is not recognized

**Solution:**

Install Python and ensure that Python is added to the system PATH. Restart the terminal and verify:

```powershell
python --version
```

### Issue 2: Virtual environment activation is blocked

**Solution:**

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### Issue 3: Flask module not found

**Solution:**

Activate the virtual environment and install the requirements:

```powershell
python -m pip install -r requirements.txt
```

### Issue 4: Database directory or file is missing

**Solution:**

The application automatically creates the `instance` directory and initializes the database during startup. Check the terminal for database errors if initialization fails.

### Issue 5: Port 5000 is already in use

**Solution:**

Stop the other application using port 5000 before starting this application again.

## 12. Important Notes

- Use fictional patient information during development and testing.
- Do not expose the Flask development server to public networks.
- Do not use the default development secret key in production.
- Back up the SQLite database before making changes to important records.
- The application is intended for academic purposes and is not a clinically validated healthcare system.

## 13. Project Repository

GitHub Repository:

https://github.com/Khushi-patel05/Team4_SE_Mini_Project

Project Directory:

`Healthcare_Appointment_Patient_Record_Manager`
