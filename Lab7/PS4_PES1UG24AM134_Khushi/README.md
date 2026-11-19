# Lab 7 – Fuzz Testing

**Student:** Khushi Patel  
**SRN:** PES1UG24AM134  
**Problem:** Cloud Storage Tier

## Objective

Use Hypothesis-based fuzz testing to evaluate the Cloud Storage Tier functions. Test a wide range of valid, invalid, and unexpected inputs to identify potential errors and ensure that the functions behave safely and consistently.

## Files

- `processor.py` – Defensive implementations of the three functions under test.
- `test_processor.py` – Hypothesis fuzz tests and property-based tests.
- `requirements.txt` – Python testing dependencies.
- `Screenshot/` – Screenshots showing successful test execution.

## Functions Covered

1. `parse_storage_quota(quota_str)` – Converts storage quota values from MB, GB, and TB into Gigabytes (GB).
2. `compute_compression_ratio(size_metric_str)` – Calculates the compression ratio using raw bytes divided by compressed bytes in the `raw_bytes:compressed_bytes` format.
3. `lookup_bandwidth_tier_rate(tier_descriptor)` – Retrieves the egress rate per GB for HOT, COLD, and ARCHIVE storage tiers.

## Testing Approach

- Hypothesis-based fuzz testing to generate a wide range of unexpected inputs.
- Tests for valid and invalid storage quota formats.
- Tests for malformed compression metrics and division-by-zero cases.
- Tests for valid and unsupported bandwidth tier descriptors.
- Property-based tests to verify expected function behaviour.
- Exception handling to ensure invalid inputs are handled safely.

## Run Tests (Windows PowerShell / VS Code Terminal)

Run these commands from this directory:

```bash
py -m pip install -r requirements.txt
py -m pytest -v
```

Hypothesis automatically generates multiple test inputs for each fuzz test.

The test suite contains three no-crash fuzz tests and three property-based tests.

