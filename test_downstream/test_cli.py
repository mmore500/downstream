import subprocess


def test_downstream_cli_help():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream",
            "--help",
        ],
        check=True,
    )


def test_downstream_cli_version():
    subprocess.run(
        [
            "python3",
            "-m",
            "downstream",
            "--version",
        ],
        check=True,
    )


def test_downstream_cli_steady_algo():
    test_cases = "".join(f"8 {T}\n" for T in range(80))
    result = subprocess.run(
        [
            "python3",
            "-m",
            "downstream",
            "dstream.steady_algo.assign_storage_site",
        ],
        input=test_cases,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 80


def test_downstream_cli_stretched_algo():
    test_cases = "".join(f"8 {T}\n" for T in range(80))
    result = subprocess.run(
        [
            "python3",
            "-m",
            "downstream",
            "dstream.stretched_algo.assign_storage_site",
        ],
        input=test_cases,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 80


def test_downstream_cli_tilted_algo():
    test_cases = "".join(f"8 {T}\n" for T in range(80))
    result = subprocess.run(
        [
            "python3",
            "-m",
            "downstream",
            "dstream.tilted_algo.assign_storage_site",
        ],
        input=test_cases,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 80


def test_downstream_cli_has_ingest_capacity():
    test_cases = "".join(f"8 {T}\n" for T in range(80))
    result = subprocess.run(
        [
            "python3",
            "-m",
            "downstream",
            "dstream.steady_algo.has_ingest_capacity",
        ],
        input=test_cases,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 80


def test_downstream_cli_lookup_ingest_times():
    test_cases = "".join(f"8 {T}\n" for T in range(80))
    result = subprocess.run(
        [
            "python3",
            "-m",
            "downstream",
            "dstream.steady_algo.lookup_ingest_times",
        ],
        input=test_cases,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 80
