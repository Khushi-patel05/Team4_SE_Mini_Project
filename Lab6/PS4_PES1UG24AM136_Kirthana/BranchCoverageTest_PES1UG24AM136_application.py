import pytest
from library_fines import late_fine, can_borrow, renewal_status


@pytest.mark.parametrize(
    "member,days_kept,damaged,expected",
    [
        ("student", 14, False, 0),       # not overdue
        ("student", 15, False, 2),       # overdue, below cap
        ("faculty", 31, False, 1),       # faculty loan period
        ("guest", 100, False, 200),      # fine capped
        ("student", 14, True, 150),      # damage charge
        ("student", 15, True, 152),      # overdue plus damage
    ],
)
def test_late_fine_valid_paths(member, days_kept, damaged, expected):
    assert late_fine(member, days_kept, damaged) == expected


@pytest.mark.parametrize(
    "member,days_kept,message",
    [
        ("unknown", 10, "unknown member"),
        ("student", -1, "invalid days"),
    ],
)
def test_late_fine_validation_paths(member, days_kept, message):
    with pytest.raises(ValueError, match=message):
        late_fine(member, days_kept, False)


@pytest.mark.parametrize(
    "books_held,pending_fine,member,expected",
    [
        (1, 0, "student", True),       # regular member below limit
        (3, 0, "student", False),      # regular member at limit
        (9, 0, "faculty", True),       # faculty below limit
        (10, 0, "faculty", False),     # faculty at limit
        (0, 101, "student", False),    # fine restriction takes precedence
        (0, 100, "student", True),     # fine exactly at threshold
    ],
)
def test_can_borrow_all_decisions(books_held, pending_fine, member, expected):
    assert can_borrow(books_held, pending_fine, member) is expected


@pytest.mark.parametrize(
    "times_renewed,reserved,days_left,expected",
    [
        (0, True, 5, "denied"),             # reservation takes precedence
        (2, False, 5, "limit reached"),     # renewal count limit
        (1, False, -1, "overdue"),           # negative days remaining
        (1, False, 0, "renewed"),            # zero days is not overdue
        (1, False, 5, "renewed"),            # ordinary renewal
    ],
)
def test_renewal_all_decisions(times_renewed, reserved, days_left, expected):
    assert renewal_status(times_renewed, reserved, days_left) == expected
