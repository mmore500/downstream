import os
import subprocess

assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def test_unpack_data_packed_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.unpack_data_packed",
            "--help",
        ],
        check=True,
    )


def test_unpack_data_packed_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.unpack_data_packed",
            "--version",
        ],
        check=True,
    )


def test_unpack_data_packed_cli_csv():
    output_file = "/tmp/dstream_unpack_data_packed_cli.csv"
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.unpack_data_packed",
            output_file,
            "--read-kwarg",
            "schema_overrides={'data_hex': pl.String}",
        ],
        check=True,
        input=f"{assets}/packed.csv".encode(),
    )
    assert os.path.exists(output_file)
