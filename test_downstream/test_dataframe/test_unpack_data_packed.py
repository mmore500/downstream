import polars as pl
from polars import testing as pl_testing
import pytest

import downstream
from downstream import dstream, dsurf
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


def test_unpack_data_packed_invalid():

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
            "downstream_validate_unpacked": ["pl.col('dstream_S') == 42", ""],
        },
    )
    with pytest.raises(ValueError):
        unpack_data_packed(df)


def test_unpack_data_packed_single_row():
    df = pl.DataFrame(
        {
            "foo": ["bar"],
            "data_hex": ["0F0E0D0C0B0A09080706050403020100"],
            "dstream_algo": ["dstream.steady_algo"],
            "dstream_storage_bitoffset": [4],
            "dstream_storage_bitwidth": [96],
            "dstream_T_bitoffset": [100],
            "dstream_T_bitwidth": [16],
            "dstream_S": [100],
            "downstream_version": [downstream.__version__],
            "downstream_validate_unpacked": [""],
            "downstream_validate_exploded": ["pl.lit(42)"],
            "downstream_exclude_unpacked": [False],
        }
    )

    result = unpack_data_packed(df)

    expected_df = pl.DataFrame(
        {
            "foo": ["bar"],
            "dstream_data_id": [0],
            "dstream_algo": ["dstream.steady_algo"],
            "dstream_T": [12320],
            "dstream_S": [100],
            "dstream_storage_hex": ["F0E0D0C0B0A0908070605040"],
            "downstream_version": [downstream.__version__],
            "downstream_validate_exploded": ["pl.lit(42)"],
        }
    )

    pl_testing.assert_frame_equal(
        result, expected_df, check_column_order=False, check_dtypes=False
    )


def test_unpack_data_packed_pup():

    surface1 = dsurf.Surface(dstream.steady_algo, 8)
    surface1.ingest_multiple(8, lambda x: x)

    buffer1 = "".join(map("{:02x}".format, surface1))
    data1 = "{:02x}".format(surface1.T) + buffer1

    surface2 = dsurf.Surface(dstream.steady_algo, 8)
    surface2.ingest_multiple(11, lambda x: x)

    buffer2 = "".join(map("{:02x}".format, surface2))
    data2 = "{:02x}".format(surface2.T) + buffer2

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": [data1, data2],
            "dstream_storage_bitoffset": [8, 8],
            "dstream_storage_bitwidth": [64, 64],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [8, 8],
            "dstream_S": [8, 8],
        },
    )
    res = unpack_data_packed(df)

    assert len(res) == 2


def test_unpack_data_packed_pup_validated():

    surface1 = dsurf.Surface(dstream.steady_algo, 8)
    surface1.ingest_multiple(8, lambda x: x)

    buffer1 = "".join(map("{:02x}".format, surface1))
    data1 = "{:02x}".format(surface1.T) + buffer1

    surface2 = dsurf.Surface(dstream.steady_algo, 8)
    surface2.ingest_multiple(11, lambda x: x)

    buffer2 = "".join(map("{:02x}".format, surface2))
    data2 = "{:02x}".format(surface2.T) + buffer2

    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": [data1, data2],
            "dstream_storage_bitoffset": [8, 8],
            "dstream_storage_bitwidth": [16, 16],
            "dstream_T_bitoffset": [0, 0],
            "dstream_T_bitwidth": [8, 8],
            "dstream_S": [8, 8],
            "downstream_validate_unpacked": ["", "pl.col('dstream_T') == 11"],
            "downstream_exclude_unpacked": [False, True],
        },
    )
    res = unpack_data_packed(df)

    assert len(res) == 1


def test_unpack_data_packed_bounds():
    df = pl.DataFrame(
        {
            "foo": ["bar"],
            "data_hex": ["0F0E0D0C0B0A09080706050403020100"],
            "dstream_algo": ["dstream.steady_algo"],
            "dstream_storage_bitoffset": [120],
            "dstream_storage_bitwidth": [96],
            "dstream_T_bitoffset": [100],
            "dstream_T_bitwidth": [16],
            "dstream_S": [100],
            "downstream_version": [downstream.__version__],
            "downstream_validate_unpacked": [""],
            "downstream_validate_exploded": ["pl.lit(42)"],
            "downstream_exclude_unpacked": [False],
        }
    )

    with pytest.raises(ValueError):
        unpack_data_packed(df)
