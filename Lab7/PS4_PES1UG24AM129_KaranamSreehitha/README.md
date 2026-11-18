# Lab 7 - Hospital Triage Priority
## Fuzz Testing with Hypothesis

### 1. Objective
To perform property-based fuzz testing on the hospital triage priority processor using the Hypothesis testing framework.

The tests target:
- Patient vitals summary parsing
- Patient BMI calculation
- Ward bed allocation

### 2. Tools and Technologies
- Python 3.11.9
- Hypothesis 6.170.15
- Pytest 9.2.0

### 3. Implementation
The starter `processor.py` module was tested using Hypothesis-generated inputs.

The test suite includes:
- Three malformed-input fuzz tests using `st.text()` and `st.none()`.
- Three property-based tests to verify valid inputs.
- Three targeted edge-case tests for missing vitals fields, zero BMI height, and unknown ward codes.

### 4. Testing Results

Latest test execution:

- Total tests: 9
- Passed: 6
- Failed: 3
- Warnings: 1

The three malformed-input fuzz tests exposed crashes in the original processor functions. The six valid-input and targeted edge-case tests passed.

### 5. Bugs Identified

#### Vitals Summary
- Missing comma-separated values can cause `IndexError`.
- Invalid or empty numeric fields can cause `ValueError`.
- `None` input causes `AttributeError`.

#### BMI Calculation
- Missing or invalid weight/height values can cause `ValueError`.
- `None` input causes `AttributeError`.
- Zero height causes `ZeroDivisionError`.

#### Ward Bed Allocation
- Missing or invalid bed numbers can cause `ValueError`.
- `None` input causes `AttributeError`.
- Unknown ward codes cause `KeyError`.

### 6. Conclusion
Hypothesis successfully generated malformed inputs and exposed input-validation weaknesses in all three processor functions.

The valid-input property tests and targeted edge-case tests passed. The results demonstrate how property-based fuzz testing can identify unexpected failures and help improve software robustness.

The original starter implementation was retained to document the defects discovered during testing.