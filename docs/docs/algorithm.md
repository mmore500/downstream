# Algorithm Selection

Downstream offers three core site selection algorithms.
Each one curates a different temporal distribution of stored items while preserving the constant-space property of a traditional ring buffer.

| Algorithm | Distribution | Typical use case |
|-----------|--------------|------------------|
| **Steady** | Uniform spacing across the entire stream | Trend analysis or when every time period matters |
| **Stretched** | Density thins with depth in the stream | Emphasize initial conditions or ancient history |
| **Tilted** | Density thins with item age | Recent-history monitoring |

Hybrid variants combine multiple algorithms by partitioning the buffer.

All algorithms share the same interface.
However, naive stretched and tilted algorithms have ingest limits of up to `2**S - 2` items, where `S` is the surface size.
You can test limits programmatically using `*_algo.has_ingest_capacity` or `*_algo.get_ingest_capacity`.

For more details on algorithm behavior and guarantees, see our [paper on the underlying algorithms](https://doi.org/10.48550/arXiv.2409.06199).
For [hstrat](https://github.com/mmore500/hstrat) users, analysis of how algorithm choice affects phylogeny reconstruction is available [here](https://doi.org/10.1109/ALIFE-CIS64968.2025.10979833).
