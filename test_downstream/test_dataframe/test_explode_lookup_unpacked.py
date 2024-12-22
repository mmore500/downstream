import polars as pl
import pytest

import downstream
from downstream.dataframe import unpack_data_packed
from downstream.dataframe._explode_lookup_unpacked import (
    explode_lookup_unpacked,
)


def test_explode_lookup_unpacked_empty():

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
            "downstream_validate_exploded": "pl.col('dstream_T') + 1 != 0",
        },
    )
    df = unpack_data_packed(df)
    res = explode_lookup_unpacked(df, value_type="uint8")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert res.is_empty()


def test_explode_lookup_unpacked_bit():

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
            "downstream_validate_exploded": ["pl.col('dstream_T') != 0"] * 2,
        },
    )
    df = unpack_data_packed(df)
    res = explode_lookup_unpacked(df, value_type="uint8")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()


def test_explode_lookup_unpacked_byte():

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
            "downstream_validate_exploded": ["pl.col('dstream_T') != 0"] * 2,
        },
    )
    df = unpack_data_packed(df)
    res = explode_lookup_unpacked(df, value_type="uint8")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()


def test_explode_lookup_unpacked_64():

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": [
                "aa11ccddaa11ccddaa11ccddaa11ccddaa11ccddaa11ccddaa11ccddaa11ccdd",
                "221188dd221188dd221188dd221188dd221188dd221188dd221188dd221188dd",
            ],
            "dstream_storage_bitoffset": [16, 16],
            "dstream_storage_bitwidth": [128, 128],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [16, 16],
            "dstream_S": [2, 2],
            "downstream_validate_exploded": ["pl.col('dstream_T') != 0"] * 2,
            "downstream_exclude_exploded": [False, False],
        },
    )
    df = unpack_data_packed(df)
    res = explode_lookup_unpacked(df, value_type="uint64")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()


def test_explode_lookup_unpacked_invalid():

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": [
                "aa11ccddaa11ccddaa11ccddaa11ccddaa11ccddaa11ccddaa11ccddaa11ccdd",
                "221188dd221188dd221188dd221188dd221188dd221188dd221188dd221188dd",
            ],
            "dstream_storage_bitoffset": [16, 16],
            "dstream_storage_bitwidth": [128, 128],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [16, 16],
            "dstream_S": [2, 2],
            "downstream_validate_exploded": [
                "pl.col('dstream_Tbar') == 0",
                "pl.col('dstream_Tbar') != 0",
            ],
        },
    )
    df = unpack_data_packed(df)
    with pytest.raises(ValueError):
        explode_lookup_unpacked(df, value_type="uint64")
