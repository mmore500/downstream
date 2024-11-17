import numpy as np

from downstream._auxlib._modpow2_batched import modpow2_batched


def test_modpow2_batched():
    a = np.array([10, 10, 10, 15, 20, 16, 1, 3, 1023, 0])
    b = np.array([2, 4, 8, 8, 16, 16, 2, 8, 1024, 8])

    expected = np.array([0, 2, 2, 7, 4, 0, 1, 3, 1023, 0])
    np.testing.assert_array_equal(modpow2_batched(a, b), expected)