import numpy as np

from downstream._auxlib._ctz import ctz


def test_ctz():
    # fmt: off
    assert [*map(ctz, range(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]


def test_ctz_numpy():
    np.testing.assert_array_equal(
        ctz(np.arange(1, 17)),
        np.array([0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4]),
    )
