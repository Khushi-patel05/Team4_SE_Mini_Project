# Static Code Analysis — Issues and Fixes

The original `hostel_allocation.py` file was analyzed using Pylint, Bandit, and Flake8. The following issues were identified and fixed.

| Issue | Type / Severity | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe YAML deserialization | Security — High | Original `load_config()` | `yaml.load()` with the unsafe `yaml.Loader` could allow unsafe object construction from untrusted YAML input. | Replaced it with `yaml.safe_load()`. |
| Hardcoded database password | Security — High | Original `connectWardenDb()` | A database password was written directly in the source code. | Read the password from the `WARDEN_DB_PASSWORD` environment variable instead. |
| Flask debug mode enabled | Security — Medium | Original `app.run()` | Running Flask with debug mode enabled can expose sensitive debugging functionality. | Changed the application to run with `debug=False`. |
| Remote logging configuration listener | Security — Medium | Original logging configuration | A remote logging configuration listener could expose a security risk if accessible to untrusted users. | Disabled the listener and logged a warning instead. |
| Incorrect room capacity condition | Logic — Medium | Original `allocateRoom()` | The capacity check used `>` instead of `>=`, which could allow a room to exceed its capacity. | Changed the condition to skip a room when its occupancy is greater than or equal to capacity. |
| Gender restriction not enforced | Logic — Medium | Original `allocateRoom()` | The allocation logic did not ensure that the student's gender matched the room's designated gender. | Added a gender check before allocating a room. |
| Duplicate student allocation | Logic — Medium | Original `allocateRoom()` | A student could be allocated more than once, causing inconsistent allocation records. | Checked existing allocations before creating a new allocation. |
| Room occupancy not updated when vacating | Logic — Medium | Original `vacateRoom()` | Removing a student from the allocation dictionary did not remove them from the room's occupant list. | Updated both the allocation dictionary and room occupant list. |
| Mutable default argument | Code quality — Low | Original `allocateRoom()` | Using `preferred=[]` as a default argument could cause the same list to be shared between function calls. | Changed the default to `None` and initialized the list inside the function. |
| Incorrect priority ordering | Logic — Low | Original `priorityOrder()` | Students were sorted in ascending year order instead of prioritizing senior students. | Sorted students by year in descending order. |
| Incorrect vacant-bed count | Logic — Low | Original `vacantBeds()` | The function counted vacant rooms rather than the total number of unoccupied beds. | Calculated vacant beds using room capacity minus current occupancy. |
| Inconsistent naming and missing documentation | Code quality — Low | Multiple functions | Some functions used inconsistent naming conventions and lacked docstrings. | Used consistent `snake_case` names and added docstrings. |
| Formatting and style violations | Code quality — Low | Multiple lines | The original code contained formatting and style issues reported by the static analysis tools. | Corrected formatting and verified the code with Pylint and Flake8. |

## After-Fix Verification

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified; 0 low, 0 medium, and 0 high severity issues.
- **Flake8:** No output, indicating no reported style violations.
  
These results show that the updated file passes the checks performed by the three tools. They do not guarantee that the program is completely free of all bugs or security vulnerabilities.