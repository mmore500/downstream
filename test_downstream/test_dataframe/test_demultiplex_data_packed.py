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


def _make_df(data_hex: list, storage_multiplex: int = 1) -> pl.DataFrame:
    """Packed data with `storage_multiplex` 16-bit buffers, then shared T."""
    n = len(data_hex)
    return pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"] * n,
            "downstream_version": [downstream.__version__] * n,
            "data_hex": data_hex,
            "dstream_storage_bitoffset": [0] * n,
            "dstream_storage_bitwidth": [16] * n,
            "dstream_T_bitoffset": [16 * storage_multiplex] * n,
            "dstream_T_bitwidth": [16] * n,
            "dstream_S": [16] * n,
        },
    )


def _with_multiplex(df: pl.DataFrame, values: list) -> pl.DataFrame:
    return df.with_columns(
        dstream_storage_multiplex=pl.Series(values, dtype=pl.UInt32),
    )


def test_demultiplex_data_packed_absent():
    df = _make_df(["aa11ccdd"])
    pl_testing.assert_frame_equal(demultiplex_data_packed(df), df)


@pytest.mark.parametrize("value", [0, 1])
def test_demultiplex_data_packed_unmultiplexed(value: int):
    df = _with_multiplex(_make_df(["aa11ccdd", "221188dd"]), [value] * 2)
    res = demultiplex_data_packed(df)

    assert res["dstream_storage_multiplex_id"].to_list() == [0, 0]
    assert res["dstream_storage_multiplex_id"].dtype == pl.UInt32
    pl_testing.assert_frame_equal(res.drop("dstream_storage_multiplex_id"), df)


def test_demultiplex_data_packed_split():
    df = _with_multiplex(
        _make_df(["aa11ccdd22110001", "0123456789ab0002"], 3), [3, 3]
    )
    res = demultiplex_data_packed(df)

    # one row per buffer, in input row order and then buffer order
    assert res["dstream_storage_multiplex_id"].to_list() == [0, 1, 2] * 2
    # each buffer's storage offset points to its own buffer
    assert res["dstream_storage_bitoffset"].to_list() == [0, 16, 32] * 2
    # other columns, including data and shared T, are forwarded
    assert (
        res["data_hex"].to_list()
        == [df["data_hex"][0]] * 3 + [df["data_hex"][1]] * 3
    )
    assert res["dstream_T_bitoffset"].to_list() == [48] * 6
    assert res.columns == [*df.columns, "dstream_storage_multiplex_id"]


def test_demultiplex_data_packed_mixed():
    df = _with_multiplex(_make_df(["aa11ccdd0088", "aa110088"]), [2, 0])
    res = demultiplex_data_packed(df)
    assert res["dstream_storage_multiplex_id"].to_list() == [0, 1, 0]
    assert res["dstream_storage_bitoffset"].to_list() == [0, 16, 0]


def test_demultiplex_data_packed_out_of_bounds():
    df = _make_df(["aa11ccdd"], 2)  # room for 2 buffers, not 3
    demultiplex_data_packed(_with_multiplex(df, [2]))
    with pytest.raises(ValueError):
        demultiplex_data_packed(_with_multiplex(df, [3]))


def test_unpack_data_packed_multiplex():
    multiplexed = _with_multiplex(_make_df(["aa11ccdd0088"], 2), [2])
    separate = _make_df(["aa110088", "ccdd0088"])

    res = unpack_data_packed(multiplexed)
    expected = unpack_data_packed(separate)

    assert res["dstream_storage_multiplex_id"].to_list() == [0, 1]
    assert res["dstream_T"].to_list() == [0x88, 0x88]  # shared T
    pl_testing.assert_frame_equal(
        res.drop(
            "dstream_storage_multiplex",
            "dstream_storage_multiplex_id",
            "dstream_data_id",
            strict=False,
        ),
        expected.drop("dstream_data_id"),
    )


def test_unpack_data_packed_multiplex_absent():
    res = unpack_data_packed(_make_df(["aa11ccdd", "221188dd"]))
    assert "dstream_storage_multiplex_id" not in res.columns


def test_explode_lookup_packed_multiplex():
    multiplexed = _with_multiplex(_make_df(["aa11ccdd0088"], 2), [2])
    separate = _make_df(["aa110088", "ccdd0088"])

    res = explode_lookup_packed(multiplexed, value_type="uint8")
    expected = explode_lookup_packed(separate, value_type="uint8")

    # each data item keeps the position of its buffer
    assert sorted(res["dstream_storage_multiplex_id"].unique()) == [0, 1]
    pl_testing.assert_frame_equal(
        res.drop("dstream_storage_multiplex_id", "dstream_data_id"),
        expected.drop("dstream_data_id"),
        check_row_order=False,
    )


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
    _with_multiplex(_make_df(["aa11ccdd0088"], 2), [2]).write_parquet(
        input_file
    )

    subprocess.run(
        ["python3", "-m", module, output_file],
        check=True,
        input=input_file.encode(),
    )
    res = pl.read_parquet(output_file)
    assert set(res["dstream_storage_multiplex_id"].to_list()) == {0, 1}
