# Issues Identified and Fixed

## 1. Security Issues – Bandit

| Issue | Severity | Problem Identified | Correction |
|---|---|---|---|
| SQL Injection (B608) | Medium | SQL queries used f-strings to insert applicant details directly into the query. | Replaced f-strings with parameterized SQL queries. |
| Unsafe eval() (B307) | Medium | eval() was used to execute the salary expression. | Replaced eval() with a numeric salary limit. |
| Silent Exception Handling (B110) | Low | A broad exception was caught and silently ignored. | Removed the unnecessary exception handler and silent pass statement. |

## 2. Code Quality Issues – Pylint

| Issue | Problem Identified | Correction |
|---|---|---|
| Missing docstrings | Module and functions lacked documentation. | Added module and function docstrings. |
| Invalid function names | Functions used CamelCase naming. | Renamed functions using snake_case. |
| Inconsistent return statements | shortlist() did not return a value on every execution path. | Modified it to consistently return a list. |
| Unused variable | total_seen was assigned but never used. | Removed the unused variable. |
| File handling | File was opened without a context manager or explicit encoding. | Used a context manager, UTF-8 encoding and CSV writer. |
| Long lines and indentation | Statements exceeded line-length limits or had inconsistent indentation. | Reformatted the source code. |

## 3. Formatting Issues – Flake8

| Issue | Description | Correction |
|---|---|---|
| E501 | Lines exceeded the allowed length. | Wrapped long statements. |
| F841 | Unused local variable. | Removed the variable. |
| W291 | Trailing whitespace. | Removed unnecessary whitespace. |
| E302 | Incorrect spacing before a function definition. | Applied the required blank lines. |

## 4. Final Verification

The corrected application was analysed using all three tools.

- **Pylint:** 10.00/10
- **Bandit:** 0 findings
- **Flake8:** 0 violations

The application was also executed successfully after the corrections.