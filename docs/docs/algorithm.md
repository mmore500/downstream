# Selecting a downstream Algorithm

Downstream offers three core site selection algorithms.
Each one curates a different temporal distribution of stored items while preserving the constant-space property of a traditional ring buffer.

| Algorithm | Distribution | Typical use case |
|-----------|--------------|------------------|
| **Steady** | Uniform spacing across the entire stream | Trend analysis or when every time period matters |
| **Stretched** | Density thins with depth in the stream | Emphasize initial conditions or ancient history |
| **Tilted** | Density thins with item age | Recent-history monitoring |

Hybrid variants combine multiple algorithms by partitioning the buffer.
Their names follow the pattern `hybrid_<ratio>_steady_<ratio>_stretched...`.
The naming convention can be helpful when multiple distributions are desired simultaneously.

All algorithms share the same interface.
However, stretched and tilted variants have ingest limits of up to `2**S - 2` items, where `S` is the surface size.
You can test limits programmatically using `dstream.verify_ingest_capacity`.

For background details see the [Downstream algorithms preprint](https://doi.org/10.48550/arXiv.2409.06199).
