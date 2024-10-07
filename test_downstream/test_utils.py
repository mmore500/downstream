from downstream.utils import ctz, bit_floor, modpow2

def test_ctz():
    # fmt: off
    assert [*map(ctz, range(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]


def test_bit_floor():
    # fmt: off
    assert [*map(bit_floor, range(1, 17))] == [
        1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16
    ]

def test_modpow2():
    assert modpow2(10, 2) == 0  # 10 % 2 = 0
    assert modpow2(10, 4) == 2  # 10 % 4 = 2
    assert modpow2(10, 8) == 2  # 10 % 8 = 2
    assert modpow2(15, 8) == 7  # 15 % 8 = 7
    assert modpow2(20, 16) == 4  # 20 % 16 = 4
    assert modpow2(16, 16) == 0  # 16 % 16 = 0
    assert modpow2(1, 2) == 1  # 1 % 2 = 1
    assert modpow2(3, 8) == 3  # 3 % 8 = 3
    assert modpow2(1023, 1024) == 1023  # 1023 % 1024 = 1023
    assert modpow2(0, 8) == 0  # 0 % 8 = 0