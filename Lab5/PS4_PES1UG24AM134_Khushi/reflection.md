# Lab 5: Static Code Analysis – Reflection

### 1. What is static code analysis, and why is it important?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, coding mistakes, and style violations early in development. It improves code quality, reliability, security, and maintainability.

### 2. What are the differences between Pylint, Bandit, and Flake8?

- **Pylint:** Checks code quality, naming conventions, documentation, unused variables, and programming practices.
- **Bandit:** Identifies potential security vulnerabilities and unsafe coding patterns.
- **Flake8:** Checks Python code against PEP 8 guidelines, including formatting, whitespace, and line length.

Each tool focuses on a different aspect of code quality.

### 3. What issues did you identify and fix in your program?

The original room scheduler contained several issues:

- A mutable default argument in the `schedule_room()` function.
- A bare exception that silently ignored errors.
- Unsafe shell command execution using `os.system()`.
- Invalid time slots that could produce negative durations.
- Missing documentation and inconsistent naming conventions.
- Formatting violations and unused variables.

I fixed these issues by improving input validation, using safer file handling, adding documentation, correcting naming conventions, and following Python formatting standards.

### 4. How did static code analysis improve your program?

Static code analysis helped me identify problems that were not immediately obvious during program execution. Pylint improved the code quality, Bandit helped eliminate security vulnerabilities, and Flake8 ensured consistent formatting.

After making the changes, the Pylint score improved from 5.60/10 to 10.00/10. Bandit reported zero security issues, and Flake8 reported zero violations. The program also continued to execute successfully.