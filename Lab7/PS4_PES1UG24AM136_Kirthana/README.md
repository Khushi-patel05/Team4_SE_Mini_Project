# Lab 7 – Fuzz Testing

**Student:** Kirthana S  
**SRN:** PES1UG24AM136  
**Problem:** Library Fines

## Objective
Use Hypothesis-based fuzz testing to check that the Library Fines functions handle a wide range of inputs safely and satisfy their expected properties.

## Files
- `library_fines.py` – defensive implementations of the three functions under test.
- `test_library_fines.py` – Hypothesis fuzz tests and property-based tests.
- `requirements.txt` – Python test dependencies.

## Functions covered
1. `parse_member_id(member_id)` – parses IDs in `TYPE-NUMBER` format; invalid input returns `(None, None)`.
2. `total_fine(days_csv)` – calculates 2 units per day beyond 14 days; malformed entries are ignored.
3. `shelf_code(title)` – returns uppercase initials of the first two words; invalid or short input returns an empty string.

## Run tests (Windows PowerShell / VS Code terminal)
Run these commands from this directory:

```powershell
py -m pip install -r requirements.txt
py -m pytest -v
```

Hypothesis generates multiple test inputs automatically for each fuzz test. The suite includes three no-crash fuzz tests and three property tests.

## Required evidence
After running the tests successfully, capture a screenshot of the terminal showing the `py -m pytest -v` command, all test cases marked `PASSED`, and the final pytest summary. Do not use a typed or recreated test output as evidence; capture the actual terminal run.
