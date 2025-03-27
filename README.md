# Downstream --- C++ Implementation

![downstream wordmark](https://raw.githubusercontent.com/mmore500/downstream/master/docs/assets/downstream-wordmark.png)

[![CI](https://github.com/mmore500/downstream/actions/workflows/ci.yaml/badge.svg?branch=cpp)](https://github.com/mmore500/downstream/actions/workflows/cpp-ci.yaml?query=branch:cpp)
[![GitHub stars](https://img.shields.io/github/stars/mmore500/downstream.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/downstream)
[
![PyPi](https://img.shields.io/pypi/v/downstream.svg)
](https://pypi.python.org/pypi/downstream)
[![DOI](https://zenodo.org/badge/776865597.svg)](https://zenodo.org/doi/10.5281/zenodo.10866541)

downstream provides efficient, constant-space implementations of stream curation algorithms.

-   Free software: MIT license

<!---
-   Documentation: <https://downstream.readthedocs.io>.
-->

## Installation

C++ downstream is packaged as a header-only library.
It can be added to a system-wide include path, or incorporated as a git submodule in another project.

## API Reference

See the [Python quickstart](quickstart.md) for outline and intuition.

Each algorithm variant is accessible through its own namespace:

* Steady: `downstream::dstream_steady`
* Stretched: `downstream::dstream_stretched`
* Tilted: `downstream::dstream_tilted`

See [selecting a dstream algorithm](algorithm.md) for more information.

#### has_ingest_capacity
```cpp
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
bool has_ingest_capacity(const UINT S, const UINT T);
```
Determines if there is capacity to ingest a data item at logical time T.

* `S`: Current site capacity
* `T`: Logical time of data item

#### assign_storage_site
```cpp
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T);
```
Site selection algorithm for steady curation. Returns selected site or nullopt if data should be discarded.

* `S`: Current site capacity
* `T`: Logical time of data item

### Internal Implementation
```cpp
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T);
```

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
