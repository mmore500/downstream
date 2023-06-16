from pylib import longevity_ordering_piecewise_ascending as loapa


def test_get_a030109_index_of_value():

    for n in range(2000):
        assert loapa.get_a030109_index_of_value(
            loapa.get_a030109_value_at_index(n),
            (n + 1).bit_length(),
        ) == n
