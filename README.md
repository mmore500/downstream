# Downstream --- C++ Implementation

![downstream wordmark](https://raw.githubusercontent.com/mmore500/downstream/master/docs/assets/downstream-wordmark.png)

[![CI](https://github.com/mmore500/downstream/actions/workflows/cpp-ci.yaml/badge.svg?branch=cpp)](https://github.com/mmore500/downstream/actions/workflows/cpp-ci.yaml?query=branch:cpp)
[![GitHub stars](https://img.shields.io/github/stars/mmore500/downstream.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/downstream)
[
![PyPi](https://img.shields.io/pypi/v/downstream.svg)
](https://pypi.python.org/pypi/downstream)
[![DOI](https://zenodo.org/badge/776865597.svg)](https://zenodo.org/doi/10.5281/zenodo.10866541)

downstream provides efficient, constant-space implementations of stream curation algorithms.

-   Free software: MIT license
-   Documentation: <https://mmore500.github.io/downstream>.

## Installation

C++ downstream is packaged as a header-only library.
It can be added to a system-wide include path, or incorporated as a git submodule in another project.

## API Reference

See the [Python quickstart](https://mmore500.github.io/downstream/quickstart) for outline and intuition.

Each algorithm variant is accessible through its own namespace:

* Steady: `downstream::dstream_steady`
* Stretched: `downstream::dstream_stretched`
* Tilted: `downstream::dstream_tilted`

See [selecting a dstream algorithm](https://mmore500.github.io/downstream/algorithm) for more information.

#### `has_ingest_capacity`
```cpp
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
bool has_ingest_capacity(const UINT S, const UINT T);
```
Determines if there is capacity to ingest a data item at logical time T.

* `S`: Buffer size (must be a power of two)
* `T`: Stream position of data item (zero-indexed)

#### `assign_storage_site`
```cpp
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T);
```
Site selection algorithm for steady curation. Returns selected site or nullopt if data should be discarded.

* `S`: Buffer size (must be a power of two)
* `T`: Stream position of data item (zero-indexed)

#### `_assign_storage_site` (low-level interface)
```cpp
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T);
```

## Citing

If downstream contributes to a scientific publication, please cite it as

> Yang C., Wagner J., Dolson E., Zaman L., & Moreno M. A. (2025). Downstream: efficient cross-platform algorithms for fixed-capacity stream downsampling. arXiv preprint arXiv:2506.12975. https://doi.org/10.48550/arXiv.2506.12975

```bibtex
@misc{yang2025downstream,
      doi={10.48550/arXiv.2506.12975},
      url={https://arxiv.org/abs/2506.12975},
      title={Downstream: efficient cross-platform algorithms for fixed-capacity stream downsampling},
      author={Connor Yang and Joey Wagner and Emily Dolson and Luis Zaman and Matthew Andres Moreno},
      year={2025},
      eprint={2506.12975},
      archivePrefix={arXiv},
      primaryClass={cs.DS},
}
```

And don't forget to leave a [star on GitHub](https://github.com/mmore500/downstream/stargazers)!
