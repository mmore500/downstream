import itertools as it
import random

import pytest

import pylib


@pytest.mark.parametrize("num_indices", [2**x for x in range(64)])
def test_inverse_get_longevity_mapped_position_of_index(num_indices):
    random.seed(num_indices)

    for index in it.chain(
        range(min(3000, num_indices)),
        (random.randrange(num_indices) for __ in range(3000)),
    ):

        mapped_position = (
            pylib.longevity_ordering.get_longevity_mapped_position_of_index(
                index,
                num_indices,
            )
        )
        assert (
            pylib.longevity_ordering.get_longevity_index_of_mapped_position(
                mapped_position,
                num_indices,
            )
            == index
        )
