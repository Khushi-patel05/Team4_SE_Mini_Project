# Lab 7 – Fuzzing for Input Validation Bugs

**Student Name:** Porla Neha  
**SRN:** PES1UG25AM808  
**Lab:** 7  
**Topic:** Fuzzing for Input Validation Bugs

## 1. About the Lab

This lab focuses on identifying and fixing input validation bugs using fuzz testing. The Python program contains three functions:

- `mask_imei()` – Masks an IMEI number while keeping the last four characters visible.
- `parse_parts_order()` – Parses spare parts and their quantities.
- `parse_model()` – Separates the phone brand and model.

## 2. Tools and Technologies Used

- Python
- pytest
- Hypothesis
- Visual Studio Code
- Git and GitHub

## 3. Bugs Identified

The original program had the following issues:

1. `mask_imei()` crashed when it received `None`.
2. `parse_parts_order()` crashed when a quantity contained invalid text instead of a number.
3. `parse_model()` crashed when it received `None`.

## 4. Fixes Implemented

The following improvements were made:

- Added safe string conversion to handle unexpected input types.
- Added validation for empty and invalid parts-order entries.
- Used exception handling for invalid quantity conversion.
- Added safe handling of empty phone model input.
- Ensured that unexpected inputs do not cause the functions to crash.

## 5. Testing

Hypothesis was used to generate different input values, including:

- Random strings
- Empty strings
- Special characters
- `None` values

Three automated tests were implemented to check that each function handles unexpected inputs without crashing.

**Testing command:**

```bash
python -m pytest test_phone_repair_quote_parser.py -v
```

All three tests passed after the fixes were implemented.

## 6. Screenshots

The `screenshots` folder contains the following evidence:

| Screenshot | Description |
|---|---|
| SS1_original_buggy_output.png | Original buggy program output |
| SS2_hypothesis_failures.png | Hypothesis tests failing on the original code |
| SS3_fixed_program_output.png | Fixed program output |
| SS4_all_tests_passing.png | All tests passing after fixes |

## 7. Reflection

This lab helped us understand how fuzz testing identifies unexpected input-related failures. We learned how Hypothesis generates test inputs automatically and how defensive programming techniques, such as input validation and exception handling, improve program reliability.

## 8. Conclusion

The three functions were tested and improved to handle unexpected inputs safely. Hypothesis testing confirmed that the corrected functions do not crash for the generated test inputs. This lab demonstrated the importance of automated testing and robust input validation in software development.
