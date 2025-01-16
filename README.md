# Downstream

[![CSL CI](https://github.com/mmore500/downstream/actions/workflows/csl-ci.yaml/badge.svg?branch=csl)](https://github.com/mmore500/downstream/actions/workflows/csl-ci.yaml?query=branch:csl)
[![Python CI](https://github.com/mmore500/downstream/actions/workflows/python-ci.yaml/badge.svg?branch=python)](https://github.com/mmore500/downstream/actions/workflows/python-ci.yaml?query=branch:python)
[![Rust CI](https://github.com/mmore500/downstream/actions/workflows/rust-ci.yaml/badge.svg?branch=rust)](https://github.com/mmore500/downstream/actions/workflows/rust-ci.yaml?query=branch:csl)
[![Zig CI](https://github.com/mmore500/downstream/actions/workflows/zig-ci.yaml/badge.svg?branch=zig)](https://github.com/mmore500/downstream/actions/workflows/zig-ci.yaml?query=branch:zig)
[![GitHub stars](https://img.shields.io/github/stars/mmore500/downstream.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/downstream)
[
![PyPi](https://img.shields.io/pypi/v/downstream.svg)
](https://pypi.python.org/pypi/downstream)
![Crates.io](https://img.shields.io/crates/v/downstream)
[![DOI](https://zenodo.org/badge/776865597.svg)](https://zenodo.org/doi/10.5281/zenodo.10866541)
<!-- [![Documentation Status](https://readthedocs.org/projects/downstream/badge/?version=latest)](https://downstream.readthedocs.io/en/latest/?badge=latest) -->
<!-- [![documentation coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fmmore500.github.io%2Fdownstream%2Fdocumentation-coverage-badge.json)](https://downstream.readthedocs.io/en/latest/) -->
<!-- [![code coverage status](https://codecov.io/gh/mmore500/downstream/branch/master/graph/badge.svg)](https://codecov.io/gh/mmore500/downstream) -->
<!-- [![dotos](https://img.shields.io/endpoint?url=https%3A%2F%2Fmmore500.com%2Fdownstream%2Fdoto-badge.json)](https://github.com/mmore500/downstream/search?q=todo+OR+fixme&type=) -->

downstream provides efficient, constant-space implementations of stream curation algorithms.

-   Free software: MIT license

<!---
-   Documentation: <https://downstream.readthedocs.io>.
-->

## Installation

To install from PyPi with pip, run

`python3 -m pip install "downstream[jit]"`

A containerized release of `downstream` is available via <https://ghcr.io>

```bash
singularity exec docker://ghcr.io/mmore500/downstream python3 -m downstream --help
```

## Documentation

Slide deck & graphics for this project are at <https://hopth.ru/ce>.

See `https://github.com/mmore500/hstrat-surface-concept` for usage examples.

## Citing

If downstream contributes to a scientific publication, please cite it as

> Matthew Andres Moreno. (2024). mmore500/downstream. Zenodo. https://zenodo.org/doi/10.5281/zenodo.10866541

```bibtex
@software{moreno2024downstream,
  author = {Matthew Andres Moreno},
  title = {mmore500/downstream},
  month = mar,
  year = 2024,
  publisher = {Zenodo},
  doi = {10.5281/zenodo.10866541},
  url = {https://zenodo.org/doi/10.5281/zenodo.10866541}
}
```

And don't forget to leave a [star on GitHub](https://github.com/mmore500/downstream/stargazers)!

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [mmore500/cookiecutter-dishtiny-project](https://github.com/mmore500/cookiecutter-dishtiny-project) project template.

<!---
This package uses [Empirical](https://github.com/devosoft/Empirical#readme), a library of tools for scientific software development, with emphasis on also being able to build web interfaces using Emscripten.
-->
