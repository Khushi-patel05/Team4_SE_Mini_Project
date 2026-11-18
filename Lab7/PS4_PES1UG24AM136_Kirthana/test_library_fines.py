from hypothesis import given, strategies as st

from library_fines import parse_member_id, total_fine, shelf_code


# Fuzz tests: arbitrary strings (and None) must never crash the functions.
ANY_INPUT = st.one_of(st.text(), st.none())


@given(ANY_INPUT)
def test_parse_member_id_no_crash(value):
    result = parse_member_id(value)
    assert isinstance(result, tuple)
    assert len(result) == 2


@given(ANY_INPUT)
def test_total_fine_no_crash(value):
    result = total_fine(value)
    assert isinstance(result, int)
    assert result >= 0


@given(ANY_INPUT)
def test_shelf_code_no_crash(value):
    result = shelf_code(value)
    assert isinstance(result, str)
    assert result == result.upper()


# Property tests: valid inputs must preserve the expected behaviour.
@given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll')), min_size=1),
       st.integers(min_value=0, max_value=10**9))
def test_parse_member_id_valid_values(member_type, number):
    result = parse_member_id(f"{member_type}-{number}")
    assert result == (member_type.upper(), number)


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=0, max_size=30))
def test_total_fine_matches_rule(days_list):
    csv_value = ','.join(str(day) for day in days_list)
    expected = sum((day - 14) * 2 for day in days_list if day > 14)
    assert total_fine(csv_value) == expected


@given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll')), min_size=1),
       st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll')), min_size=1),
       st.lists(st.text(min_size=1), min_size=0, max_size=5))
def test_shelf_code_uses_first_two_initials(first, second, remaining_words):
    title = ' '.join([first, second] + remaining_words)
    assert shelf_code(title) == (first[0] + second[0]).upper()
