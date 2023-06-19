import pylib


def test_round_to_one_sigfig():
    assert pylib.round_to_one_sigfig(1234) == 1000
    assert pylib.round_to_one_sigfig(9876) == 10000
    assert pylib.round_to_one_sigfig(567) == 600
    assert pylib.round_to_one_sigfig(-325) == -300
