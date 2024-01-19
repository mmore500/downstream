from pylib import bit_floor


def test_bit_floor():
    assert bit_floor(0b00000000) == 0b00000000
    assert bit_floor(0b00000001) == 0b00000001
    assert bit_floor(0b00000010) == 0b00000010
    assert bit_floor(0b00000011) == 0b00000010
    assert bit_floor(0b00000100) == 0b00000100
    assert bit_floor(0b00000101) == 0b00000100
    assert bit_floor(0b00000110) == 0b00000100
    assert bit_floor(0b00000111) == 0b00000100
    assert bit_floor(0b00001000) == 0b00001000
    assert bit_floor(0b00001001) == 0b00001000
