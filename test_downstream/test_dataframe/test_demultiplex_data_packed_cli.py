import subprocess


def test_demultiplex_data_packed_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.demultiplex_data_packed",
            "--help",
        ],
        check=True,
    )


def test_demultiplex_data_packed_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream.dataframe.demultiplex_data_packed",
            "--version",
        ],
        check=True,
    )
