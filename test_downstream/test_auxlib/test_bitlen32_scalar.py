import numpy as np

from downstream._auxlib._bitlen32_scalar import bitlen32_scalar


def test_bitlen32_scalar_zeros():
    arr = np.array([0, 0, 0])
    expected = np.array([0, 0, 0])
    np.testing.assert_array_equal(bitlen32_scalar(arr[0]), expected[0])


def test_bitlen32_scalar_small_positive_integers():
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    expected = np.array([1, 2, 2, 3, 3, 3, 3, 4])
    np.testing.assert_array_equal(bitlen32_scalar(arr[0]), expected[0])
    np.testing.assert_array_equal(bitlen32_scalar(arr[1]), expected[1])
    np.testing.assert_array_equal(bitlen32_scalar(arr[2]), expected[2])
    np.testing.assert_array_equal(bitlen32_scalar(arr[3]), expected[3])
    np.testing.assert_array_equal(bitlen32_scalar(arr[4]), expected[4])
    np.testing.assert_array_equal(bitlen32_scalar(arr[5]), expected[5])
    np.testing.assert_array_equal(bitlen32_scalar(arr[6]), expected[6])

    arr = np.array([1023, 1024, 1025])
    expected = np.array([10, 11, 11])
    np.testing.assert_array_equal(bitlen32_scalar(arr[0]), expected[0])
    np.testing.assert_array_equal(bitlen32_scalar(arr[1]), expected[1])
    np.testing.assert_array_equal(bitlen32_scalar(arr[2]), expected[2])


def test_bitlen32_scalar_large_integers():
    arr = np.array([2**31 - 1, 2**31, 2**32 - 1], dtype=np.uint32)
    expected = np.array([31, 32, 32])
    np.testing.assert_array_equal(bitlen32_scalar(arr[0]), expected[0])
    np.testing.assert_array_equal(bitlen32_scalar(arr[1]), expected[1])
    np.testing.assert_array_equal(bitlen32_scalar(arr[2]), expected[2])

    arr = np.array([2**31 - 1, 2**30, 2**30 - 1], dtype=np.int32)
    expected = np.array([31, 31, 30])
    np.testing.assert_array_equal(bitlen32_scalar(arr[0]), expected[0])
    np.testing.assert_array_equal(bitlen32_scalar(arr[1]), expected[1])
    np.testing.assert_array_equal(bitlen32_scalar(arr[2]), expected[2])

    arr = np.array([2**53 - 1], dtype=np.int64)
    expected = np.array([53])
    np.testing.assert_array_equal(bitlen32_scalar(arr[0]), expected[0])


def test_bitlen32_scalar_mixed():
    arr = np.array([0, 1, 0, 2, 0, 4])
    expected = np.array([0, 1, 0, 2, 0, 3])
    np.testing.assert_array_equal(bitlen32_scalar(arr[0]), expected[0])
    np.testing.assert_array_equal(bitlen32_scalar(arr[1]), expected[1])
    np.testing.assert_array_equal(bitlen32_scalar(arr[2]), expected[2])
    np.testing.assert_array_equal(bitlen32_scalar(arr[3]), expected[3])
    np.testing.assert_array_equal(bitlen32_scalar(arr[4]), expected[4])
    np.testing.assert_array_equal(bitlen32_scalar(arr[5]), expected[5])