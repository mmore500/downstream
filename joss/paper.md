---
title: 'Downstream: efficient cross-platform algorithms for fixed-capacity stream downsampling'
tags:
  - Python
  - Rust
  - C++
  - Zig
  - CSL
authors:
  - name: Connor Yang
    orcid: 0009-0004-1240-2362
    affiliation: "1, 5"
  - name: Joey Wagner
    orcid: 0009-0000-6141-976X
    affiliation: "6, 9"
  - name: Emily Dolson
    orcid: 0000-0001-8616-4898
    affiliation: "7, 8, 9"
  - name: Luis Zaman
    orcid: 0000-0001-6838-7385
    affiliation: "2, 3, 4"
  - name: Matthew Andres Moreno
    orcid: 0000-0003-4726-4479
    affiliation: "2, 3, 4, 5"
affiliations:
  - name: Undergraduate Research Opportunities Program
    index: 1
  - name: Department of Ecology and Evolutionary Biology
    index: 2
  - name: Center for the Study of Complex Systems
    index: 3
  - name: Michigan Institute for Data and AI in Society
    index: 4
  - name: University of Michigan, Ann Arbor, United States
    index: 5
  - name: Professorial Assistantship Program
    index: 6
  - name: Department of Computer Science and Engineering
    index: 7
  - name: Program in Ecology, Evolution, and Behavior
    index: 8
  - name: Michigan State University, East Lansing, United States
    index: 9
date: 10 February 2025
bibliography: paper.bib
---

# Summary

Due to ongoing accrual over long durations, a defining characteristic of real-world data streams is the requirement for rolling, often real-time, mechanisms to coarsen or summarize stream history.
One common data structure for this purpose is the ring buffer, which maintains a running downsample comprising most recent stream data.
In some downsampling scenarios, however, it can instead be necessary to maintain data items spanning the entirety of elapsed stream history.
Fortunately, approaches generalizing the ring buffer mechanism have been devised to support alternate downsample compositions, while maintaining the ring buffer's update efficiency and optimal use of memory capacity [@Moreno2024;@Gunther2014].
The Downstream library implements algorithms supporting three such downsampling generalizations: (1) "steady," which curates data evenly spaced across the stream history; (2) "stretched," which prioritizes older data; and (3) "tilted," which prioritizes recent data.
To enable a broad spectrum of applications ranging from embedded devices to high-performance computing nodes and AI/ML hardware accelerators, Downstream supports multiple programming languages, including C++, Rust, Python, Zig, and the Cerebras Software Language.
For seamless interoperation, the library incorporates distribution through multiple packaging frameworks, extensive cross-implementation testing, and cross-implementation documentation.

# Statement of Need

Efficient data stream processing is crucial in modern computing systems, where workloads of continuous, high-volume data have become more prevalent [@Cordeiro2016].
Applications of data stream processing include sensor networks [@Eiman2003], distributed big-data processing [@he2010comet], real-time network traffic analysis [@Johnson2005;@Muthukrishnan2005], systems log management [@Fischer2012], fraud monitoring [@RajeshwariU2016], trading in financial markets [@Agarwal2009], environmental monitoring [@Hill2009], and astronomical surveys [@Graham2012], which all generate data at rates that exceed practical storage capacity, while requiring analysis across varying time horizons.

Within the broader ecosystem of tools for data stream processing, Downstream targets, in specific, use cases that require best-effort downsampling within fixed memory capacity.
Within this domain, Downstream especially benefits scenarios involving:

1. real-time operations, due to support for $\mathcal{O}(1)$ data processing;
2. need for compact memory layout with minimal overhead, especially where individual data items are small (e.g., single bits or bytes) relative to bookkeeping metadata or where curated downsamples are frequently copied/transmitted; and/or
3. support for SIMD acceleration (e.g., ARM SVE, x86 AVX, GPU, etc.), due to branchless structure of underlying algorithms.

As such, Downstream is well-suited to emerging AI/ML hardware accelerator platforms, such as Cerebras Systems' Wafer-Scale Engine (WSE) [@Lie2023], Graphcore's Intelligence Processing Unit [@gepner2024performance], Tenstorrent's Tensix processors [@vasiljevic2021compute], and Groq's GropChip [@abts2022groq].
Pursuing an aggressive scale-out paradigm, these platforms bring hundreds, thousands, or --- in the case of the Wafer-Scale Engine --- hundreds of thousands of processing elements to bear on a single chip.
As a design trade-off, however, on-device memory available per processor on these platforms is generally scarce.
For instance, although the Cerebras WSE-2 supplies 40 gigabytes of on-chip memory in total, split between processor elements this amounts to less than 50 kilobytes each [@Lie2023].
Indeed, a key use case motivating the Downstream library has been in managing data for agent-based evolution experiments conducted on the WSE platform, a topic discussed further in "Projects Using This Software."

# Approach

Algorithms in Downstream consist of two components:
1. *site selection*, which controls ongoing runtime downsample curation, and
2. *site lookup*, which identifies stream arrival indices (i.e., timepoints) for stored data.

Downstream's runtime data management applies a minimalistic strategy.
First, a fixed-capacity working buffer is assumed, with user-defined size.
Second, stored data remains fixed in place without subsequent editing or relocation.
Operations on ingested items are therefore limited to storing, discarding (i.e., without storage), or overwriting previously stored data.
Hence, downsample curation is wholly determined by "site selection" --- i.e., the placement of each ingested data item.
This scheme, in essence, represents a generalized ring buffer, and --- as such --- provides compact, efficient processing and storage [@Gunther2014].

 \autoref{fig:schematic} illustrates Downstream's single-operation "site selection" approach.
At any point, but typically in a postprocessing step, a corresponding "site lookup" procedure can calculate stored items' arrival index, allowing this metadata to be omitted in storage.

In practice, typical nuts-and-bolts steps for end-user code are thus: (1) initialize a fixed-size buffer with desired capacity ($S$), (2) maintain a count $T$ of elapsed stream depth, and (3) use $T$ and $S$ to call the site selection method of a chosen Downstream algorithm to place each arriving stream item in the buffer (or discard it).
From this point forward, steps in using or analyzing stored data will vary by use case.
Among a variety of supported possibilities, one simple workflow would be to (1) dump memory segments comprising counter $T$ and stored buffer content as hexidecimal strings in a tabular data file (e.g., Parquet, CSV, etc.) then (2) using Downstream CLI, explode as long format (i.e., one row per data item) with corresponding data item lookups (i.e., stream arrival index).

![Schematic illustration of a Downstream site selection algorithm operating on a data stream with a fixed-capacity memory buffer ($S = 4$ sites). Each new item in the data stream (right) arrives over time ($T \in[0, 8]$), and is either stored in the memory buffer or discarded. Storage decisions are made independently at each timestep, with each item mapped to one of the $S$ memory sites ($k \in {0, 1, 2, 3}$). Previously stored items may be overwritten. This example illustrates curation of a steady-spaced downsample. Green box (top) depicts lookup operation to calculate stream indices of stored data at time $T=8$.
  \label{fig:schematic}
](assets/schematic_smaller.png)

# Features

Downstream provides algorithms for curating stream downsample density according to three primary temporal distributions: steady, stretched, and tilted.

The **steady algorithm** maintains uniform spacing between retained items.
This approach is best suited for applications in which it is important to maintain data from all time periods, such as for trend analysis in long-term monitoring systems.
In addition to an approach proposed in [@Moreno2024], Downstream includes Python implementation of the ``compressing ring buffer'' approach for steady curation developed by [@Gunther2014].

The **stretched algorithm** prioritizes older data while maintaining recent context, focusing on preserving the origins of the stream.
Specifically, the density of retained data is thinned proportionally to depth in the stream.
This approach suits applications where detailed understanding of initial conditions is critical.

The **tilted algorithm** prioritizes recent information over older data.
Specifically, the density of retained data is thinned proportionally to age.
This makes it well-suited for monitoring and alerting systems where recent trends are most relevant, but historical context still provides valuable perspective --- such as in real-time monitoring systems [@tabassum2018sampling], where recent data carries more operational significance than older data [@aggarwal2006biased].

| **Algorithm Name** | **Distribution of Retained Data**  | **Example Use Case**             |
| ------------------ | ---------------------------------- | -------------------------------- |
| Steady             | Evenly distributed                 | Long-term systems monitoring     |
| Tilted          | Favors recent data                 | Ancestry markers in evolutionary simulations             |
| Stretched             | Favors older data                  | Real-time alert monitoring       |

Table: Comparison of core Downstream algorithms.

To support diverse end-user integrations, Downstream has been implemented across five programming languages: C++, Rust, Python, Zig, and the Cerebras Software Language (CSL).
We have organized each implementation as a standalone branch within the library's git repository.

For all implementations, we provide:
1. Steady, stretched, and tilted site selection methods.
2. API documentation, to demonstrate function signatures and semantics.
3. Installation instructions, through standard package managers where supported (e.g., Python's PyPI, Cargo's Rust).
C++ code is provided as a header-only library.
4. Extensive validation tests, ensuring complete interchangeability and exact compatibility between platforms (e.g., separate data collection and analysis steps).

On an as-needed basis, implementations are provided for additional hybrid algorithms, which split buffer space between multiple temporal distributions.
Support for high-throughput bulk lookup operations is implemented in Python, with both CLI- and library-based interfaces available.
A Python-based CLI is also provided for validation testing, facilitating the development of additional implementations for new languages or platforms.

# Empirical Scaling Benchmark

![Execution time of Downstream site selection algorithms across varying runtime environments. (Left) Per-site real execution time across different surface sizes ($S \in \{64, 256, 1024\}$), representing the size of the buffer. (Right) Real execution time across different time ranges ($T \in [0, 2^{16})$ vs. $[0, 2^{32})$).
Bars show bootstrap 95% confidence intervals.
  \label{fig:benchmark}
](assets/benchmark_combined_new.png)

A key goal of Downstream is efficient scaling to large buffer sizes and deep stream durations.
To test the library's performance, we conducted empirical benchmarking trials of Python site selection methods.
Shown in \autoref{fig:benchmark}, we observed consistent execution time across both buffer size and stream depth (i.e., number of data points processed).
Statistical analysis detects no significant differences in execution time between conditions ($\alpha=0.05$; Kruskal-Wallis; $n=5$).

<!--
- [Buffer size benchmarks](https://github.com/mmore500/downstream-benchmark/blob/binder/binder/2025_04_13_assign_sites_batched_graphing_T_ranges.ipynb)
- [Surface size benchmarks](https://github.com/mmore500/downstream-benchmark/blob/binder/binder/2025_04_13_assign_sites_batched_graphing_S_ranges.ipynb)
-->

## Projects Using the Software

A motivating use case for the Downstream library is in supporting work on *hereditary stratigraphy*, a decentralized, approximate phylogeny tracking method for large-scale, parallel and distributed agent-based evolution simulations.
In this use case, phylogenetic history (i.e., a population's ancestry tree) is estimated from Downstream-curated data embedded in agent genomes.
This data comprises a running downsample of randomly-generated checkpoint values, generated and appended for each generation elapsed.
By comparing these checkpoint values, it is possible to estimate when the lineages of extant genomes diverged [@moreno2022hereditary].
Notably, this use case can make use of both steady and tilted distributions [@moreno2025testing], and depends on post-hoc stream index lookup to identify the generational timing of inferred phylogenetic events.

To this end, Downstream serves as a key dependency for the library implementing hereditary stratigraphy methodology, *hstrat* [@moreno2022hstrat].
In recent work with *hstrat*, the CSL Downstream implementation has been applied to support phylogeny tracking in massively distributed, agent-based evolution simulations conducted on the 850,000-processor WSE platform [@Moreno2024].
<!-- TODO: this approach has enabled phylogeny reconstructions scaling up to one billion tips -->
In other forthcoming work employing WSE-based simulations of hypermutator evolution, Downstream has also been used to collect time series data leading up to in-simulation extinction events.

In both examples, Downstream provides a mechanism for best-effort trade-offs between runtime efficiency and data quality, wherein a considered amount of precision (chosen based on experimental objectives) is exchanged for memory savings, dynamic flexibility, and --- ultimately --- increased scalability.
We anticipate this pattern continuing as a recurring theme in further applications of the library.

# Related Software

Several notable projects provide data stream processing functionality related to Downstream.

The most similar piece of software to Downstream is Gunther's work on compressing circular buffers [@Gunther2014].
This approach exploits modular arithmetic as the basis for a ring buffer generalization with steady-spaced coarsening behavior.
Included software, written in Java, notably supports additional aggregation algorithms (e.g., averaging, summing, extrema, etc.) in addition to sampling, as is the focus in Downstream.
Downstream extends beyond [@Gunther2014], however, in enabling support for stretched and tilted downsampling, as well as cross-language support and high-throughput lookup decoding.

Reservoir sampling approaches provide representative samples of data streams, but lack  deterministic temporal distribution guarantees and metadata-free stream arrival index attribution provided by Downstream [@aggarwal2006biased;@hentschel2018temporally].

Apache Flink and Spark Streaming are general-purpose distributed computing frameworks for stream processing, which focus on distributed computation over massive data streams rather than data downsampling [@carbone2015apache;@salloum2016big].

InfluxDB and TimescaleDB are time-series databases that offer storage solutions for continuous data in applications like IoT devices, but typically require open-ended storage capacity or downsampling strategies fundamentally different from Downstream's algorithms [@naqvi2017time;@stefancova2018evaluation].

# Future Work

As originally proposed [@Moreno2024], Downstream's stretched and tilted algorithms only support stream sizes up to $2^S-2$ items (where $S$ is the buffer size).
Preliminary work, included in recent releases of Downstream, is underway to explore extensions beyond this point.
Work is also underway on more comprehensive cross-platform benchmarks.

More generally, we plan to continue developing library features --- e.g., extending partially-supported functionality across language branches, supporting additional programming languages, etc. --- on an as-needed basis, and welcome user requests or contributions to this end.


# Acknowledgements

Thank you to Vivaan Singhvi for contributing supplemental material, including benchmarks and additional implementations, to the Downstream and hstrat libraries.
This research was supported by the University of Michigan through the Undergraduate Research Opportunities Program, by Michigan State University through computational resources provided by the Institute for Cyber-Enabled Research, and by the Eric and Wendy Schmidt AI in Science Postdoctoral Fellowship, a Schmidt Sciences program.

This material is based upon work supported by the U.S. Department of Energy, Office of Science, Office of Advanced Scientific Computing Research (ASCR), under Award Number DE-SC0025634.
This report was prepared as an account of work sponsored by an agency of the United States Government.
Neither the United States Government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof.
The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.


# References

<div id="refs"></div>

\pagebreak
\appendix
