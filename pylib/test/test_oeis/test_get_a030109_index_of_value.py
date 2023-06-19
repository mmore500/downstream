import pylib


def test_get_a030109_index_of_value():

    for n in range(2000):
        assert (
            pylib.oeis.get_a030109_index_of_value(
                pylib.oeis.get_a030109_value_at_index(n),
                (n + 1).bit_length(),
            )
            == n
        )
