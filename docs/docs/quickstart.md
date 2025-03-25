# Quickstart

[Selecting a DStream Algorithm](algorithm.md)

## Ring Buffer Generalization Intuition

![Traditional ring buffer](buffer-2.png)

A traditional circular ring buffer maintains the n most recent data points through oldest-value overwriting.

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