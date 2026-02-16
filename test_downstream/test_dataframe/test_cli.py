import os
import subprocess

import pytest

assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def test_cli_unpack_data_packed_uint():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.unpack_data_packed",
            "--version",
        ],
        check=True,
    )

    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.unpack_data_packed",
            "/tmp/dstream_unpack_data_packed.csv",
            "--read-kwarg",
            "schema_overrides={'data_hex': pl.String}",
        ],
        check=True,
        input=f"{assets}/packed.csv".encode(),
    )

    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.unpack_data_packed",
            "/tmp/dstream_unpack_data_packed.csv",
        ],
        check=True,
        input=(f"{assets}/packed.csv\n" * 4096).encode(),
    )


def test_cli_explode_lookup_packed_uint():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_packed_uint",
            "--version",
        ],
        check=True,
    )

    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_packed_uint",
            "/tmp/dstream_explode_lookup_packed_uint.csv",
            "--read-kwarg",
            "schema_overrides={'data_hex': pl.String}",
        ],
        check=True,
        input=f"{assets}/packed.csv".encode(),
    )

    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_packed_uint",
            "/tmp/dstream_explode_lookup_packed_uint.csv",
            "--read-kwarg",
            "schema_overrides={'data_hex': pl.String}",
        ],
        check=True,
        input=(f"{assets}/packed.csv\n" * 4096).encode(),
    )


def test_cli_explode_lookup_unpacked_uint():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_unpacked_uint",
            "--version",
        ],
        check=True,
    )

    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_unpacked_uint",
            "/tmp/dstream_explode_lookup_unpacked_uint.pqt",
            "--read-kwarg",
            "schema_overrides={'dstream_storage_hex': pl.String}",
        ],
        check=True,
        input=f"{assets}/unpacked.csv".encode(),
    )

    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_unpacked_uint",
            "/tmp/dstream_explode_lookup_unpacked_uint.pqt",
            "--shrink-dtypes",
            "--read-kwarg",
            "schema_overrides={'dstream_storage_hex': pl.String}",
        ],
        check=True,
        input=(f"{assets}/unpacked.csv\n" * 4096).encode(),
    )


@pytest.mark.parametrize(
    "target",
    [
        "dstream.compressing_algo.assign_storage_site",
        "dstream.compressing_algo.has_ingest_capacity",
        "dstream.compressing_algo.lookup_ingest_times",
    ],
)
@pytest.mark.parametrize("S", [3, 5, 6, 7, 8, 9, 10, 16])
def test_cli_compressing_nonpow2(target: str, S: int):
    test_cases = "".join(f"{S} {T}\n" for T in range(S * 10))
    result = subprocess.run(
        ["python3", "-m", "downstream", target],
        input=test_cases,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().split("\n")
    assert len(lines) == S * 10


# RE https://github.com/mmore500/downstream/pull/91
def test_cli_regression91():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_packed_uint",
            "--output-filetype",
            "csv",
            "/dev/null",
        ],
        check=True,
        input=(f"{assets}/regression91.pqt").encode(),
    )
