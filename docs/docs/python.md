# Python API Reference

## Contents

- [Algorithm API Example: `dstream.steady_algo`](#algorithm-api-example-dstreamsteady_algo)
- [Additional algorithms in `dstream`](#additional-algorithms-in-dstream)
- [Container API: `dsurf.Surface`](#container-api-dsurfsurface)
- [Dataframe API](#dataframe-api)


---
# Algorithm API Example: `dstream.steady_algo`

Implements the steady downsampling algorithm, which retains items in a uniform distribution across elapsed stream history.

Import as
```python3
from downstream.dstream import steady_algo
```

Or, alternately
```python3
from downstream import dstream
steady_algo = dstream.steady_algo
```


## `steady_algo.assign_storage_site`

::: steady_algo._steady_assign_storage_site.steady_assign_storage_site

## `steady_algo.assign_storage_site_batched`

::: steady_algo._steady_assign_storage_site_batched.steady_assign_storage_site_batched


## `steady_algo.get_ingest_capacity`

::: steady_algo._steady_get_ingest_capacity.steady_get_ingest_capacity


## `steady_algo.has_ingest_capacity`

::: steady_algo._steady_has_ingest_capacity.steady_has_ingest_capacity


## `steady_algo.has_ingest_capacity_batched`

::: steady_algo._steady_has_ingest_capacity_batched.steady_has_ingest_capacity_batched


## `steady_algo.lookup_ingest_times`

::: steady_algo._steady_lookup_ingest_times.steady_lookup_ingest_times


## `steady_algo.lookup_ingest_times_batched`

::: steady_algo._steady_lookup_ingest_times_batched.steady_lookup_ingest_times_batched


## `steady_algo.lookup_ingest_times_eager`

::: steady_algo._steady_lookup_ingest_times_eager.steady_lookup_ingest_times_eager


---
# Additional Algorithms in `dstream`

The following additional algorithms are available in the `dstream` module:

* `circular_algo` implements a simple ring buffer for last *n* sampling.
* `compressing_algo` implements steady curation via [Gunther's compressing circular buffer algorithm](https://doi.org/10.1145/2559995).
* `hybrid_0_steady_1_stretched_2_algo` for hybrid downsampling combining steady and stretched algorithms.
* `hybrid_0_steady_1_stretchedxtc_2_algo` for hybrid downsampling combining steady and stretchedxtc algorithms.
* `hybrid_0_steady_1_tilted_2_algo` for hybrid downsampling combining steady and tilted algorithms.
* `hybrid_0_steady_1_tiltedxtc_2_algo` for hybrid downsampling combining steady and tiltedxtc algorithms.
* `primed_algo_*` which fills surface left-to-right before delegating to another algorithm.
* `stretched_algo` for stretched downsampling.
* `stretchedxtc_algo` for stretched downsampling, with infinite `T` domain extension.
* `tilted_algo` for tilted downsampling.
* `tiltedxtc_algo` for stretched downsampling, with infinite `T` domain extension.


These algorithms follow identical API conventions as `steady_algo`, as shown above.

---

# Container API: `dsurf.Surface`

Import as
```python3
from downstream.dsurf import Surface
```

Or, alternately
```python3
from downstream import dsurf
Surface = dstream.Surface
```

## `dsurf.Surface`

::: dsurf.Surface

# Dataframe API

Import as
```python3
from downstream import dataframe
```

## `dataframe.explode_lookup_packed`

::: downstream.dataframe._explode_lookup_packed.explode_lookup_packed

## `dataframe.explode_lookup_unpacked`

::: downstream.dataframe._explode_lookup_unpacked.explode_lookup_unpacked

## `dataframe.unpack_data_packed`

::: downstream.dataframe._unpack_data_packed.unpack_data_packed

# Command Line Interface

For information on available command line interface (CLI) commands
```bash
python3 -m downstream --help
```
