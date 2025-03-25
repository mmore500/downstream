# Quickstart

[Selecting a DStream Algorithm](algorithm.md)

## Ring Buffer Generalization Intuition

![Traditional ring buffer](buffer-2.png)

Data streams consist of a strictly-ordered sequence of read-once inputs that often exceed available memory capacity. Traditional approaches like circular ring buffers address this limitation by maintaining only the most recent data points and discarding older information. In contrast, Downstream maintains representative, approximate records of stream history by introducing three novel algorithms: 1) "steady" creates evenly spaced snapshots across the entire history, 2) "stretched" preserves important older data points, and 3) "tilted" prioritizes recent information.

![DStream](buffer-1.png)

DStream generalizes this concept with by maintaining representative, approximate records of stream history.


## Installing

To install from PyPi with pip, run

`python3 -m pip install downstream`

Or optionally, to install with JIT

`python3 -m pip install "downstream[jit]"`

A containerized release of `downstream` is available via <https://ghcr.io>

```bash
singularity exec docker://ghcr.io/mmore500/downstream python3 -m downstream --help
```

`downstream` is also available in [C++](cpp.md), [Rust](rust.md), [Zig](zig.md), and [CSL](csl.md). Installation instructions are avaiable on each of their respective pages.

## Working with the Data Structure

```

```

## Lookup


## Serializing


## Running Lookup via Dataframe CLI