# `uv-demo` PyPI package

[![PyPI - Version](https://img.shields.io/pypi/v/uv-demo)](https://pypi.org/project/uv-demo/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uv-demo)](https://pypi.org/project/uv-demo/)
[![Pepy Total Downloads](https://img.shields.io/pepy/dt/uv-demo)](https://pypi.org/project/uv-demo/)
[![Code Quality Check](https://github.com/lucaspar/uv-demo/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/lucaspar/uv-demo/actions/workflows/code-quality.yaml)

A demo and template for a modern Python package managed by `uv`. Very useless as a package.

Use this as a template for new projects, or as a reference for how to set up a Python project with the following:

+ [x] `uv` as the Python package manager.
+ [x] [`tox`](./tox.ini) for testing the three latest Python versions.
+ [x] [`pre-commit` hooks](./.pre-commit-config.yaml) for code formatting and linting.
+ [x] [GitHub Actions](./.github/workflows/) for testing and publishing.
+ [x] `gh-act` for running GitHub Actions locally.
+ [x] [Makefile](./makefile) with common targets.
+ [x] Documentation with `pdoc` + GitHub Pages.
+ [x] Deptry to highlight missing and unused dependencies.

## System Dependencies

+ `uv`
    + `curl -LsSf https://astral.sh/uv/install.sh | sh`
+ `make`
    + `sudo apt install make`
    + `sudo pacman -S make`
+ For running GitHub Actions locally
    + [Docker](https://docs.docker.com/desktop/install/linux/)
    + `gh` (GitHub CLI)
        + `sudo pacman -S github-cli`
        + [Others](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
    + [`gh-act`](https://github.com/nektos/gh-act)
        + `gh extension install nektos/gh-act`

## Quick start

This will install all dependencies (`uv sync`) and run the entrypoint script:

```bash
uv run uv-demo
```

## Make targets

```bash
make
# equivalent to make install test

make install
# runs uv sync

make test
# runs tests for supported python versions

make serve-coverage
# serves coverage report on localhost:8000

make gact
# runs GitHub Actions locally with gh-act
#
# >>> WARNING: if the secrets file has a valid API key,
#   this target will actually publish the package to PyPI.
#
# Install with:     gh extension install nektos/gh-act
# or see            https://github.com/nektos/act

make clean
# removes all venv, tox, cache, and generated files

make update
# updates uv and pre-commit hooks

make publish
# publishes the package to PyPI
#
# >>> WARNING: if the secrets file has a valid API key,
#   this target will actually publish the package to PyPI.
```

## Integration with GitHub Actions

See the [Upload Python Package workflow file](.github/workflows/python-publish.yaml) for this package.

### Running actions locally

You can use `act` to run GitHub Actions locally. Use cases:

1. While writing a workflow, to test the workflow locally before pushing to the repository.
2. Run the publishing workflow without setting secrets on GitHub.
3. Before opening a pull request, to check the workflow will pass.

Copy the example secrets file and edit it with the required secrets:

```bash
cp config/secrets.env.example config/secrets.env
```

Then run `make gact` to run the GitHub Actions workflow locally.
