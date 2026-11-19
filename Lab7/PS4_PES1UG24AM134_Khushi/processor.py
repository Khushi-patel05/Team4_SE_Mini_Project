
def parse_storage_quota(quota_str):
    """
    Parses storage quota strings into Gigabytes (GB).

    Supported formats: 500MB, 20GB, 2TB.
    Returns the formatted quota string.
    Raises ValueError for invalid inputs.
    """

    if not isinstance(quota_str, str):
        raise ValueError("Quota must be a string.")

    cleaned = quota_str.strip().upper()

    if len(cleaned) <= 2:
        raise ValueError("Invalid quota format.")

    val_str = cleaned[:-2]
    unit = cleaned[-2:]

    try:
        value = int(val_str)
    except ValueError:
        raise ValueError("Quota must contain a valid integer.")

    if value < 0:
        raise ValueError("Quota cannot be negative.")

    multipliers = {
        "MB": 0.001,
        "GB": 1.0,
        "TB": 1000.0
    }

    if unit not in multipliers:
        raise ValueError("Unsupported storage unit.")

    gb_total = value * multipliers[unit]

    return f"Quota: {gb_total:.2f} GB"


def compute_compression_ratio(size_metric_str):
    """
    Computes compression ratio:
    raw_bytes / compressed_bytes.

    Expected format: raw_bytes:compressed_bytes.
    Returns the ratio rounded to 2 decimal places.
    """

    if not isinstance(size_metric_str, str):
        raise ValueError("Size metric must be a string.")

    parts = size_metric_str.strip().split(":")

    if len(parts) != 2:
        raise ValueError("Invalid size metric format.")

    try:
        raw_bytes = float(parts[0].strip())
        comp_bytes = float(parts[1].strip())
    except ValueError:
        raise ValueError("Size values must be numeric.")

    if not (float("-inf") < raw_bytes < float("inf")):
        raise ValueError("Raw bytes must be finite.")

    if not (float("-inf") < comp_bytes < float("inf")):
        raise ValueError("Compressed bytes must be finite.")

    if raw_bytes < 0 or comp_bytes < 0:
        raise ValueError("Byte values cannot be negative.")

    if comp_bytes == 0:
        raise ValueError("Compressed bytes cannot be zero.")

    ratio = raw_bytes / comp_bytes

    return round(ratio, 2)


def lookup_bandwidth_tier_rate(tier_descriptor):
    """
    Looks up the egress rate per GB using the first
    three letters of the storage tier.

    Supported tiers: HOT, COLD, ARCHIVE.
    """

    if not isinstance(tier_descriptor, str):
        raise ValueError("Tier descriptor must be a string.")

    cleaned = tier_descriptor.strip().upper()

    if len(cleaned) < 3:
        raise ValueError("Tier descriptor is too short.")

    prefix = cleaned[:3]

    tier_rates = {
        "HOT": 0.08,
        "COL": 0.05,
        "ARC": 0.02
    }

    if prefix not in tier_rates:
        raise ValueError("Unknown storage tier.")

    return tier_rates[prefix]


def main():
    print("==== Running parse_storage_quota ====")
    q_input = input("Enter quota (e.g. 500MB, 10GB, 2TB): ")
    print(parse_storage_quota(q_input))

    print("\n==== Running compute_compression_ratio ====")
    c_input = input("Enter raw:compressed bytes (e.g. 1024:256): ")
    print("Compression Ratio:", compute_compression_ratio(c_input))

    print("\n==== Running lookup_bandwidth_tier_rate ====")
    t_input = input("Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): ")
    print("Rate per GB: $", lookup_bandwidth_tier_rate(t_input))


if __name__ == "__main__":
    main()
