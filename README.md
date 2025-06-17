# Downstream --- Zig Implementation

![downstream wordmark](https://raw.githubusercontent.com/mmore500/downstream/master/docs/assets/downstream-wordmark.png)

[![CI](https://github.com/mmore500/downstream/actions/workflows/zig-ci.yaml/badge.svg?branch=zig)](https://github.com/mmore500/downstream/actions/workflows/zig-ci.yaml?query=branch:zig)
[![GitHub stars](https://img.shields.io/github/stars/mmore500/downstream.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/downstream)
[![DOI](https://zenodo.org/badge/776865597.svg)](https://zenodo.org/doi/10.5281/zenodo.10866541)

downstream provides efficient, constant-space implementations of stream curation algorithms.

-   Free software: MIT license
-   Documentation: <https://mmore500.github.io/downstream>

## Installation

Zig downstream is packaged as a source module and CLI. Clone this repository and
build with `zig build`.  The resulting executable will be available at
`./zig-out/bin/downstream`.

To embed downstream into another project, add it as a module within your own
`build.zig` script, e.g.

```zig
const downstream = b.addModule("downstream", .{ .root_source_file =
    b.path("path/to/downstream/src/main.zig") });
```

## API Reference

See the [Python quickstart](https://mmore500.github.io/downstream/quickstart) for
outline and intuition.

Each algorithm variant is accessible through its own namespace:

* Steady: `downstream.dstream.steady_algo`
* Stretched: `downstream.dstream.stretched_algo`
* Tilted: `downstream.dstream.tilted_algo`

See [selecting a dstream algorithm](https://mmore500.github.io/downstream/algorithm)
for more information.

#### `has_ingest_capacity`
```zig
pub fn has_ingest_capacity(comptime u: type, S: u, T: u) bool
```
Determines if there is capacity to ingest a data item at logical time `T`.

* `S`: Current site capacity
* `T`: Logical time of data item

#### `assign_storage_site`
```zig
pub fn assign_storage_site(comptime u: type, S: u, T: u) u
```
Site selection algorithm for steady curation. Returns selected site or `S` if
data should be discarded.

* `S`: Current site capacity
* `T`: Logical time of data item

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
