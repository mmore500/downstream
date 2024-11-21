import numpy as np

from downstream._auxlib._ctz_batched32 import ctz_batched32


def test_ctz_batched32():
    np.testing.assert_array_equal(
        ctz_batched32(np.arange(1, 17)),
        np.array([0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4]),
    )
