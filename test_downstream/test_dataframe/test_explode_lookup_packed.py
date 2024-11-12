import polars as pl

import downstream
from downstream.dataframe import explode_lookup_packed


def test_explode_lookup_packed_empty():

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
    res = explode_lookup_packed(df, value_type="uint8")

    for col in "data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert res.is_empty()


def test_explode_lookup_packed_bit():

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": ["aa11ccdd", "221188dd"],
            "dstream_storage_bitoffset": [0, 0],
            "dstream_storage_bitwidth": [16, 16],
            "dstream_T_bitoffset": [16, 16],
            "dstream_T_bitwidth": [16, 16],
            "dstream_S": [16, 16],
        },
    )
    res = explode_lookup_packed(df, value_type="uint8")

    for col in "data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()


def test_explode_lookup_packed_byte():

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": ["aa11ccdd", "221188dd"],
            "dstream_storage_bitoffset": [0, 0],
            "dstream_storage_bitwidth": [16, 16],
            "dstream_T_bitoffset": [16, 16],
            "dstream_T_bitwidth": [16, 16],
            "dstream_S": [2, 2],
        },
    )
    res = explode_lookup_packed(df, value_type="uint8")

    for col in "data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()


def test_explode_lookup_packed_64():

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": ["aa11ccdd", "221188dd"],
            "dstream_storage_bitoffset": [16, 16],
            "dstream_storage_bitwidth": [128, 128],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [16, 16],
            "dstream_S": [2, 2],
        },
    )
    res = explode_lookup_packed(df, value_type="uint64")

    for col in "data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()
