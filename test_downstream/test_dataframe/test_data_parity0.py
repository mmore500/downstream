import numpy as np
import polars as pl
import pytest

import downstream
from downstream.dataframe import unpack_data_packed
from downstream.dataframe._unpack_data_packed import (
    _deserialize_h_matrix,
    _hex_to_bits,
)


def _spaced(row_str):
    """Convert '1010' to '1 0 1 0' for H matrix format."""
    return " ".join(row_str)


def _h_matrix(*rows):
    """Build newline-delimited, space-separated H matrix string."""
    return "\n".join(_spaced(r) for r in rows)


def _make_base_df(**extra_cols):
    base = {
        "dstream_algo": ["dstream.steady_algo", "dstream.steady_algo"],
        "downstream_version": [downstream.__version__] * 2,
        "data_hex": ["aa11ccdd", "221188dd"],
        "dstream_storage_bitoffset": [0, 0],
        "dstream_storage_bitwidth": [16, 16],
        "dstream_T_bitoffset": [16, 16],
        "dstream_T_bitwidth": [4, 4],
        "dstream_S": [16, 16],
    }
    base.update(extra_cols)
    return pl.DataFrame(base)


# --- _hex_to_bits tests ---


def test_hex_to_bits_single_hex_char():
    result = _hex_to_bits("f")
    np.testing.assert_array_equal(result, [1, 1, 1, 1])


def test_hex_to_bits_zero():
    result = _hex_to_bits("0")
    np.testing.assert_array_equal(result, [0, 0, 0, 0])


def test_hex_to_bits_two_chars():
    result = _hex_to_bits("0f")
    np.testing.assert_array_equal(
        result, [0, 0, 0, 0, 1, 1, 1, 1],
    )


def test_hex_to_bits_odd_length():
    # odd-length hex: "a" -> 1010
    result = _hex_to_bits("a")
    np.testing.assert_array_equal(result, [1, 0, 1, 0])


def test_hex_to_bits_even_length():
    result = _hex_to_bits("ff")
    np.testing.assert_array_equal(result, [1] * 8)


def test_hex_to_bits_longer():
    result = _hex_to_bits("00ff")
    assert len(result) == 16
    np.testing.assert_array_equal(result[:8], [0] * 8)
    np.testing.assert_array_equal(result[8:], [1] * 8)


# --- _deserialize_h_matrix tests ---


def test_deserialize_h_matrix_single_row():
    h = _deserialize_h_matrix("1 1 1 1")
    np.testing.assert_array_equal(h, [[1, 1, 1, 1]])


def test_deserialize_h_matrix_two_rows():
    h = _deserialize_h_matrix("1 1 1 1\n1 0 1 0")
    np.testing.assert_array_equal(h, [[1, 1, 1, 1], [1, 0, 1, 0]])


def test_deserialize_h_matrix_identity():
    h = _deserialize_h_matrix(
        "1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1",
    )
    np.testing.assert_array_equal(h, np.eye(4, dtype=np.uint8))


def test_deserialize_h_matrix_dtype():
    h = _deserialize_h_matrix("0 1\n1 0")
    assert h.dtype == np.uint8


def test_deserialize_h_matrix_bad_input():
    with pytest.raises(Exception):
        _deserialize_h_matrix("not a matrix")


# --- _apply_data_parity0 integration tests ---


def test_parity_no_rule_column():
    df = _make_base_df()
    res = unpack_data_packed(df)
    assert "downstream_data_parity0_result" not in res.columns
    assert "downstream_data_parity0_rule" not in res.columns


def test_parity_rule_produces_result():
    h_row_32 = _spaced("1" * 32)
    df = _make_base_df(
        downstream_data_parity0_rule=[h_row_32, h_row_32],
    )
    res = unpack_data_packed(df)
    assert "downstream_data_parity0_result" in res.columns
    assert "downstream_data_parity0_rule" not in res.columns
    assert res["downstream_data_parity0_result"].dtype == pl.UInt32


def test_parity_rule_identity_matrix():
    h_rows = []
    for i in range(32):
        row = ["0"] * 32
        row[i] = "1"
        h_rows.append("".join(row))
    h_matrix = _h_matrix(*h_rows)

    df = _make_base_df(
        downstream_data_parity0_rule=[h_matrix, h_matrix],
    )
    res = unpack_data_packed(df)
    results = res["downstream_data_parity0_result"].to_list()
    expected_0 = bin(int("aa11ccdd", 16)).count("1")
    expected_1 = bin(int("221188dd", 16)).count("1")
    assert results[0] == expected_0
    assert results[1] == expected_1


def test_parity_rule_empty_string():
    df = _make_base_df(
        downstream_data_parity0_rule=["", ""],
    )
    res = unpack_data_packed(df)
    assert "downstream_data_parity0_result" in res.columns
    assert res["downstream_data_parity0_result"].to_list() == [0, 0]


def test_parity_rule_mismatched_length_raises():
    df = _make_base_df(
        downstream_data_parity0_rule=["1 0 1", "1 0 1"],
    )
    with pytest.raises(ValueError, match="does not match"):
        unpack_data_packed(df)


def test_parity_rule_all_zeros():
    h_row = _spaced("0" * 32)
    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"],
            "downstream_version": [downstream.__version__],
            "data_hex": ["001100dd"],
            "dstream_storage_bitoffset": [0],
            "dstream_storage_bitwidth": [16],
            "dstream_T_bitoffset": [16],
            "dstream_T_bitwidth": [4],
            "dstream_S": [16],
            "downstream_data_parity0_rule": [h_row],
        }
    )
    res = unpack_data_packed(df)
    assert res["downstream_data_parity0_result"].to_list() == [0]


def test_parity_rule_with_categorical_type():
    h_row_32 = _spaced("1" * 32)
    df = _make_base_df(
        downstream_data_parity0_rule=[h_row_32, h_row_32],
    ).cast({"downstream_data_parity0_rule": pl.Categorical})
    res = unpack_data_packed(df)
    assert "downstream_data_parity0_result" in res.columns


def test_parity_rule_multiple_h_rows():
    h_matrix = _h_matrix("1" * 32, "0" * 32)
    df = _make_base_df(
        downstream_data_parity0_rule=[h_matrix, h_matrix],
    )
    res = unpack_data_packed(df)
    results = res["downstream_data_parity0_result"].to_list()
    # all-zero row never contributes; at most 1 violation
    assert all(r <= 1 for r in results)


def test_parity_rule_forwarded_alongside_other_columns():
    h_row_32 = _spaced("1" * 32)
    df = _make_base_df(
        downstream_data_parity0_rule=[h_row_32, h_row_32],
        downstream_validate_unpacked=["", ""],
        downstream_exclude_unpacked=[False, False],
    )
    res = unpack_data_packed(df)
    assert "downstream_data_parity0_result" in res.columns
    assert len(res) == 2


def test_parity_result_zero_means_pass():
    h_row = _spaced("1" * 32)
    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"],
            "downstream_version": [downstream.__version__],
            "data_hex": ["ff00ff00"],
            "dstream_storage_bitoffset": [0],
            "dstream_storage_bitwidth": [16],
            "dstream_T_bitoffset": [16],
            "dstream_T_bitwidth": [4],
            "dstream_S": [16],
            "downstream_data_parity0_rule": [h_row],
        }
    )
    res = unpack_data_packed(df)
    # "ff00ff00" has 16 set bits, even parity -> 0
    assert res["downstream_data_parity0_result"].to_list() == [0]


def test_parity_result_as_packed_validation_filter_pass():
    """Parity result can be used as a downstream_filter_packed expression
    to drop rows failing the parity check."""
    h_row = _spaced("1" * 32)
    # "ff00ff00" has 16 set bits (even parity -> 0, passes)
    # "ff00ff07" has 19 set bits (odd parity -> 1, fails)
    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"] * 2,
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": ["ff00ff00", "ff00ff07"],
            "dstream_storage_bitoffset": [0, 0],
            "dstream_storage_bitwidth": [16, 16],
            "dstream_T_bitoffset": [16, 16],
            "dstream_T_bitwidth": [4, 4],
            "dstream_S": [16, 16],
            "downstream_data_parity0_rule": [h_row, h_row],
            "downstream_filter_packed": [
                "pl.col('downstream_data_parity0_result') == 0",
                "pl.col('downstream_data_parity0_result') == 0",
            ],
        }
    )
    res = unpack_data_packed(df)
    # Only the passing row should remain
    assert len(res) == 1
    assert res["downstream_data_parity0_result"].to_list() == [0]


def test_parity_result_as_packed_validation_rule_pass():
    """Parity result can be used as a downstream_validate_packed expression
    to assert all rows pass the parity check."""
    h_row = _spaced("1" * 32)
    # Both rows have even parity -> result 0
    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"] * 2,
            "downstream_version": [downstream.__version__] * 2,
            "data_hex": ["ff00ff00", "ff00ff00"],
            "dstream_storage_bitoffset": [0, 0],
            "dstream_storage_bitwidth": [16, 16],
            "dstream_T_bitoffset": [16, 16],
            "dstream_T_bitwidth": [4, 4],
            "dstream_S": [16, 16],
            "downstream_data_parity0_rule": [h_row, h_row],
            "downstream_validate_packed": [
                "pl.col('downstream_data_parity0_result') == 0",
                "pl.col('downstream_data_parity0_result') == 0",
            ],
        }
    )
    res = unpack_data_packed(df)
    assert len(res) == 2
    assert res["downstream_data_parity0_result"].to_list() == [0, 0]


def test_parity_result_as_packed_validation_rule_fail():
    """Packed validation using parity result raises when a row fails."""
    h_row = _spaced("1" * 32)
    # "ff00ff07" has odd parity -> result 1 -> validation fails
    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"],
            "downstream_version": [downstream.__version__],
            "data_hex": ["ff00ff07"],
            "dstream_storage_bitoffset": [0],
            "dstream_storage_bitwidth": [16],
            "dstream_T_bitoffset": [16],
            "dstream_T_bitwidth": [4],
            "dstream_S": [16],
            "downstream_data_parity0_rule": [h_row],
            "downstream_validate_packed": [
                "pl.col('downstream_data_parity0_result') == 0",
            ],
        }
    )
    with pytest.raises(ValueError):
        unpack_data_packed(df)


def test_parity_result_nonzero_means_fail():
    h_row = _spaced("1" * 32)
    df = pl.DataFrame(
        {
            "dstream_algo": ["dstream.steady_algo"],
            "downstream_version": [downstream.__version__],
            "data_hex": ["ff00ff07"],
            "dstream_storage_bitoffset": [0],
            "dstream_storage_bitwidth": [16],
            "dstream_T_bitoffset": [16],
            "dstream_T_bitwidth": [4],
            "dstream_S": [16],
            "downstream_data_parity0_rule": [h_row],
        }
    )
    res = unpack_data_packed(df)
    # "ff00ff07" has 19 set bits -> odd parity -> 1 violation
    assert res["downstream_data_parity0_result"].to_list() == [1]
