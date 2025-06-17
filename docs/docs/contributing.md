# Contributing

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

You can contribute in many ways:

### Language Implementations

Library code for each supported programming language is implemented on a dedicated branch (e.g., Python on the `python` branch, C++ on the `cpp` branch).
Implementations generally follow the following structure:

- Core algorithm variants under `dstream/` directory including:
      - `steady_algo`
      - `stretched_algo`
      - `tilted_algo`
      - as needed for particular use cases, secondary algorithms and hybrid variants (e.g., `hybrid_0_steady_1_stretched_2_algo`)


Internal support code is organized into an accompanying `_auxlib` module.

Additional implementations and outside contributions are welcome!
If you create an implementation in another language, we're happy to either link to your repository or host it directly in ours on a dedicated branch.
New implementations should follow the existing conventions and structure, as far as possible.
Also consider implementing the project's established CLI interface for testing/debugging, which will enable out-of-the-box compatibility with our testing framework --- see the cpp or zig CI workflow for examples of how tests are run across implementations.

If you'd like to request support for an additional programming language, please open an issue!

Contributions to the repository are governed by our Code of Conduct, based on the [Contributor Covenant, version 2.0](https://www.contributor-covenant.org/version/2/0/code_of_conduct.html).

### Report Bugs

Report bugs at [https://github.com/mmore500/downstream/issues](https://github.com/mmore500/downstream/issues).

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

downstream could always use more documentation, whether as part of the official dstream docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at [https://github.com/mmore500/downstream/issues](https://github.com/mmore500/downstream/issues).

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Deploying

Version bumping and deployment is triggered through the `release` GitHub action, which is dispatched manually by maintainers via the GitHub Actions web interface.
