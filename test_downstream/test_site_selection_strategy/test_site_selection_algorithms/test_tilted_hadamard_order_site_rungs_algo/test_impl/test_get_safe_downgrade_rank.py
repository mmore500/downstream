import typing

import pytest

from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_safe_downgrade_rank,
)


@pytest.mark.parametrize(
    "test_params, expected_result",
    [
        # Expected to cover the first case described in source code comment
        (
            {
                "cycle_num_ranks": 100,
                "required_cycle_rank_position": 28,
                "required_lag": 100,
                "end_rank": 255,
                "hanoi_offset": 2,
                "cadence_for_asserts": 4,
                "hanoi_value_for_asserts": 1,
            },
            130,
        ),
        # Expected to cover the second case described in source code comment
        (
            {
                "cycle_num_ranks": 100,
                "required_cycle_rank_position": 80,
                "required_lag": 100,
                "end_rank": 255,
                "hanoi_offset": 2,
                "cadence_for_asserts": 4,
                "hanoi_value_for_asserts": 1,
            },
            82,
        ),
    ],
)
def test_get_safe_downgrade_rank_(
    test_params: typing.Dict,
    expected_result: int,
):
    actual_result = get_safe_downgrade_rank(**test_params)
    assert actual_result == expected_result
