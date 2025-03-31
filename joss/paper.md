---
title: 'Downstream: efficient, constant-space implementations of stream curation algorithms.'
tags:
  - Python
  - Rust
  - C++
authors:
  - name: Connor Yang
    orcid: 0009-0004-1240-2362
    affiliation: 1
  - name: Matthew Andres Moreno
    orcid: 0000-0003-4726-4479
    affiliation: 1
affiliations:
 - name: University of Michigan
   index: 1
date: 10 February 2025
bibliography: paper.bib
---

# Summary

Downstream offers efficient algorithms for curation of continuous data streams across multiple programming languages including C++, Python, Rust, Zig, and the Cerebras Software Language. These data streams consist of a strictly-ordered sequence of read-once inputs that often exceed available memory capacity. While traditional approaches like circular ring buffers address this limitation by retaining only the most recent data points, Downstream maintains representative, approximate records of stream history through three novel algorithms: (1) "steady," which creates evenly spaced snapshots across the entire history; (2) "stretched," which preserves important older data points; and (3) "tilted," which prioritizes recent information. The library features extensive cross-implementation testing, automated documentation and deployment, and is available through standard package managers.

# Statement of Need

Efficient operations over data streams are critical in harnessing the ever-increasing volume and velocity of data generation. Operations over data streams typically hinge on efficient mechanisms to aggregate or summarize history on a rolling basis. For high-volume data streams, it is critical to manage state in a manner that is fast and memory efficient — particularly in resource-constrained or real-time contexts. Work with data streams assumes input greatly exceeds memory capacity, with streams often treated as unbounded. Indeed, real-world computing often requires real-time operations on a continuous, indefinite basis. Notable application domains involving data streams include sensor networks, distributed big-data processing, real-time network traffic analysis, systems log management, fraud monitoring, trading in financial markets, environmental monitoring, and astronomy. Drawing only on primitive, low-level operations and ensuring full, overhead-free use of available memory, this “DStream” framework ideally suits domains that are resource-constrained (e.g., embedded systems), performance-critical (e.g., real-time), and fine-grained (e.g., individual data items as small as single bits or bytes).


# Projects Using the Software

[@moreno2022hstrat]

# Related Software



# Future Work

My research has produced three novel data streaming algorithms that operate within fixed memory constraints while preserving representative information. The "steady" algorithm provides even coverage of elapsed history, the "stretched" algorithm prioritizes preservation of older data points, and the "tilted" algorithm emphasizes recent data while maintaining historical context. To validate these algorithms, I plan to conduct comprehensive benchmarks comparing memory efficiency, throughput, and information retention quality across all five language implementations (Python, C++, Rust, Zig, and CSL). These benchmarks will measure performance under various resource constraints, simulating real-world scenarios in embedded systems and high-throughput applications. I'll also quantify the information preservation capabilities of each algorithm compared to traditional circular buffers using statistical metrics. By semester's end, I aim to complete all language implementations, cross-implementation testing, benchmarking, documentation, and packaging for distribution through standard package managers. The final product will provide researchers with efficient tools for handling large data streams across various computational environments, particularly benefiting resource-constrained and performance-critical applications that require fine-grained data processing.


# Acknowledgements



# References

<div id="refs"></div>

\pagebreak
\appendix