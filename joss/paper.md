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

Downstream offers efficient algorithms for the curation of continuous data streams, implemented across multiple programming languages including C++, Rust, Python, Zig, and the Cerebras Software Language.
We define a data stream as a strictly-ordered sequence of read-once inputs.
In real-world applications, data streams often require real-time operations on a continuous, indefinite basis [@Cordeiro2016].
This often exceeds available memory capacities, requiring memory-efficient alternatives to storing entire streams directly.
While traditional approaches like circular ring buffers address this limitation by retaining only the most recent data points, Downstream maintains representative, approximate records of stream history through three algorithms proposed in [@moreno2024algorithms]: (1) "steady," which creates evenly spaced snapshots across the entire history; (2) "stretched," which preserves important older data points; and (3) "tilted," which prioritizes recent information.
The library features extensive cross-implementation testing, automated documentation and deployment, and is available through standard package managers.

# Statement of Need

Efficient data stream processing is a foundational challenge in modern computing systems, where the ability to analyze continuous, high-volume data has become more prevalent [@Cordeiro2016].
Applications of data stream processing include [@moreno2024structured] sensor networks [@Eiman2003], distributed big-data processing [@he2010comet], real-time network traffic analysis [@Johnson2005;@Muthukrishnan2005], systems log management [@Fischer2012], fraud monitoring [@RajeshwariU2016], trading in financial markets [@Agarwal2009], environmental monitoring [@Hill2009], and astronomy [@Graham2012], which all generate data at rates that exceed practical storage capacity while requiring analysis across varying time horizons.

Downstream addresses limitations of traditional approaches to data streaming by providing algorithms that compress stream history into fixed memory capacities while preserving meaningful data points according to specific temporal importance criteria.

By exclusively operating with primitive operations and eliminating memory overhead, the framework enables efficient operations in severely resource-constrained environments including embedded systems, where available memory is often measured in kilobytes.
For instance, hardware accelerators like the Cerebras WSE-2 demonstrate this constraint clearly—despite having 40 gigabytes of total on-chip memory, each individual core has access to under 50 kilobytes of memory [@Lie2023].

The capability for efficient stream compression is particularly valuable for applications such as hereditary stratigraphy [@Moreno2024] in large-scale phylogenetic tracking, where memory-efficient evolutionary history tracking must be maintained across distributed computing environments.
Downstream algorithms are currently being used to support such phylogenetic tracking in distributed digital evolution simulations.

The framework's distinct approach of requiring only single-operation "site selection" with no metadata storage provides significant improvements in space efficiency compared to previous methods.
This makes Downstream especially valuable for applications where individual data items may be as small as single bits or bytes—scenarios, where conventional approaches would consume more memory for metadata than for the data itself.


# Methods

To simplify the process of stream curation, this approach makes some assumptions: first, the output buffer is of a fixed length; second, stored data remains static without subsequent editing or relocation.
Operations on ingested items are therefore limited to discarding without storage, storing, or overwriting previously stored data.
This reduces the problem of stream curation to one of site selection—determining the placement of each subsequent data item.

In a typical use case, an application would integrate Downstream by: (1) initializing a fixed-size buffer with the desired capacity, (2) passing each new data point through the selected algorithm's site selection function to determine whether and where to store it, and (3) later accessing the preserved history through standard lookup operations.
For instance, in the hereditary stratigraphy example, the buffer represents the genetic information of a specific genome, with each selected site representing a mutation within a particular generation.
In [@Moreno2024], multiple such genomes are instantiated, and undergo many such generations to simulate evolution.
Lookup procedures can then be used for post-hoc analysis by reconstructing a phylogenetic tree from the resulting data.

To support diverse use cases, the three Downstream algorithms address different temporal distributions.

The **steady algorithm** creates evenly distributed snapshots across stream history by preserving data points with the most historical significance while maintaining relatively uniform spacing between retained items.
This approach is best suited for applications in which it is important to maintain data from all time periods, such as long-term monitoring systems that need to detect patterns across their entire operational history [@microsoft_monitoring] and trend analysis across extended timeframes [@techtarget_monitoring].

The **stretched algorithm** prioritizes older data while maintaining recent context, focusing on preserving the origins of the stream.
This approach particularly benefits applications where understanding initial conditions is critical for providing context for current behaviors, such as system diagnostics, evolutionary patterns [@moreno2024algorithms], and environmental monitoring systems [@researchgate_monitoring].

The **tilted algorithm** prioritizes recent information over older data.
This makes it well-suited for monitoring and alerting systems where recent trends are most relevant, but historical context still provides valuable perspective such as in real-time monitoring systems [@tabassum2018sampling] where recent data carries more operational significance than older data [@aggarwal2006biased].

| Algorithm Name | Distribution of Retained Data  | Example Use Case             |
| -------------- | ------------------------------ | ---------------------------- |
| Steady         | Evenly distributed             | Long-term systems monitoring |
| Stretched      | Biases recent data             | Evolutionary history         |
| Steady         | Biases older data              | Real-time alert monitoring   |

![Comparison of the three Downstream algorithms
  \label{table:algos}
]

# Implementation

Downstream has been implemented across five programming languages in order to support diverse computing environments, including C++, Rust, Python, Zig, and the Cerebras Software Language.
This multi-language approach enables integration with various systems from embedded devices to high-performance computing environments, supporting both research prototypes and production deployments.
Each of the implementations reside in a separate branch of the Downstream GitHub repository and contains site selection implementation for the three main Downstream algorithms.
In addition, some branches include hybrid variants that combine multiple temporal distributions.
Support for dataframe processing is available in Pyhton
To enhance usability and reliability, the framework incorporates features across all implementations:
1. Each algorithm is run against cross-validation tests with other language versions to ensure consistent behavior.
2. Documentation is available for all languages, with function headings listed for at least one of the algorithms.
All other algorithms should share the same heading.
3. The library is available through standard package managers for each supported language, including pip for Python and Cargo for Rust.
It is also available for C++ as a header-only library.
4. Users can specify precise memory constraints, allowing the framework to adapt to varying resource environments without compromising functionality.


# Results and Performance

![Comparison of mean real execution time across varying buffer sizes and number of ingested elements.
  \label{fig:benchmark}
](assets/benchmark_combined.png)

Preliminary testing has shown that for all Downstream algorithms, execution time for site selection operations remain constant regardless of buffer size or the number of data points processed.
Due to Downstream’s zero overhead approach, it maintains efficient stream curation regardless of the environment.
The performance results are illustrated in \autoref{fig:benchmark}.


# Projects Using the Software

[@Moreno2024] has incorporated Downstream algorithms for maintaining historical records in distributed digital evolution simulations, tracking phylogenetic information across massively distributed, agent-based experiments conducted on the 850,000 core Cerebras Wafer-Scale Engine.

# Related Software

Several existing frameworks address aspects of data stream processing with approaches distinct from Downstream.

Algorithm 938 [@Gunther2014] from the ACM Transactions on Mathematical Software collection uses circular buffer-related methodology for data sequence compression but implements different mechanisms for data point selection and historical representation.
Downstream includes an implementation of this algorithm for comparison, while extending beyond the original Java implementation to support various programming languages and focuses on broader summarization operations beyond just stream curation.

Apache Flink and Spark Streaming are general-purpose distributed computing frameworks for stream processing, but focus much more on scalability and distributed computation over massive data streams rather than historical data retention within fixed memory constraints [@carbone2015apache;@salloum2016big].

InfluxDB and TimescaleDB are time-series databases that offer storage solutions for continuous data for applications like IoT devices, but typically require expanding storage capacity or implement downsampling strategies fundamentally different from Downstream's algorithms [@naqvi2017time;@stefancova2018evaluation].

The reservoir sampling algorithm maintains representative samples of data streams but lacks the temporal distribution guarantees provided by Downstream's specialized algorithms [@aggarwal2006biased;@hentschel2018temporally].

# Future Work

To validate these algorithms, further benchmarks can be conducted to compare memory efficiency and throughput across all five language implementations.
These benchmarks can measure performance under various real-world constraints, simulating in embedded systems and high-throughput applications.

To further improve accessibility, we plan to continue implementing Downstream in more languages, including Julia, as well as any other implementations requested by users.
<!-- Additionally, we aim to enhance support for dataframe processing to simplify integration with data analysis workflows. -->
Each new implementation will follow the existing structure mentioned previously.

For stretched and tilted algorithms, which currently support up to 2^S-2 ingestions (where S is the buffer size), future work will address behavior beyond this threshold by potentially switching curation behavior at values 2^S-1 and onwards.

# Acknowledgements


Thank you to Vivaan Singhvi and Joey Wagner for providing supplemental material including benchmarks and additional implementations to the Downstream and hstrat libraries.
This material is based upon work supported by the U.S. Department of Energy, Office of Science, Office of Advanced Scientific Computing Research (ASCR), under Award Number DE-SC0025634.
This report was prepared as an account of work sponsored by an agency of the United States Government.
Neither the United States Government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof.
The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.
This material is also based upon work supported by the Eric and Wendy Schmidt AI in Science Postdoctoral Fellowship, a Schmidt Sciences program.
Computational resources were provided in part by the Michigan State University Institute for Cyber-Enabled Research (ICER).


# References

<div id="refs"></div>

\pagebreak
\appendix