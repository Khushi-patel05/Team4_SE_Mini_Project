# Static Code Analysis – Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command execution using os.system() | High – Security (Bandit B605) | 43 | Executes a shell command using user-influenced file input, creating a potential command injection vulnerability. It also uses the Unix-only `cat` command, which fails on Windows. | Remove `os.system()` and use Python file handling to read and display the log. |
| Invalid time slot accepted | Medium – Functional | 49 | The program accepts the time slot `14-12`, resulting in a negative duration of -2 hours. | Validate time-slot format and ensure the end time is later than the start time. |
| Non-string time slot accepted | Medium – Functional | 50 | The program accepts an integer (`1530`) as a time slot, which can cause errors when the slot is processed. | Validate input types and reject invalid time-slot values. |
| Bare except with pass | Low – Security/Quality (Bandit B110) | 27–28 | The cancellation function catches every exception and silently ignores it, hiding unexpected errors. | Handle the specific exception or explicitly check whether the reservation exists. |
| Mutable default argument | Code Quality (Pylint W0102) | 11 | The function uses an empty list as a default argument. Mutable defaults can cause unexpected shared state between function calls. | Use `None` as the default and initialize a new list inside the function. |
| Missing documentation and naming conventions | Code Quality (Pylint) | 1, 11, 39 | The module and functions lack docstrings, and `logConflicts` does not follow Python's snake_case naming convention. | Add appropriate docstrings and rename the function using snake_case. |
| Formatting violations and unused variables | Style (Flake8) | 11–59 | The file contains long lines, insufficient blank lines, and unused local variables. | Apply PEP 8 formatting and remove unused variables. |

