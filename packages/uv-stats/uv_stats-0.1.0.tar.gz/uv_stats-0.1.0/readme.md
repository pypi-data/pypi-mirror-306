# uv Audit Tool

Make pritty statistic about package in concole

[![PyPI](https://img.shields.io/pypi/v/uv-stats)](https://pypi.org/project/uv-stats/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uv-stats)](https://pypi.org/project/uv-stats/)
[![uvxt](https://img.shields.io/badge/family-uvxt-purple)](https://pypi.org/project/uvxt/)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rocshers_uv-stats&metric=coverage)](https://sonarcloud.io/summary/new_code?id=rocshers_uv-stats)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rocshers_uv-stats&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=rocshers_uv-stats)

[![Downloads](https://static.pepy.tech/badge/uv-stats)](https://pepy.tech/project/uv-stats)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/uv-stats)](https://gitlab.com/rocshers/python/uv-stats)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/uv-stats)](https://gitlab.com/rocshers/python/uv-stats)

Powered by [clickpy](https://clickpy.clickhouse.com)

## Quick start

```bash
uvx uv-stats fastapi

# Or using uvxt
uv tool install uvxt
uvxt stats fastapi
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/uv-stats/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/uv-stats>

Before adding changes:

```bash
make install
```

After changes:

```bash
make format test
```
