\# Lab 5 – Static Code Analysis

\## Issue Identification and Resolution



\### 1. Pylint Findings



| Issue | Code | Problem | Resolution |

|---|---|---|---|

| Missing module docstring | C0114 | Module lacked documentation | Added module docstring |

| Missing function docstrings | C0116 | Functions lacked descriptions | Added function docstrings |

| Mutable default argument | W0102 | Used an empty list as default | Replaced with None |

| String formatting | C0209 | Used regular string formatting | Replaced with f-string |

| Bare exception | W0702 | Used unspecified exception handling | Removed silent exception handling |

| Invalid function naming | C0103 | Used camelCase | Changed to snake\_case |

| Unused argument | W0613 | Route argument was unused | Used route ID for validation |

| Global statement | W0603 | Modified global state unnecessarily | Removed global statement |

| Missing encoding | W1514 | File opened without encoding | Specified UTF-8 |

| Unsafe file handling | R1732 | Files were not closed safely | Used context managers |



\### 2. Bandit Findings



| Issue | Code | Severity | Resolution |

|---|---|---|---|

| Silent exception handling | B110 | Low | Removed try-except-pass pattern |

| Standard pseudo-random generator | B311 | Low | Replaced random.choice with secrets.choice |



\### 3. Flake8 Findings



| Issue | Code | Resolution |

|---|---|---|

| Missing blank lines | E302 | Added required blank lines |

| Long line | E501 | Wrapped long statement |

| Bare except | E722 | Removed bare exception |

| Missing blank lines after function | E305 | Corrected spacing |



\### 4. Additional Functional Improvements



\- Added validation for passenger counts.

\- Rejected negative passenger counts.

\- Rejected non-integer passenger counts.

\- Added handling for unavailable routes.

\- Prevented division by zero for routes without trips.

\- Improved JSON file handling.



\### 5. Final Results



| Tool | Before | After |

|---|---|---|

| Pylint | 6.25/10 | 10.00/10 |

| Bandit | 2 low-severity findings | 0 findings |

| Flake8 | 10 violations | 0 violations |

