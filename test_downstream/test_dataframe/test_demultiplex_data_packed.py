import os
import subprocess

import polars as pl
from polars import testing as pl_testing
import pytest

import downstream
from downstream.dataframe import (
    demultiplex_data_packed,
    explode_lookup_packed,
    unpack_data_packed,
)


def _make_df(data_hex: list, multiplex: int = 1) -> pl.DataFrame:
    """Packed data with `multiplex` 16-bit buffers, then a shared 16-bit T."""
    n = len(data_hex)
    return pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"] * n,
            "downstream_version": [downstream.__version__] * n,
            "data_hex": data_hex,
            "dstream_storage_bitoffset": [0] * n,
            "dstream_storage_bitwidth": [16] * n,
            "dstream_T_bitoffset": [16 * multiplex] * n,
            "dstream_T_bitwidth": [16] * n,
            "dstream_S": [16] * n,
        },
    )


def test_demultiplex_data_packed_default():
    df = _make_df(["aa11ccdd"])
    pl_testing.assert_frame_equal(demultiplex_data_packed(df), df)
    pl_testing.assert_frame_equal(demultiplex_data_packed(df, multiplex=0), df)


def test_demultiplex_data_packed_one():
    df = _make_df(["aa11ccdd", "221188dd"])
    res = demultiplex_data_packed(df, multiplex=1)

    assert res["dstream_multiplex_idx"].to_list() == [0, 0]
    assert res["dstream_multiplex_idx"].dtype == pl.UInt32
    pl_testing.assert_frame_equal(res.drop("dstream_multiplex_idx"), df)


def test_demultiplex_data_packed_split():
    df = _make_df(["aa11ccdd22110001", "0123456789ab0002"], multiplex=3)
    res = demultiplex_data_packed(df, multiplex=3)

    # one row per buffer, in input row order and then buffer order
    assert res["dstream_multiplex_idx"].to_list() == [0, 1, 2, 0, 1, 2]
    # each buffer's storage offset points to its own buffer
    assert res["dstream_storage_bitoffset"].to_list() == [0, 16, 32] * 2
    # other columns, including data and shared T, are forwarded
    assert (
        res["data_hex"].to_list()
        == [df["data_hex"][0]] * 3 + [df["data_hex"][1]] * 3
    )
    assert res["dstream_T_bitoffset"].to_list() == [48] * 6
    assert res.columns == [*df.columns, "dstream_multiplex_idx"]


def test_demultiplex_data_packed_negative():
    df = _make_df(["aa11ccdd"])
    with pytest.raises(ValueError):
        demultiplex_data_packed(df, multiplex=-1)


def test_unpack_data_packed_multiplex():
    multiplexed = _make_df(["aa11ccdd0088"], multiplex=2)
    separate = _make_df(["aa110088", "ccdd0088"])

    res = unpack_data_packed(multiplexed, multiplex=2)
    expected = unpack_data_packed(separate)

    assert res["dstream_multiplex_idx"].to_list() == [0, 1]
    assert res["dstream_T"].to_list() == [0x88, 0x88]  # shared T
    pl_testing.assert_frame_equal(
        res.drop("dstream_multiplex_idx", "dstream_data_id"),
        expected.drop("dstream_data_id"),
    )


def test_unpack_data_packed_multiplex_default():
    df = _make_df(["aa11ccdd", "221188dd"])
    res = unpack_data_packed(df)
    assert "dstream_multiplex_idx" not in res.columns


def test_explode_lookup_packed_multiplex():
    multiplexed = _make_df(["aa11ccdd0088"], multiplex=2)
    separate = _make_df(["aa110088", "ccdd0088"])

    res = explode_lookup_packed(multiplexed, multiplex=2, value_type="uint8")
    expected = explode_lookup_packed(separate, value_type="uint8")

    # each data item keeps the position of its buffer
    assert sorted(res["dstream_multiplex_idx"].unique().to_list()) == [0, 1]
    pl_testing.assert_frame_equal(
        res.drop("dstream_multiplex_idx", "dstream_data_id"),
        expected.drop("dstream_data_id"),
        check_row_order=False,
    )


def test_explode_lookup_packed_multiplex_default():
    df = _make_df(["aa11ccdd", "221188dd"])
    res = explode_lookup_packed(df, value_type="uint8")
    assert "dstream_multiplex_idx" not in res.columns


@pytest.mark.parametrize(
    "module",
    [
        "downstream.dataframe.unpack_data_packed",
        "downstream.dataframe.explode_lookup_packed_uint",
    ],
)
def test_multiplex_cli(module: str, tmp_path):
    input_file = os.path.join(tmp_path, "multiplexed.pqt")
    output_file = os.path.join(tmp_path, "output.pqt")
    _make_df(["aa11ccdd0088"], multiplex=2).write_parquet(input_file)

    subprocess.run(
        ["python3", "-m", module, output_file, "--multiplex", "2"],
        check=True,
        input=input_file.encode(),
    )
    res = pl.read_parquet(output_file)
    assert set(res["dstream_multiplex_idx"].to_list()) == {0, 1}
