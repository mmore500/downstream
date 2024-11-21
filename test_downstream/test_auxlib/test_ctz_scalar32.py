import numpy as np

from downstream._auxlib._ctz_scalar32 import ctz_scalar32


def test_ctz_scalar32():
    # fmt: off
    assert [*map(ctz_scalar32, np.arange(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]
