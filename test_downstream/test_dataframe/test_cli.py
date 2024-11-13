import os
import subprocess

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
        ],
        check=True,
        input=f"{assets}/packed.csv".encode(),
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
        ],
        check=True,
        input=f"{assets}/packed.csv".encode(),
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
            "--shrink-dtypes",
        ],
        check=True,
        input=f"{assets}/unpacked.csv".encode(),
    )
