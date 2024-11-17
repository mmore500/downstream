import numpy as np

from downstream._auxlib._ctz_batched import ctz_batched


def test_ctz_batched():
    np.testing.assert_array_equal(
        ctz_batched(np.arange(1, 17)),
        np.array([0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4]),
    )
