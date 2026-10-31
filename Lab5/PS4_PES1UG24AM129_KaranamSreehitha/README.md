# Lab 5 – Static Code Analysis

## Objective
To analyse and improve the quality, security and formatting of a Python application using Pylint, Bandit and Flake8.

## Project Description
This project analyses a Campus Shuttle System implemented in Python. The program manages shuttle routes, passenger trip records, driver assignments and fleet data using JSON.

## Tools Used
- Python 3.11.9
- Pylint
- Bandit
- Flake8
- Visual Studio Code
- Git and GitHub

## Execution

Run the application:

```bash
python shuttle_system.py
```

## Static Analysis Commands

```bash
pylint shuttle_system.py
bandit shuttle_system.py
flake8 shuttle_system.py
```

## Final Results

| Tool | Result |
|---|---|
| Pylint | 10.00/10 |
| Bandit | No issues identified |
| Flake8 | No violations |

## Folder Structure

- `shuttle_system.py` – Corrected Python program.
- `shuttle_system_original.py` – Original Python program.
- `reports/before/` – Initial analysis reports.
- `reports/after/` – Final analysis reports.
- `documentation/issues.md` – Identified issues and corrections.
- `documentation/reflections.md` – Lab reflections.
- `Lab5_Report.pdf` – Complete report with screenshots.

## Conclusion
The program was improved by resolving the issues identified through static code analysis. The final results demonstrate improvements in code quality, security and formatting.
