import pytest

import pylib


@pytest.mark.parametrize("input, expected_result", [
    (0, 0),  # 0 is not divisible by 2
    (1, 0),  # 1 is an odd number
    (2, 1),  # 2 / 2 = 1
    (4, 2),  # 4 / 2 / 2 = 1
    (12, 2),  # 12 / 2 / 2 = 3
    (1024, 10),  # 1024 is 2^10
    (1280, 8),  # 1280 / 2^8 = 5
    (15, 0),  # 15 is an odd number
])
def test_remove_factors_of_2(input, expected_result):
    result = pylib.count_factors_of_2(input)
    assert result == expected_result
