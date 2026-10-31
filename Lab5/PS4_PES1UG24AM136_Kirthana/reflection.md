# Lab 5 – Reflection

## 1. What is Static Code Analysis?

Static code analysis is the process of examining source code without executing the program. It helps identify potential errors, security vulnerabilities and coding standard violations before the software is deployed.

## 2. What is the Difference Between Pylint, Bandit and Flake8?

- **Pylint:** Checks overall Python code quality, including naming conventions, documentation, unused variables and possible programming issues.
- **Bandit:** Focuses on identifying common security vulnerabilities in Python applications.
- **Flake8:** Checks coding style and formatting, including line length, whitespace and unused code.

## 3. What Issues Were Identified in the Recruitment Tracker?

The original program contained SQL injection risks, unsafe use of eval(), silent exception handling, missing documentation, inconsistent naming conventions, unused variables, inconsistent return statements, and file-handling and formatting issues.

## 4. How Did Static Code Analysis Improve the Application?

The analysis tools helped identify and correct security and maintainability problems. Parameterized SQL improved database query safety, while removing eval() prevented arbitrary expression execution. Better documentation, naming conventions and file handling improved readability and maintainability.

The final application achieved a Pylint score of 10.00/10, zero Bandit findings and zero Flake8 violations. Its functionality was also verified through successful execution.