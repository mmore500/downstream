# Quickstart


## Ring Buffer Generalization Intuition


Data streams consist of a strictly ordered sequence of read once inputs.
They often exceed available memory capacity.

Traditional approaches like circular ring buffers keep only the most recent data points.
They discard older information.

![Traditional ring buffer](buffer-2.png)


In contrast, downstream maintains representative records of stream history using three algorithms.
The steady algorithm creates evenly spaced snapshots across the entire history.
The stretched algorithm preserves important older data points.
The tilted algorithm prioritizes recent information.
![downstream](buffer-1.png)
We provide a more detailed description of available algorithms in [Selecting a downstream Algorithm](algorithm.md).
That page offers guidance on picking one for your use case.

## Installing

To install from PyPi with pip, run

```bash
python3 -m pip install downstream
```

Or optionally, to install with JIT

```bash
python3 -m pip install "downstream[jit]"
```

A containerized release of downstream is available via <https://ghcr.io>.

```bash
singularity exec docker://ghcr.io/mmore500/downstream python3 -m downstream --help
```

downstream is also available in [C++](cpp.md), [Rust](rust.md), [Zig](zig.md), and [CSL](csl.md).

Installation instructions are available on each of their respective pages.

## Working with the Data Structure

- Buffer size must be a power of 2 (e.g., 8, 16, 32)
- Site assignment maps data item index T to a storage location using either:

    - `assign_storage_site`: For processing single data points
    - `assign_storage_site_batched`: For efficient processing of multiple data points

- For [hstrat](https://github.com/mmore500/hstrat) users: you can store a random differentia or make a random choice whether to toggle single-bit differentia with each generations elapsed

### Example: Using the Steady Algorithm
```python
from downstream import dstream

# Initialize a buffer with size 8 (must be a power of 2)
buffer_size = 8

# Process a stream of data items
for data_index in range(20):
    # Determine site based on buffer size and index T
    site = dstream.steady_algo.assign_storage_site(buffer_size, data_index)

    if site is not None:
        # Store data at the selected site
        print(f"Data point {data_index} stored at position {site}")
```

## Lookup
The Python implementation provides `lookup_surface` to recover the stream index of values stored in a buffer.
For high throughput workloads, use `lookup_surface_batched` which applies numpy vectorization and numba parallelization for speed.

Most workflows serialize buffer contents and run lookups in bulk rather than online.
The following sections describe this process.

## Serializing
After processing a stream, the buffer and counter `T` can be converted into a hexadecimal representation using `dstream.hexlify_surface`.
We recommend including a `dstream_version` column in any saved dataframe.
Each language branch provides small examples demonstrating serialization.

## Running Lookup via Dataframe CLI
Serialized data can be analyzed with the command line tool
```
python3 -m downstream dataframe explode --input mydata.csv --output long.csv
```
The command expands the stored hexadecimal buffer into one row per data item with its lookup index.
Validators are also available for sanity checking serialized records.
