from downstream._auxlib._is_in_unit_test import is_in_unit_test


def test_is_in_unit_test():
    assert is_in_unit_test() is True
