import polars as pl

import downstream
from downstream.dataframe import unpack_data_packed


def test_unpack_data_empty():

    df = pl.DataFrame(
        {
            "dstream_algo": [],
            "downstream_version": [],
            "data_hex": [],
            "dstream_storage_bitoffset": [],
            "dstream_storage_bitwidth": [],
            "dstream_T_bitoffset": [],
            "dstream_T_bitwidth": [],
            "dstream_S": [],
        },
    )
    res = unpack_data_packed(df)

    for col in "dstream_algo", "dstream_S", "dstream_T", "dstream_storage_hex":
        assert col in res.columns

    assert res.is_empty()


def test_unpack_data_packed():

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": ["aa11ccdd", "221188dd"],
            "dstream_storage_bitoffset": [0, 0],
            "dstream_storage_bitwidth": [16, 16],
            "dstream_T_bitoffset": [16, 16],
            "dstream_T_bitwidth": [4, 4],
            "dstream_S": [16, 16],
        },
    )
    res = unpack_data_packed(df)

    for col in "dstream_algo", "dstream_S", "dstream_T", "dstream_storage_hex":
        assert col in res.columns

    assert len(res) == 2
