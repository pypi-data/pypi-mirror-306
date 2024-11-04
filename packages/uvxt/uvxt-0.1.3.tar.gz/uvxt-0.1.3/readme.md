# uvxt - uv tools collection

A collection of tools that, in conjunction with the capabilities of the uv, will increase your productivity

[![PyPI](https://img.shields.io/pypi/v/uvxt)](https://pypi.org/project/uvxt/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uvxt)](https://pypi.org/project/uvxt/)
[![uvxt](https://img.shields.io/badge/family-uvxt-purple)](https://pypi.org/project/uvxt/)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rocshers_uvxt&metric=coverage)](https://sonarcloud.io/summary/new_code?id=rocshers_uvxt)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rocshers_uvxt&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=rocshers_uvxt)

[![Downloads](https://static.pepy.tech/badge/uvxt)](https://pepy.tech/project/uvxt)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/uvxt)](https://gitlab.com/rocshers/python/uvxt)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/uvxt)](https://gitlab.com/rocshers/python/uvxt)

## Quick start

```bash
uv tool install uvxt
uvxt audit
```

or

```bash
uvx uvxt audit
```

## Commands

- `uvxt up` - Launch the [uv-up](https://pypi.org/project/uv-up/)
- `uvxt audit` - Launch the [uv-audit](https://pypi.org/project/uv-audit/)
- `uvxt stats` - Launch the [uv-stats](https://pypi.org/project/uv-stats/)
- `uvxt version` - Launch the [uv-version](https://pypi.org/project/uv-version/)

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/uvxt/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/uvxt>

### How to add a new tool?

1) Create your CLI application.
   - We strongly recommend using `typer` for easy integration into uvxt.
   - Make sure that your package dependencies do not conflict with those already described in uvxt.
2) Upload your module to PyPI.
3) Add this package as a dependency to uvxt via `uv add`.
4) Import your CLI application in [uvxt/cli.py](./uvxt/cli.py)
5) Check that everything works fine.
6) Make a PR.

### Development Commands

Before adding changes:

```bash
make install
```

After changes:

```bash
make format test
```
