"""Retain half a rolling window and half a steady sample of older arrivals.

For a power-of-two buffer size S >= 4, the latest S/2 arrivals are retained
alongside steady_algo(S/2)'s sample of the preceding prefix. These are logical
groups: items age into the historical sample in place, without relocation or
per-item metadata. Before T reaches S, every arrival is retained.

T counts calls to this algorithm. To sample every 2**n raw timesteps, call
the algorithm only on those timesteps and supply the sampled stream's index.
Multiply reconstructed timestamps by 2**n to recover raw timestamps.

See docs/rolling_steady.md for the derivation and complexity assumptions.
"""

import lazy_loader

__getattr__, __dir__, _ = lazy_loader.attach_stub(__name__, __file__)
