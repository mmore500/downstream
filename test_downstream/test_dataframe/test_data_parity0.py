import polars as pl
import pytest

import downstream
from downstream.dataframe import unpack_data_packed
from downstream.dataframe._unpack_data_packed import _calculate_data_parity0


class TestComputeDataParity0:
    """Unit tests for _calculate_data_parity0."""

    def test_empty_h_matrix(self):
        assert _calculate_data_parity0("ff", "") == 0

    def test_single_row_all_ones(self):
        # data_hex="f" -> bits="1111", H row="1111" -> 1^1^1^1 = 0
        assert _calculate_data_parity0("f", "1111") == 0

    def test_single_row_parity_one(self):
        # data_hex="7" -> bits="0111", H row="1111" -> 0^1^1^1 = 1
        assert _calculate_data_parity0("7", "1111") == 1

    def test_single_row_selective(self):
        # data_hex="a" -> bits="1010", H row="1010" -> 1&1 ^ 0&0 ^ 1&1 ^ 0&0 = 0
        assert _calculate_data_parity0("a", "1010") == 0

    def test_multi_row(self):
        # data_hex="a" -> bits="1010"
        # H row 0: "1000" -> 1 (violation)
        # H row 1: "0100" -> 0
        assert _calculate_data_parity0("a", "1000 0100") == 1

    def test_two_hex_chars(self):
        # data_hex="ff" -> bits="11111111"
        # H row: "10101010" -> 1^1^1^1 = 0
        assert _calculate_data_parity0("ff", "10101010") == 0

    def test_identity_rows(self):
        # data_hex="a" -> bits="1010"
        # H = identity matrix, syndrome = data bits = "1010", 2 nonzero
        result = _calculate_data_parity0("a", "1000 0100 0010 0001")
        assert result == 2

    def test_mismatched_length_raises(self):
        with pytest.raises(ValueError, match="does not match"):
            _calculate_data_parity0("ff", "101")

    def test_zero_data(self):
        # data_hex="0" -> bits="0000", any H row -> syndrome 0
        assert _calculate_data_parity0("0", "1111") == 0
        assert _calculate_data_parity0("0", "1111 1010") == 0

    def test_longer_hex(self):
        # data_hex="0f" -> bits="00001111"
        # H row: "00001111" -> 0^0^0^0^1^1^1^1 = 0
        assert _calculate_data_parity0("0f", "00001111") == 0
        # H row: "00001110" -> 1^1^1 = 1
        assert _calculate_data_parity0("0f", "00001110") == 1

    def test_all_violations(self):
        # data_hex="f" -> bits="1111"
        # H = identity, syndrome = "1111", all 4 are violations
        result = _calculate_data_parity0("f", "1000 0100 0010 0001")
        assert result == 4

    def test_no_violations(self):
        # data_hex="0" -> bits="0000"
        # H = identity, syndrome = "0000", 0 violations
        result = _calculate_data_parity0("0", "1000 0100 0010 0001")
        assert result == 0


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
        h_row_32 = "1" * 32
        df = self._make_base_df(
            downstream_data_parity0_rule=[h_row_32, h_row_32],
        )
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" in res.columns
        assert "downstream_data_parity0_rule" not in res.columns
        assert res["downstream_data_parity0_result"].dtype == pl.UInt32

    def test_rule_identity_matrix(self):
        """Identity H matrix: violation count equals number of set bits."""
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
        # Identity matrix syndrome = data bits; violations = popcount
        expected_0 = bin(int("aa11ccdd", 16)).count("1")
        expected_1 = bin(int("221188dd", 16)).count("1")
        assert results[0] == expected_0
        assert results[1] == expected_1

    def test_rule_empty_string(self):
        """Empty rule string produces zero violations."""
        df = self._make_base_df(
            downstream_data_parity0_rule=["", ""],
        )
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" in res.columns
        results = res["downstream_data_parity0_result"].to_list()
        assert results == [0, 0]

    def test_rule_mismatched_length_raises(self):
        """H matrix row length not matching data bits should raise."""
        df = self._make_base_df(
            downstream_data_parity0_rule=["101", "101"],
        )
        with pytest.raises(ValueError, match="does not match"):
            unpack_data_packed(df)

    def test_rule_parity_check_passes(self):
        """All-zero H matrix yields zero violations."""
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
        assert res["downstream_data_parity0_result"].to_list() == [0]

    def test_rule_with_categorical_type(self):
        """Rule column as Categorical should also work."""
        h_row_32 = "1" * 32
        df = self._make_base_df(
            downstream_data_parity0_rule=[h_row_32, h_row_32],
        ).cast({"downstream_data_parity0_rule": pl.Categorical})
        res = unpack_data_packed(df)
        assert "downstream_data_parity0_result" in res.columns

    def test_rule_multiple_h_rows(self):
        """Multiple H matrix rows: count nonzero syndrome bits."""
        # 2 rows: all-1s row and all-0s row
        row1 = "1" * 32
        row2 = "0" * 32
        h_matrix = f"{row1} {row2}"
        df = self._make_base_df(
            downstream_data_parity0_rule=[h_matrix, h_matrix],
        )
        res = unpack_data_packed(df)
        results = res["downstream_data_parity0_result"].to_list()
        # All-zero H row never contributes; all-1s row may or may not
        # At most 1 violation (from the all-1s row)
        assert all(r <= 1 for r in results)

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

    def test_result_zero_means_pass(self):
        """Zero violations means data passes parity check."""
        # data_hex with even popcount and all-1s H row -> 0 violations
        # "ff" has 8 set bits -> even parity -> syndrome = 0
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
                "downstream_data_parity0_rule": ["1" * 32],
            }
        )
        res = unpack_data_packed(df)
        # "ff00ff00" has 16 set bits, even parity -> 0
        assert res["downstream_data_parity0_result"].to_list() == [0]

    def test_result_nonzero_means_fail(self):
        """Nonzero violations means data fails parity check."""
        # "ff00ff07" has 19 set bits -> odd parity -> 1 violation
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
                "downstream_data_parity0_rule": ["1" * 32],
            }
        )
        res = unpack_data_packed(df)
        assert res["downstream_data_parity0_result"].to_list() == [1]
