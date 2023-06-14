import itertools as it
import random

import pytest

import pylib.longevity_ordering_alternating as loa

@pytest.mark.parametrize("num_indices", [2**x for x in range(64)])
@pytest.mark.parametrize("polarity", [True, False])
def test_inverse_get_longevity_mapped_position_of_index(num_indices, polarity):
    random.seed(num_indices)

    for index in it.chain(
        range(min(3000, num_indices)),
        (random.randrange(num_indices) for __ in range(3000)),
    ):

        mapped_position = (
            loa.get_longevity_mapped_position_of_index(
                index,
                num_indices,
                polarity,
            )
        )
        assert (
            loa.get_longevity_index_of_mapped_position(
                mapped_position,
                num_indices,
                polarity,
            )
            == index
        )
