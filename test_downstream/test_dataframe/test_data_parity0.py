import polars as pl
import pytest

import downstream
from downstream.dataframe import unpack_data_packed
from downstream.dataframe._unpack_data_packed import _compute_data_parity0


class TestComputeDataParity0:
    """Unit tests for _compute_data_parity0."""

    def test_empty_h_matrix(self):
        assert _compute_data_parity0("ff", "") == ""

    def test_single_row_all_ones(self):
        # data_hex="f" -> bits="1111", H row="1111" -> 1^1^1^1 = 0
        assert _compute_data_parity0("f", "1111") == "0"

    def test_single_row_parity_one(self):
        # data_hex="7" -> bits="0111", H row="1111" -> 0^1^1^1 = 1
        assert _compute_data_parity0("7", "1111") == "1"

    def test_single_row_selective(self):
        # data_hex="a" -> bits="1010", H row="1010" -> 1&1 ^ 0&0 ^ 1&1 ^ 0&0 = 0
        assert _compute_data_parity0("a", "1010") == "0"

    def test_multi_row(self):
        # data_hex="a" -> bits="1010"
        # H row 0: "1000" -> 1
        # H row 1: "0100" -> 0
        assert _compute_data_parity0("a", "1000 0100") == "10"

    def test_two_hex_chars(self):
        # data_hex="ff" -> bits="11111111"
        # H row: "10101010" -> 1^1^1^1 = 0
        assert _compute_data_parity0("ff", "10101010") == "0"

    def test_identity_rows(self):
        # data_hex="a" -> bits="1010"
        # H = identity matrix picks out individual bits
        result = _compute_data_parity0("a", "1000 0100 0010 0001")
        assert result == "1010"

    def test_mismatched_length_raises(self):
        with pytest.raises(ValueError, match="does not match"):
            _compute_data_parity0("ff", "101")

    def test_zero_data(self):
        # data_hex="0" -> bits="0000", any H row -> syndrome 0
        assert _compute_data_parity0("0", "1111") == "0"
        assert _compute_data_parity0("0", "1111 1010") == "00"

    def test_longer_hex(self):
        # data_hex="0f" -> bits="00001111"
        # H row: "00001111" -> 0^0^0^0^1^1^1^1 = 0
        assert _compute_data_parity0("0f", "00001111") == "0"
        # H row: "00001110" -> 1^1^1 = 1
        assert _compute_data_parity0("0f", "00001110") == "1"


class TestUnpackDataPackedWithParity:
    """Integration tests for downstream_data_parity0_rule in unpack_data_packed."""

    def _make_base_df(self, **extra_cols):
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

    def test_no_rule_column(self):
        """Without the rule column, no result column should appear."""
        df = self._make_base_df()
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" not in res.columns
        assert "downstream_data_parity0_rule" not in res.columns

    def test_rule_produces_result(self):
        """With a rule column, a result column should be produced."""
        # data_hex="aa11ccdd" -> 32 bits
        # Use a simple single-row H matrix of all 1s (32 bits)
        h_row_32 = "1" * 32
        df = self._make_base_df(
            downstream_data_parity0_rule=[h_row_32, h_row_32],
        )
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" in res.columns
        assert "downstream_data_parity0_rule" not in res.columns
        # results should be single-character strings ("0" or "1")
        results = res["downstream_data_parity0_result"].to_list()
        assert all(r in ("0", "1") for r in results)

    def test_rule_identity_matrix(self):
        """Identity-like H matrix extracts individual bits."""
        # data_hex="f" would be 4 bits, but we need a full valid packed row
        # Use data_hex="f0000000" (32 bits), extract first 4 bits
        h_rows = []
        for i in range(32):
            row = ["0"] * 32
            row[i] = "1"
            h_rows.append("".join(row))
        h_matrix = " ".join(h_rows)

        df = self._make_base_df(
            downstream_data_parity0_rule=[h_matrix, h_matrix],
        )
        res = unpack_data_packed(df)
        results = res["downstream_data_parity0_result"].to_list()
        # Each result should be a 32-char binary string matching data_hex bits
        assert len(results[0]) == 32
        # "aa11ccdd" in binary
        expected_bits = bin(int("aa11ccdd", 16))[2:].zfill(32)
        assert results[0] == expected_bits

    def test_rule_empty_string(self):
        """Empty rule string produces empty result."""
        df = self._make_base_df(
            downstream_data_parity0_rule=["", ""],
        )
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" in res.columns
        results = res["downstream_data_parity0_result"].to_list()
        assert results == ["", ""]

    def test_rule_mismatched_length_raises(self):
        """H matrix row length not matching data bits should raise."""
        df = self._make_base_df(
            downstream_data_parity0_rule=["101", "101"],
        )
        with pytest.raises(ValueError, match="does not match"):
            unpack_data_packed(df)

    def test_rule_parity_check_passes(self):
        """A well-constructed H matrix yields all-zero syndrome."""
        # Construct data where parity check passes
        # data_hex="00" -> bits="00000000"
        # Any H matrix -> syndrome all zeros
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
                "downstream_data_parity0_rule": [
                    "00000000000000000000000000000000"
                ],
            }
        )
        res = unpack_data_packed(df)
        assert res["downstream_data_parity0_result"].to_list() == ["0"]

    def test_rule_with_categorical_type(self):
        """Rule column as Categorical should also work."""
        h_row_32 = "1" * 32
        df = self._make_base_df(
            downstream_data_parity0_rule=[h_row_32, h_row_32],
        ).cast({"downstream_data_parity0_rule": pl.Categorical})
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" in res.columns

    def test_rule_multiple_h_rows(self):
        """Multiple H matrix rows produce multi-bit syndrome."""
        # data_hex="aa11ccdd" -> 32 bits
        # 2 rows of H matrix, each 32 bits
        row1 = "1" * 32
        row2 = "0" * 32
        h_matrix = f"{row1} {row2}"
        df = self._make_base_df(
            downstream_data_parity0_rule=[h_matrix, h_matrix],
        )
        res = unpack_data_packed(df)
        results = res["downstream_data_parity0_result"].to_list()
        # Each result should be 2 chars (one per H row)
        assert all(len(r) == 2 for r in results)
        # Second bit always 0 (all-zero H row)
        assert all(r[1] == "0" for r in results)

    def test_rule_forwarded_alongside_other_columns(self):
        """Parity result coexists with other optional columns."""
        h_row_32 = "1" * 32
        df = self._make_base_df(
            downstream_data_parity0_rule=[h_row_32, h_row_32],
            downstream_validate_unpacked=["", ""],
            downstream_exclude_unpacked=[False, False],
        )
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" in res.columns
        assert len(res) == 2
