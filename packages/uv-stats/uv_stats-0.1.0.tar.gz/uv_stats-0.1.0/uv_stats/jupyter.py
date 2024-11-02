from uv_stats.manager import UvStatsManager


def print(package_name: str):
    manager = UvStatsManager(package_name)
    manager.run(to_console=True)
