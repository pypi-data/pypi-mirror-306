from importlib import metadata as _metadata

from uv_stats.cli import cli  # noqa: F401

try:
    __version__ = _metadata.version('uv-stats')

except _metadata.PackageNotFoundError:
    __version__ = '0.0.0'
