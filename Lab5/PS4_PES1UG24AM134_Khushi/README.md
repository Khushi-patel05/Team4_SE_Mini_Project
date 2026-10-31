# Lab 5 – Static Code Analysis
## Hostel Room Allocation System

### 1. Project Overview
This project demonstrates static code analysis and code-quality improvement for a Python-based Hostel Room Allocation System. The program manages room allocation, occupant information, fee calculation, priority-based allocation, lottery allocation, and waitlist information.

The source code was analysed using **Pylint, Bandit, and Flake8** to identify code-quality, security, and formatting issues.

### 2. Objectives
- Analyse the Python source code using Pylint, Bandit, and Flake8.
- Identify code-quality issues, potential security risks, and formatting violations.
- Apply corrections to improve code readability, maintainability, and security.
- Run the analysis tools after the corrections.
- Maintain before-and-after reports as evidence of the analysis.

### 3. Technologies and Tools

| Tool | Purpose |
|---|---|
| Python | Implementation of the hostel allocation program |
| Pylint | Code-quality analysis |
| Bandit | Python security analysis |
| Flake8 | Style and formatting checks |
| Git and GitHub | Version control and submission |

### 4. Project Structure

```text
PS4_PES1UG25AM808_PorlaNeha/
├── README.md
├── hostel_allocation.py
├── issues.md
├── reflection.md
├── pylint_report_before.txt
├── pylint_report_after.txt
├── bandit_report_before.txt
├── bandit_report_after.txt
├── flake8_report_before.txt
└── flake8_report_after.txt
```

### 5. Static Analysis Commands

Run the following commands from the project directory.

**Pylint**
```bash
python -m pylint hostel_allocation.py
```

**Bandit**
```bash
python -m bandit -r hostel_allocation.py
```

**Flake8**
```bash
python -m flake8 hostel_allocation.py
```

### 6. Reports

The repository contains the analysis reports generated before and after the corrections.

| Tool | Before report | After report |
|---|---|---|
| Pylint | `pylint_report_before.txt` | `pylint_report_after.txt` |
| Bandit | `bandit_report_before.txt` | `bandit_report_after.txt` |
| Flake8 | `flake8_report_before.txt` | `flake8_report_after.txt` |

These reports provide evidence of the issues identified during static analysis and the results of the subsequent checks.

### 7. Program Execution

Run the application using:

```bash
python hostel_allocation.py
```

The program displays room information, student allocations, occupant lists, fee calculations, allocation priorities, lottery results, database connection information, and waitlist status.

### 8. Version Control

The Lab 5 work is maintained in the team repository under:

`Lab5/PS4_PES1UG25AM808_PorlaNeha/`

The following commits are present on the `main` branch:

1. `Fix code quality issues identified by Pylint`
2. `Fix security issues identified by Bandit`
3. `Fix formatting issues identified by Flake8`

**Note:** The Pylint and Bandit commits currently contain no file changes; their commit messages were created after the corresponding files were already present on `main`. The Flake8 commit adds `reflection.md`.

### 9. Conclusion

This project demonstrates the use of Pylint, Bandit, and Flake8 to analyse a Python application. The source code and reports are maintained in the repository to document the static analysis workflow and its results.
