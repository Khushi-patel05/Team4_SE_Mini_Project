def parse_member_id(member_id):
    """Parse an ID such as STU-1023; return (None, None) if invalid."""
    if not isinstance(member_id, str):
        return None, None

    parts = member_id.strip().split('-')
    if len(parts) != 2:
        return None, None

    member_type, number = (part.strip() for part in parts)
    if not member_type or not number:
        return None, None

    try:
        member_number = int(number)
    except ValueError:
        return None, None

    return member_type.upper(), member_number


def total_fine(days_csv):
    """Calculate fines for valid non-negative day counts in a CSV string.

    Each book incurs 2 units per day beyond 14 days. Invalid entries are
    ignored so malformed user input cannot crash the calculation.
    """
    if not isinstance(days_csv, str) or not days_csv.strip():
        return 0

    fine = 0
    for item in days_csv.split(','):
        try:
            days = int(item.strip())
        except (TypeError, ValueError):
            continue
        if days > 14:
            fine += (days - 14) * 2
    return fine


def shelf_code(title):
    """Return the uppercase initials of the first two title words."""
    if not isinstance(title, str):
        return ""

    words = title.split()
    if len(words) < 2:
        return ""

    return (words[0][0] + words[1][0]).upper()


def main():
    print("==== Running parse_member_id ====")
    user_input = input("Enter a member ID (e.g. STU-1023): ")
    result = parse_member_id(user_input)
    print("Member Type and Number:", result)

    print("\n==== Running total_fine ====")
    user_input = input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    result = total_fine(user_input)
    print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    user_input = input("Enter a book title with at least two words: ")
    result = shelf_code(user_input)
    print("Shelf Code:", result)


if __name__ == "__main__":
    main()
