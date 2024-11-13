import polars as pl
from polars import testing as pl_testing

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


def test_explode_lookup_packed_pup():

    surface1 = dsurf.Surface(dsurf.Policy(dstream.steady_algo, 8))
    for i in range(8):
        surface1.ingest(i)

    buffer1 = "".join(map("{:02x}".format, surface1))
    data1 = "{:02x}".format(surface1.T) + buffer1

    surface2 = dsurf.Surface(dsurf.Policy(dstream.steady_algo, 8))
    for i in range(11):
        surface2.ingest(i)

    buffer2 = "".join(map("{:02x}".format, surface2))
    data2 = "{:02x}".format(surface2.T) + buffer2

    df = pl.DataFrame(
        {
            "awoo": ["bar", "baz"],
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": [data1, data2],
            "dstream_storage_bitoffset": [8, 8],
            "dstream_storage_bitwidth": [96, 96],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [8, 8],
            "dstream_S": [8, 8],
        },
    )
    res = explode_lookup_packed(df, value_type="uint64")

    expected = pl.DataFrame(
        {
            "awoo": ["bar"] * 8 + ["baz"] * 8,
            "data_id": [0] * 8 + [1] * 8,
            "downstream_version": [downstream.__version__] * 16,
            "dstream_k": [*range(8), *range(8)],
            "dstream_S": [8] * 16,
            "dstream_T": [surface1.T] * 8 + [surface2.T] * 8,
            "dstream_Tbar": [*surface1.lookup(), *surface2.lookup()],
            "dstream_value": [*surface1, *surface2],
            "dstream_value_bitsize": [8] * 16,
        }
    )

    pl_testing.assert_frame_equal(
        res, expected, check_column_order=False, check_dtypes=False
    )