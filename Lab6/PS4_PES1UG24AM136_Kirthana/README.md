# Lab 6 – Code and Branch Coverage Analysis

**Assigned Repository:** L6_L7_14_library_fines  
**Student:** Kirthana S  
**SRN:** PES1UG24AM136  
**Section:** 5 C

## 1. Objective

To perform code coverage and branch coverage analysis on the Library Fines application using Python Pytest and Coverage.py. The objective is to achieve 100% statement coverage and 100% branch coverage.

## 2. Lab 6 Files

- `library_fines.py` – Original application under test (unchanged).
- `CodeCoverageTest_PES1UG24AM136_application.py` – Code coverage test cases.
- `BranchCoverageTest_PES1UG24AM136_application.py` – Branch coverage test cases.
- `Screenshot/` – Screenshots of test execution and coverage reports.

## 3. Setup

Install the required packages using Windows PowerShell:

```powershell
py -m pip install pytest coverage
```

## 4. Code Coverage Analysis

Execute the following commands:

```powershell
py -m coverage erase
py -m coverage run -m pytest -v CodeCoverageTest_PES1UG24AM136_application.py
py -m coverage report -m
```

**Result:** All 14 code coverage tests passed.

The application achieved 100% statement coverage.

## 5. Branch Coverage Analysis

Execute the following commands:

```powershell
py -m coverage erase
py -m coverage run --branch -m pytest -v BranchCoverageTest_PES1UG24AM136_application.py
py -m coverage report -m
```

**Result:** All 19 branch coverage tests passed.

The application achieved:
- Statement coverage: 100%
- Branch coverage: 100%
- Missing statements: 0
- Partial branches: 0

## 6. HTML Coverage Report

Generate the HTML coverage report using:

```powershell
py -m coverage html
```

Open the report:

```powershell
start htmlcov/index.html
```

The HTML report confirms 100% total coverage for both application files.

## 7. Screenshots

The `Screenshot/` directory contains:

1. `code_coverage` – Code coverage test execution.
2. `branch_coverage` – Branch coverage test execution.
3. `coverage_html` – HTML coverage report showing 100% coverage.

## 8. Conclusion

Successfully completed code and branch coverage analysis of the Library Fines application. All 14 code coverage tests and 19 branch coverage tests passed. The application achieved 100% statement coverage and 100% branch coverage, with no missing statements or partial branches.