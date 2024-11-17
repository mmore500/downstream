import numpy as np

from downstream._auxlib._bit_floor_batched import bit_floor_batched


def test_bit_floor_batched():
    np.testing.assert_array_equal(
        bit_floor_batched(np.arange(1, 17)),
        np.array([1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16]),
    )
