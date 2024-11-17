import numpy as np

from downstream._auxlib._ctz_scalar import ctz_scalar


def test_ctz_scalar():
    # fmt: off
    assert [*map(ctz_scalar, np.arange(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]
