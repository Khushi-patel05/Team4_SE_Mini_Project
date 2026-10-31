# Reflection — Static Code Analysis

### 1. What is the importance of static code analysis?

Static code analysis helps identify potential bugs, security vulnerabilities, and coding-standard violations without executing the program. In this project, Pylint, Bandit, and Flake8 helped improve the code quality, security, and readability of the hostel room allocation system.

### 2. What issues did you identify and fix in your code?

I fixed several issues, including unsafe YAML deserialization, a hardcoded database password, incorrect room capacity validation, missing gender restrictions during room allocation, duplicate student allocations, and inconsistent room occupancy records. I also improved function naming, documentation, and formatting.

### 3. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks code quality, potential programming errors, and coding conventions. Bandit identifies potential security vulnerabilities in Python code. Flake8 checks Python code for style violations and common programming errors. Using all three tools provides complementary checks.

### 4. What did you learn from this lab?

I learned that static analysis can identify problems before a program is executed. I also learned that security, correctness, and readability are all important aspects of software development. After fixing the issues, my code achieved a Pylint score of 10.00/10, Bandit reported no issues, and Flake8 reported no violations.