---
title: 'Downstream: efficient, constant-space cross-platform implementations of algorithms for stream curation.'
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

Real-world data streams often require real-time operations on a continuous, indefinite basis [@Cordeiro2016].
This often exceeds available memory capacities, requiring memory-efficient alternatives to storing entire streams directly.
While traditional approaches like circular ring buffers address this limitation by retaining only the most recent data points, Downstream offers three fixed-capacity sampling algorithms, proposed in [@moreno2024algorithms], that maintain representative, approximate records of stream history: (1) "steady," which creates evenly spaced snapshots across the entire history; (2) "stretched," which preserves important older data points; and (3) "tilted," which prioritizes recent information.
To ensure seamless integration into diverse computing environments, Downstream offers implementations in multiple programming languages including C++, Rust, Python, Zig, and the Cerebras Software Language.
The library features extensive cross-implementation testing, automated documentation and deployment, and is available through standard package managers.

# Statement of Need

Efficient data stream processing is crucial modern computing systems, where workloads of continuous, high-volume data has become more prevalent [@Cordeiro2016].
Applications of data stream processing include sensor networks [@Eiman2003], distributed big-data processing [@he2010comet], real-time network traffic analysis [@Johnson2005;@Muthukrishnan2005], systems log management [@Fischer2012], fraud monitoring [@RajeshwariU2016], trading in financial markets [@Agarwal2009], environmental monitoring [@Hill2009], and astronomy [@Graham2012], which all generate data at rates that exceed practical storage capacity while requiring analysis across varying time horizons.

Downstream complements existing tools for data stream analysis by providing algorithms that compress stream history into fixed memory capacities while retaining representative data points following a specified temporal distribution.

By exclusively operating with primitive operations and eliminating memory overhead, the framework targets use cases in severely resource-constrained environments including embedded systems, where available memory is often measured in kilobytes.
This makes it especially valuable for applications where individual data items may be as small as single bits or bytes—scenarios, where conventional approaches would consume more memory for metadata than for the data itself.
Large-scale hardware accelerators like the Cerebras WSE-2 share similar resource constraints-despite having 40 gigabytes of total on-chip memory, it must be divided between hundreds of thousands of cores, resulting in each individual core having access to under 50 kilobytes of memory [@Lie2023].
Downstream implementations of efficient stream compression is particularly valuable for applications such as hereditary stratigraphy [@moreno2022hstrat] in large-scale evolutionary simulations, where memory-efficient evolutionary history tracking must be maintained across distributed computing environments.
These methods are being used to collect time series data in a best effort fashion—that is, they prioritize storing representative and strategically selected items from the stream under fixed-capacity memory, but cannot guarantee retention of all significant points.
<!-- This method has been used to collect / is being explored to collect time series data in a best effort fashion -->
<!-- Downstream algorithms are currently being used to support such phylogenetic tracking in distributed digital evolution simulations [@] -->


# Approach

To simplify the process of stream curation, this approach makes some assumptions: first, the output buffer is of a fixed length; second, stored data remains static without subsequent editing or relocation.
Operations on ingested items are therefore limited to discarding without storage, storing, or overwriting previously stored data.
This reduces the problem of stream curation to one of site selection—determining the placement of each subsequent data item.

In a typical use case, an application would integrate Downstream by: (1) initializing a fixed-size buffer with the desired capacity, (2) passing each new data point through the selected algorithm's site selection function to determine whether and where to store it, and (3) later accessing the preserved history through standard lookup operations.
For instance, in the hereditary stratigraphy example, the buffer represents the genetic information of a specific genome, with each selected site representing a mutation within a particular generation.
In [@Moreno2024], multiple such genomes are instantiated, and undergo many such generations to simulate evolution.
Lookup procedures can then be used for post-hoc analysis to reconstruct a phylogenetic tree from the resulting data.

![Schematic illustration of a Downstream site selection algorithm operating on a data stream with a fixed-capacity memory buffer ($S = 4$ sites). Each new item in the data stream (right) arrives over time ($T \in[0, 8]$), and is either stored in the memory buffer or discarded. Storage decisions are made independently at each timestep, with each item mapped to one of the $S$ memory sites ($k \in {0, 1, 2, 3}$). Previously stored items may be overwritten. This example illustrates which stream items are retained and which are discarded based on their mapped site and time ingested.
  \label{fig:schematic}
](assets/schematic_smaller.png)

To support diverse use cases, the three Downstream algorithms address different temporal distributions.

The **steady algorithm** creates evenly distributed snapshots across stream history by preserving data points with the most historical significance while maintaining relatively uniform spacing between retained items.
This approach is best suited for applications in which it is important to maintain data from all time periods, such as long-term monitoring systems that need to detect patterns across their entire operational history and trend analysis across extended timeframes.

The **stretched algorithm** prioritizes older data while maintaining recent context, focusing on preserving the origins of the stream.
This approach particularly benefits applications where understanding initial conditions is critical for providing context for current behaviors, such as system diagnostics, evolutionary patterns [@moreno2024algorithms], and environmental monitoring systems.

The **tilted algorithm** prioritizes recent information over older data.
This makes it well-suited for monitoring and alerting systems where recent trends are most relevant, but historical context still provides valuable perspective such as in real-time monitoring systems [@tabassum2018sampling] where recent data carries more operational significance than older data [@aggarwal2006biased].

| **Algorithm Name** | **Distribution of Retained Data**  | **Example Use Case**             |
| ------------------ | ---------------------------------- | -------------------------------- |
| Steady             | Evenly distributed                 | Long-term systems monitoring     |
| Tilted          | Biases recent data                 | Ancestry markers in evolutionary simulations             |
| Stretched             | Biases older data                  | Real-time alert monitoring       |

Table: Comparison of the three core Downstream algorithms.

The framework's distinct approach of requiring only single-operation "site selection" illustrated in \autoref{fig:schematic} allows it to store zero metadata, providing significant improvements in space efficiency compared to previous methods.

# Implementation

Downstream has been implemented across five programming languages in order to support diverse computing environments, including C++, Rust, Python, Zig, and the Cerebras Software Language.
This multi-language approach enables integration with various systems from embedded devices to high-performance computing environments, supporting both research prototypes and production deployments.
Each of the implementations reside in a separate branch of the Downstream GitHub repository and contains site selection implementation for the three main Downstream algorithms.
In addition, some branches include hybrid variants that combine multiple temporal distributions.
Support for dataframe processing is available in Python
To enhance usability and reliability, the framework incorporates features across all implementations:

1. Each algorithm is run against cross-validation tests with the Python implementation to ensure consistent behavior. Consistent behavior is important so that data can be collected using one language implementation and analyzed in another language.

2. Documentation is available for all languages, with function headings listed for at least one of the algorithms.
All other algorithms should share the same heading.

3. The library is available through standard package managers for each supported language, including pip for Python and Cargo for Rust.
It is also available for C++ as a header-only library.

4. Users can specify precise memory constraints, allowing the framework to adapt to varying resource environments without compromising functionality.


# Results and Performance

![Execution time performance of Downstream site selection algorithms across varying runtime environments. (Left) Per-site real execution time across different surface sizes ($S \in {64, 256, 1024}$), representing the size of the buffer. (Right) Real execution time across different time range capacities ($T \in [0, 2^{16})$ and $[0, 2^{32})$), representing the number of ingested timesteps. Results show consistent performance across scales, with all three algorithms exhibiting stable execution costs. Bars show the 95% confidence intervals for each test
  \label{fig:benchmark}
](assets/benchmark_combined_new.png)

Preliminary benchmarking has shown that all Downstream algorithms exhibit consistent execution times for site seleciton operations, regardless of buffer size or surface size (i.e. the number of data points processed), as illustrated in \autoref{fig:benchmark}.

Statistical analyses were conducted to confirm that the observed differences in execution time are not statistically significant ($\alpha=0.05$; Krukall-Wallis; $n=5$). These analyses are available in the following notebooks:

- [Buffer size benchmarks](https://github.com/mmore500/downstream-benchmark/blob/binder/binder/2025_04_13_assign_sites_batched_graphing_T_ranges.ipynb)

- [Surface size benchmarks](https://github.com/mmore500/downstream-benchmark/blob/binder/binder/2025_04_13_assign_sites_batched_graphing_S_ranges.ipynb)

# Projects Using the Software

Moreno et al. [@Moreno2024] has incorporated Downstream algorithms for maintaining historical records in distributed digital evolution simulations, tracking phylogenetic information across massively distributed, agent-based experiments conducted on the 850,000 core Cerebras Wafer-Scale Engine.

# Related Software

Several existing frameworks address aspects of data stream processing with approaches distinct from Downstream.

The most similar piece of software to Downstream is Algorithm 938 [@Gunther2014] from the ACM Transactions on Mathematical Software collection which uses circular buffer-related methodology for data sequence compression, but implements different mechanisms for data point selection and historical representation.
Gunther's software also supports additional aggregation algorithms like averaging, as opposed to just sampling in Downstream.
Downstream includes a Python implementation of this algorithm for comparison, while extending beyond the original Java implementation to support various programming languages and focusing on broader summarization operations like the stretched and tilted strategies.

Apache Flink and Spark Streaming are general-purpose distributed computing frameworks for stream processing, but focus much more on scalability and distributed computation over massive data streams rather than historical data retention within fixed memory constraints [@carbone2015apache;@salloum2016big].

InfluxDB and TimescaleDB are time-series databases that offer storage solutions for continuous data for applications like IoT devices, but typically require expanding storage capacity or downsampling strategies fundamentally different from Downstream's algorithms [@naqvi2017time;@stefancova2018evaluation].

The reservoir sampling algorithm maintains representative samples of data streams but lacks the temporal distribution guarantees provided by Downstream's specialized algorithms [@aggarwal2006biased;@hentschel2018temporally].

# Future Work

To validate these algorithms, further benchmarks can be conducted to compare memory efficiency and throughput across all five language implementations.
These benchmarks can measure performance under various real-world constraints, simulating in embedded systems and high-throughput applications.

To further improve accessibility, we plan to continue implementing Downstream in more languages, including Julia, as well as any other implementations requested by users.
<!-- Additionally, we aim to enhance support for dataframe processing to simplify integration with data analysis workflows. -->
Each new implementation will follow the existing structure mentioned previously.

For stretched and tilted algorithms, which currently support up to $2^S-2$ ingestions (where $S$ is the buffer size), preliminary work addresses behavior beyond this threshold by switching curation behavior at values $2^S-1$ and onwards.

# Acknowledgements


Thank you to Vivaan Singhvi and Joey Wagner for providing supplemental material including benchmarks and additional implementations to the Downstream and hstrat libraries.
This research was supported by University of Michigan through the Undergraduate Research Opportunities Program, by Michigan State University through computational resources provided by the Institute for Cyber-Enabled Research, and by the Eric and Wendy Schmidt AI in Science Postdoctoral Fellowship, a Schmidt Sciences program.
This material is based upon work supported by the U.S. Department of Energy, Office of Science, Office of Advanced Scientific Computing Research (ASCR), under Award Number DE-SC0025634.
This report was prepared as an account of work sponsored by an agency of the United States Government.
Neither the United States Government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof.
The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.


# References

<div id="refs"></div>

\pagebreak
\appendix
