import pylib


def test_bit_decode_gray():
    for n in range(2000):
        assert pylib.bit_decode_gray(pylib.bit_encode_gray(n)) == n
        assert pylib.bit_encode_gray(pylib.bit_decode_gray(n)) == n
