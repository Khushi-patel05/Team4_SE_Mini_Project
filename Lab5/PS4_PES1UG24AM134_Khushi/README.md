# Lab 5 – Static Code Analysis

## 1. Objective

The objective of this lab is to analyse and improve the quality, security, and maintainability of a Python application using static code analysis tools.

The Room Scheduler application was analysed using three tools:

- **Pylint** – Identifies code-quality issues and evaluates Python code.
- **Bandit** – Detects potential security vulnerabilities in Python code.
- **Flake8** – Checks Python coding style and formatting violations.

The identified issues were corrected, and all three tools were executed again to verify the improvements.

## 2. Project Overview

The project contains a Python-based Room Scheduler application.

The application demonstrates the following functionality:

- Room reservation and scheduling.
- Equipment allocation.
- Reservation cancellation.
- Time-slot validation.
- Detection and logging of scheduling conflicts.
- Exporting reservation details to a JSON file.

**Main source file:** `scheduler_system.py`

## 3. Tools and Environment

| Component | Version |
|---|---|
| Python | 3.11.8 |
| Pylint | 4.1.3 |
| Bandit | 1.9.4 |
| Flake8 | 7.5.0 |
| Editor | Visual Studio Code |
| Operating System | Windows |

## 4. Installation and Execution

### Step 1: Install the required tools

```bash
pip install pylint bandit flake8
```

### Step 2: Run the application

```bash
python scheduler_system.py
```

### Step 3: Run Pylint

```bash
pylint scheduler_system.py
```

### Step 4: Run Bandit

```bash
bandit -r scheduler_system.py
```

### Step 5: Run Flake8

```bash
flake8 scheduler_system.py
```

## 5. Issues Identified and Fixed

The following issues were identified during static analysis:

| Issue | Correction |
|---|---|
| Unsafe shell command execution | Replaced `os.system()` with Python file handling. |
| Bare exception handling | Used specific exception types and descriptive error handling. |
| Mutable default argument | Replaced the mutable list default with `None`. |
| Invalid time slots | Added time-slot format and range validation. |
| File handling issues | Used context managers and UTF-8 encoding. |
| Naming and documentation issues | Improved function naming and added docstrings. |
| Formatting violations | Corrected spacing, line lengths and unused variables. |

## 6. Static Analysis Results

### Initial Results

| Tool | Initial Result |
|---|---|
| Pylint | 5.60/10 |
| Bandit | 2 security findings |
| Flake8 | 13 violations |

### Final Results

| Tool | Final Result | Status |
|---|---|---|
| Pylint | 10.00/10 | Passed |
| Bandit | 0 issues identified | Passed |
| Flake8 | 0 violations | Passed |

The final results demonstrate improvements in code quality, security and formatting.

## 7. Files Included

| File | Description |
|---|---|
| `scheduler_system.py` | Corrected Room Scheduler source code |
| `issues.md` | Summary of identified issues and their severity |
| `reflection.md` | Reflection on static code analysis |
| `pylint_before.txt` | Initial Pylint report |
| `pylint_after.txt` | Final Pylint report |
| `bandit_before.txt` | Initial Bandit report |
| `bandit_after.txt` | Final Bandit report |
| `flake8_before.txt` | Initial Flake8 report |
| `flake8_after.txt` | Final Flake8 report |

## 8. Conclusion

The Room Scheduler application was successfully analysed and improved using Pylint, Bandit and Flake8.

The corrections addressed code-quality issues, potential security risks, input validation and formatting problems.

The final application achieved a Pylint score of **10.00/10**, had **zero Bandit findings**, and produced **zero Flake8 violations**.

The corrected program was also executed successfully to verify its functionality.

## 9. Repository Information

**Submission Directory:**

```text
Lab5/
└── PS4_PES1UG24AM134_Khushi/
    ├── README.md
    ├── scheduler_system.py
    ├── issues.md
    ├── reflection.md
    ├── pylint_before.txt
    ├── pylint_after.txt
    ├── bandit_before.txt
    ├── bandit_after.txt
    ├── flake8_before.txt
    └── flake8_after.txt
```
