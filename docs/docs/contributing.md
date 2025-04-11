# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

### Language Implementations

Library code for each supported programming language is implemented on a dedicated branch (e.g., Python on the `python` branch, C++ on the `cpp` branch).
Implementations generally follow the following structure:

- Core algorithm variants under `dstream/` directory including:
      - `steady_algo`
      - `stretched_algo`
      - `tilted_algo`
      - Optional hybrid variants (e.g., `hybrid_0_steady_1_stretched_2_algo`)


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

<!-- ## Get Started!

Ready to contribute? Here's how to set up `dstream` for local development.

1. Fork the `dstream` repo on GitHub.
2. Clone your fork locally:
   ```shell
   $ git clone git@github.com:your_name_here/downstream.git
   $ cd downstream
   ```
3. Install development requirements into a virtualenv (where `X` is your local major release of Python):
   ```shell
   $ python3.X -m venv env
   $ source env/bin/activate
   $ python3.X -m pip install -r requirements-dev/py3X/requirements-all.txt
   ```
4. Alternately, to install development requirements into your local Python environment:
   ```shell
   $ python3.X -m pip install -r requirements-dev/requirements-all.txt
   ```
5. Create a branch for local development:
   ```shell
   $ git checkout -b name-of-your-bugfix-or-feature
   ```
   Now you can make your changes locally.
6. When you're done making changes, check that your changes pass the tests:
   ```shell
   $ python3.X -m pytest
   ```
   To run some tests, you will need ffmpeg installed.
   The Linux way to do this is:
   ```shell
   $ sudo apt-get update
   $ sudo apt-get install ffmpeg
   ```
7. Commit your changes and push your branch to GitHub:
   ```shell
   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature
   ```
8. Submit a pull request through the GitHub website. -->

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.rst.
3. The pull request should work for Python 3.6, 3.7 and 3.8, and for PyPy. Check https://travis-ci.com/mmore500/downstream/pull_requests and make sure that the tests pass for all supported Python versions.

<!-- ## Tips

To run a subset of tests:
```shell
$ pytest tests.test_hstrat
``` -->

## Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run:
```shell
$ bumpver patch # possible: major / minor / patch
# $ git push
# $ git push --tags
```

GitHub Actions will then deploy to PyPI if tests pass.