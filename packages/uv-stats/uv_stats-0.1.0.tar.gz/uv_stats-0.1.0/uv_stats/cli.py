import typer

import uv_stats
from uv_stats.manager import UvStatsManager

cli = typer.Typer(help='uv-stats CLI')


def version_callback(value: bool):
    if value:
        print(f'Version of uv-stats is {uv_stats.__version__}')
        raise typer.Exit(0)


@cli.callback(invoke_without_command=True)
def callback(  # noqa: C901
    ctx: typer.Context,
    #
    version: bool = typer.Option(
        False,
        '--version',
        callback=version_callback,
        help='Print version of uv-stats.',
        is_eager=True,
    ),
    #
    verbose: bool = typer.Option(
        False,
        '--verbose',
        '-v',
        help='Run with verbose',
    ),
    #
    to_console: bool = typer.Option(
        True,
        '--to-console',
        '-v',
        help='Print stats in console',
    ),
    to_svg: bool = typer.Option(
        False,
        '--to-svg',
        help='Save stats as svg "uv-stats.svg"',
    ),
    #
    package_name: str | None = typer.Argument(
        None,
        help='Target pypi package',
    ),
):
    if package_name is None:
        package_name = UvStatsManager.get_current_package_name()

    if package_name is None:
        raise ValueError('Could not find package name')

    uv_stats_manager = UvStatsManager(package_name)
    uv_stats_manager.run(to_svg=to_svg, to_console=to_console)


@cli.command('nothing', hidden=True)
def nothing_command():
    """Plug."""
    pass
