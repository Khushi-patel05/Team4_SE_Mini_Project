# Lab 5 – Static Code Analysis

## 1. Student Details

- **Name:** Kirthana S
- **SRN:** PES1UG24AM136
- **Section:** 5 C
- **Scenario:** Recruitment Tracker

## 2. Project Overview

The Recruitment Tracker is a Python application that manages applicant information using an SQLite database. It allows users to add applicants, shortlist candidates based on their expected salary, update application status, export applicant details and count applicants by status.

## 3. Objectives

- Analyse the Python application using static code analysis tools.
- Identify security vulnerabilities and code quality issues.
- Correct the identified issues.
- Verify the corrected application using Pylint, Bandit and Flake8.

## 4. Tools and Technologies

| Tool | Purpose |
|---|---|
| Python 3.12.6 | Programming language |
| SQLite3 | Database management |
| Pylint | Code quality analysis |
| Bandit | Security vulnerability analysis |
| Flake8 | Coding style and formatting checks |
| Visual Studio Code | Code editing and execution |

## 5. Issues Identified and Corrections

The initial analysis identified SQL injection risks, unsafe use of `eval()`, silent exception handling, missing docstrings, inconsistent function naming, unused variables, inconsistent return statements and formatting issues.

The following corrections were made:

- Replaced dynamically constructed SQL queries with parameterized queries.
- Removed `eval()` and used a numeric salary limit.
- Removed unnecessary silent exception handling.
- Added module and function docstrings.
- Renamed functions using snake_case.
- Removed unused variables.
- Improved return statements and file handling.
- Corrected line length, whitespace and indentation issues.

Refer to `issues.md` for the detailed list of identified issues and their corrections.

## 6. Final Static Analysis Results

| Analysis Tool | Final Result |
|---|---|
| Pylint | 10.00/10 |
| Bandit | 0 findings |
| Flake8 | 0 violations |

The final reports are included in this folder for verification.

## 7. Files Included

| File | Description |
|---|---|
| `recruitment_tracker.py` | Corrected Python application |
| `issues.md` | Issues identified and corrections |
| `reflection.md` | Lab reflection and conceptual questions |
| `pylint_before.txt` | Initial Pylint report |
| `pylint_after.txt` | Final Pylint report |
| `bandit_before.txt` | Initial Bandit report |
| `bandit_after.txt` | Final Bandit report |
| `flake8_before.txt` | Initial Flake8 report |
| `flake8_after.txt` | Final Flake8 report |

## 8. Functional Verification

The corrected application was executed successfully.

**Output:**

```text
['Nina']
2 in interview
```

The output confirms that applicant shortlisting and applicant status counting work as expected.

## 9. Conclusion

Static code analysis helped improve the security, readability and maintainability of the Recruitment Tracker application. After correcting the identified issues, the application achieved a Pylint score of 10.00/10, zero Bandit findings and zero Flake8 violations.