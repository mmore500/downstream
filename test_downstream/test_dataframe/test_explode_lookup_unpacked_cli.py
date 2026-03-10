import os
import subprocess

assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def test_explode_lookup_unpacked_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_unpacked_uint",
            "--help",
        ],
        check=True,
    )


def test_explode_lookup_unpacked_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_unpacked_uint",
            "--version",
        ],
        check=True,
    )


def test_explode_lookup_unpacked_cli_csv():
    output_file = "/tmp/dstream_explode_lookup_unpacked_uint_cli.pqt"
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.explode_lookup_unpacked_uint",
            output_file,
            "--read-kwarg",
            "schema_overrides={'dstream_storage_hex': pl.String}",
        ],
        check=True,
        input=f"{assets}/unpacked.csv".encode(),
    )
    assert os.path.exists(output_file)
