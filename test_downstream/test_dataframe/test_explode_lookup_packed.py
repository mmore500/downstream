import typing

import numpy as np
import polars as pl
from polars import testing as pl_testing
import pytest

import downstream
from downstream import dstream, dsurf
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
            "downstream_validate_exploded": [],
            "downstream_validate_unpacked": [],
        },
    )
    res = explode_lookup_packed(df, value_type="uint8")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert res.is_empty()


@pytest.mark.parametrize("dstream_T_dilation", [None, 1, 2, 3, 4, 8])
def test_explode_lookup_packed_bit(dstream_T_dilation: typing.Optional[int]):

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
            "downstream_validate_unpacked": ["pl.col('dstream_T') != 0"] * 2,
        },
    )
    if dstream_T_dilation is not None:
        df = df.with_columns(dstream_T_dilation=pl.lit(dstream_T_dilation))

    res = explode_lookup_packed(df, value_type="uint8")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()

    dstream_T_raws = res.select("dstream_T_raw").to_series().to_list()
    assert dstream_T_raws[0:16] == [0xCCDD] * 16
    assert dstream_T_raws[16:32] == [0x88DD] * 16

    dstream_Ts = res.select("dstream_T").to_series().to_list()
    assert dstream_Ts[0:16] == [0xCCDD // (dstream_T_dilation or 1)] * 16
    assert dstream_Ts[16:32] == [0x88DD // (dstream_T_dilation or 1)] * 16

    res = res.lazy().collect()
    assert (res["dstream_T"] >= res["dstream_Tbar"]).all()
    assert (res["dstream_T_raw"] >= res["dstream_Tbar"]).all()


@pytest.mark.parametrize("dstream_T_dilation", [None, 1, 2, 3, 4, 8])
def test_explode_lookup_packed_byte(dstream_T_dilation: typing.Optional[int]):

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
            "downstream_validate_unpacked": ["pl.col('dstream_T') != 0"] * 2,
        },
    )
    if dstream_T_dilation is not None:
        df = df.with_columns(dstream_T_dilation=pl.lit(dstream_T_dilation))

    res = explode_lookup_packed(df, value_type="uint8")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()

    dstream_T_raws = res.select("dstream_T_raw").to_series().to_list()
    assert dstream_T_raws[0:2] == [0xCCDD] * 2
    assert dstream_T_raws[2:4] == [0x88DD] * 2

    dstream_Ts = res.select("dstream_T").to_series().to_list()
    assert dstream_Ts[0:2] == [0xCCDD // (dstream_T_dilation or 1)] * 2
    assert dstream_Ts[2:4] == [0x88DD // (dstream_T_dilation or 1)] * 2

    res = res.lazy().collect()
    assert (res["dstream_T"] >= res["dstream_Tbar"]).all()
    assert (res["dstream_T_raw"] >= res["dstream_Tbar"]).all()


@pytest.mark.parametrize("dstream_T_dilation", [None, 1, 2, 3, 4, 8])
def test_explode_lookup_packed_64(dstream_T_dilation: typing.Optional[int]):

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
            "downstream_validate_unpacked": ["pl.col('dstream_T') != 0"] * 2,
        },
    )
    if dstream_T_dilation is not None:
        df = df.with_columns(dstream_T_dilation=pl.lit(dstream_T_dilation))

    res = explode_lookup_packed(df, value_type="uint64")

    for col in "dstream_data_id", "dstream_T", "dstream_Tbar", "dstream_value":
        assert col in res.columns

    assert len(res) == df["dstream_S"].sum()

    dstream_T_raws = res.select("dstream_T_raw").to_series().to_list()
    assert dstream_T_raws[0:2] == [0xAA11] * 2
    assert dstream_T_raws[2:4] == [0x2211] * 2

    dstream_Ts = res.select("dstream_T").to_series().to_list()
    assert dstream_Ts[0:2] == [0xAA11 // (dstream_T_dilation or 1)] * 2
    assert dstream_Ts[2:4] == [0x2211 // (dstream_T_dilation or 1)] * 2

    res = res.lazy().collect()
    assert (res["dstream_T"] >= res["dstream_Tbar"]).all()
    assert (res["dstream_T_raw"] >= res["dstream_Tbar"]).all()


def test_explode_lookup_packed_pup():

    surface1 = dsurf.Surface(dstream.steady_algo, 8)
    for i in range(8):
        surface1.ingest_one(i)

    buffer1 = "".join(map("{:02x}".format, surface1))
    data1 = "{:02x}".format(surface1.T) + buffer1

    surface2 = dsurf.Surface(dstream.steady_algo, 8)
    for i in range(11):
        surface2.ingest_one(i)

    buffer2 = "".join(map("{:02x}".format, surface2))
    data2 = "{:02x}".format(surface2.T) + buffer2

    df = pl.DataFrame(
        {
            "awoo": ["bar", "baz"],
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": [data1, data2],
            "dstream_storage_bitoffset": [8, 8],
            "dstream_storage_bitwidth": [64, 64],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [8, 8],
            "dstream_S": [8, 8],
            "downstream_exclude_exploded": [None, False],
            "downstream_exclude_unpacked": [None, False],
        },
    )
    res = explode_lookup_packed(df, calc_Tbar_argv=True, value_type="uint64")

    expected = pl.DataFrame(
        {
            "dstream_data_id": [0] * 8 + [1] * 8,
            "dstream_T": [surface1.T] * 8 + [surface2.T] * 8,
            "dstream_T_dilation": [1] * 16,
            "dstream_T_raw": [surface1.T] * 8 + [surface2.T] * 8,
            "dstream_Tbar": [*surface1.lookup(), *surface2.lookup()],
            "dstream_Tbar_argv": [
                *np.argsort(np.fromiter(surface1.lookup(), dtype=int)),
                *np.argsort(np.fromiter(surface2.lookup(), dtype=int)),
            ],
            "dstream_value": [*surface1, *surface2],
            "dstream_value_bitwidth": [8] * 16,
        }
    )

    pl_testing.assert_frame_equal(
        res, expected, check_column_order=False, check_dtypes=False
    )


def test_explode_lookup_packed_pup_exclude():

    surface1 = dsurf.Surface(dstream.steady_algo, 8)
    for i in range(8):
        surface1.ingest_one(i)

    buffer1 = "".join(map("{:02x}".format, surface1))
    data1 = "{:02x}".format(surface1.T) + buffer1

    surface2 = dsurf.Surface(dstream.steady_algo, 8)
    for i in range(11):
        surface2.ingest_one(i)

    buffer2 = "".join(map("{:02x}".format, surface2))
    data2 = "{:02x}".format(surface2.T) + buffer2

    df = pl.DataFrame(
        {
            "awoo": ["bar", "baz"],
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": [data1, data2],
            "dstream_storage_bitoffset": [8, 8],
            "dstream_storage_bitwidth": [64, 64],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [8, 8],
            "dstream_S": [8, 8],
            "downstream_exclude_exploded": [True, False],
        },
    )
    res = explode_lookup_packed(df, calc_Tbar_argv=True, value_type="uint64")

    expected = pl.DataFrame(
        {
            "dstream_data_id": [1] * 8,
            "dstream_T": [surface2.T] * 8,
            "dstream_T_dilation": [1] * 8,
            "dstream_T_raw": [surface2.T] * 8,
            "dstream_Tbar": [*surface2.lookup()],
            "dstream_Tbar_argv": np.argsort(
                np.fromiter(surface2.lookup(), dtype=int),
            ),
            "dstream_value": [*surface2],
            "dstream_value_bitwidth": [8] * 8,
        }
    )

    pl_testing.assert_frame_equal(
        res, expected, check_column_order=False, check_dtypes=False
    )
