import os

import pandas as pd

import pylib

# https://oeis.org/A130654/list
data = [
    0,
    0,
    1,
    0,
    1,
    1,
    1,
    0,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    0,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    0,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    1,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    3,
    1,
    2,
    1,
    0,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    1,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    3,
    1,
    2,
    1,
    1,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
]


def test_get_a130654_value_at_index():
    assert [
        *map(pylib.oeis.get_a130654_value_at_index, range(1, len(data) + 1))
    ] == data


def test_get_a130654_value_at_index2():
    # https://oeis.org/A130654/b130654.txt
    file_path = os.path.join(os.path.dirname(__file__), "assets", "b130654.txt")
    df = pd.read_csv(
        file_path, comment="#", sep=" ", header=None, names=["n", "value"]
    )

    assert data == df["value"].to_list()[: len(data)]

    assert [
        *map(
            pylib.oeis.get_a130654_value_at_index,
            range(1, len(df) + 1),
        )
    ] == df["value"].to_list()
