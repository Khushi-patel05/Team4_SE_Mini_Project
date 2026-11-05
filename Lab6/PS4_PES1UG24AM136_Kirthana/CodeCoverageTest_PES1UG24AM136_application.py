import pytest
from library_fines import late_fine, can_borrow, renewal_status


def test_student_on_time():
    assert late_fine("student", 10, False) == 0


def test_student_overdue():
    assert late_fine("student", 16, False) == 4


def test_faculty_overdue():
    assert late_fine("faculty", 32, False) == 2


def test_guest_fine_capped():
    assert late_fine("guest", 100, False) == 200


def test_damaged_book_adds_charge():
    assert late_fine("student", 10, True) == 150


def test_unknown_member_rejected():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 20, False)


def test_negative_days_rejected():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_can_borrow_student():
    assert can_borrow(1, 0, "student") is True


def test_cannot_borrow_with_high_fine():
    assert can_borrow(0, 101, "student") is False


def test_faculty_can_borrow():
    assert can_borrow(9, 0, "faculty") is True


def test_renewal_denied_for_reservation():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_overdue():
    assert renewal_status(1, False, -1) == "overdue"


def test_renewal_successful():
    assert renewal_status(1, False, 3) == "renewed"
