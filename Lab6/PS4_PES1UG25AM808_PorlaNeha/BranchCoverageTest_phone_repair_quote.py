import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value


# REPAIR QUOTE TESTS

def test_budget_screen():
    assert repair_quote("screen", "budget", False, False) == 4600


def test_flagship_camera_express():
    assert repair_quote("camera", "flagship", False, True) == 5800


def test_warranty_battery():
    assert repair_quote("battery", "budget", True, False) == 300


def test_warranty_screen():
    assert repair_quote("screen", "budget", True, False) == 4600


def test_charging_port_express():
    assert repair_quote("charging_port", "budget", False, True) == 1600


def test_invalid_part():
    with pytest.raises(ValueError):
        repair_quote("speaker", "budget", False, False)


def test_invalid_brand():
    with pytest.raises(ValueError):
        repair_quote("screen", "premium", False, False)


# REPAIR DAYS TESTS

def test_technician_available():
    assert repair_days("battery", True, 2) == 1


def test_no_technician():
    assert repair_days("battery", True, 0) == 3


def test_screen_out_of_stock():
    assert repair_days("screen", False, 2) == 6


def test_camera_out_of_stock():
    assert repair_days("camera", False, 2) == 6


def test_battery_out_of_stock():
    assert repair_days("battery", False, 2) == 3


def test_no_technician_and_no_stock():
    assert repair_days("battery", False, 0) == 5


# TRADE-IN VALUE TESTS

def test_trade_in_new_phone():
    assert trade_in_value(10000, 6, False) == 6000


def test_trade_in_one_to_two_years():
    assert trade_in_value(10000, 18, False) == 4000


def test_trade_in_two_to_four_years():
    assert trade_in_value(10000, 36, False) == 2000


def test_trade_in_cracked_screen():
    assert trade_in_value(10000, 6, True) == 3000


def test_trade_in_exactly_12_months():
    assert trade_in_value(10000, 12, False) == 6000


def test_trade_in_exactly_24_months():
    assert trade_in_value(10000, 24, False) == 4000


def test_trade_in_over_48_months():
    assert trade_in_value(10000, 49, False) == 0


def test_invalid_original_price():
    with pytest.raises(ValueError):
        trade_in_value(0, 10, False)


def test_invalid_age():
    with pytest.raises(ValueError):
        trade_in_value(10000, -1, False)