from pathlib import Path

from package_schemes.interfaces import Pyproject
from packaging import version
from packaging.specifiers import SpecifierSet
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from uv_stats.sources import ClickHouseSource


def clean_version_spec(spec: str):
    if ';' in spec:
        spec = spec.split(';')[0].strip()
    if '(' in spec and ')' in spec:
        spec = spec[spec.find('(') + 1 : spec.find(')')]
    else:
        spec = ''

    spec = spec.replace('"', '').replace("'", '')
    if '*.' in spec:
        spec = spec.replace('.*', '.0')
    elif spec.endswith('.*'):
        spec = spec[:-2]
    return spec


def count_compatible_dependencies(dependencies_data: dict[str, int], target_version: str):
    target_ver = version.parse(target_version)
    total = 0

    for dependency in dependencies_data:
        try:
            version_spec = clean_version_spec(dependency)

            if version_spec:
                specifier = SpecifierSet(version_spec)
                if target_ver in specifier:
                    total += dependencies_data[dependency]

            else:
                total += dependencies_data[dependency]

        except Exception as e:
            print(f"Ошибка при обработке зависимости '{dependency}': {e}")
            pass

    return total


class UvStatsManager(object):
    package_name: str

    def __init__(self, package_name: str) -> None:
        self.package_name = package_name
        self.console = Console(record=True)
        self.source = ClickHouseSource(self.package_name)

    @classmethod
    def get_current_package_name(cls) -> str | None:
        pyproject = Pyproject(Path.cwd() / 'pyproject.toml')
        return pyproject.data.project.name

    def make_header_panel(self):
        package_info = self.source.get_package_info()

        if package_info is None:
            return None

        releases_resume = self.source.get_releases_resume()
        downloads_resume = self.source.get_downloads_resume()
        depend_for_packages_resume = self.source.get_dependency_for_packages_resume()

        t0 = Table(
            'Week',
            'Month',
            'Year',
            'Total',
            title='Releases per',
            title_justify='center',
            box=box.MINIMAL,
        )
        t0.add_row(
            f'[bold bright_green]{releases_resume.last_week}[bold bright_green]',
            f'[bold bright_yellow]{releases_resume.last_month}[bold bright_yellow]',
            f'[bold bright_yellow]{releases_resume.last_year}[bold bright_yellow]',
            f'[bold bright_red]{releases_resume.total}[bold bright_red]',
        )

        t1 = Table(
            # 'name',
            'Released at',
            'Lats record',
            'Dependency for',
            # 'Avg Size',
            # title='Information',
            title_justify='center',
            box=box.MINIMAL,
        )
        t1.add_row(
            str(package_info.created_at.date()),
            str(package_info.updated_at.date()),
            f'{depend_for_packages_resume.count_packages}/{depend_for_packages_resume.count_releases}',
            # str(package_info.avg_size),
        )

        t2 = Table(
            'Week',
            'Month',
            'Year',
            'Total',
            title='Downloads per',
            title_justify='center',
            box=box.MINIMAL,
        )
        t2.add_row(
            f'[bold bright_green]{downloads_resume.last_week}[bold bright_green]',
            f'[bold bright_yellow]{downloads_resume.last_month}[bold bright_yellow]',
            f'[bold bright_yellow]{downloads_resume.last_year}[bold bright_yellow]',
            f'[bold bright_red]{downloads_resume.total}[bold bright_red]',
        )

        panel = Panel.fit(
            title=f'[bold bright_magenta]{package_info.name}[bold bright_magenta]',
            title_align='center',
            renderable=Columns(
                equal=True,
                expand=True,
                renderables=[
                    Align.left(t0),
                    Align.center(t1),
                    Align.right(t2),
                ],
            ),
        )
        return panel

    def make_releases_details(self):
        releases = self.source.get_releases()
        dependency_for = {i.requires: i.count for i in self.source.get_dependency_for_by_deps()}
        downloads_by_releases = {i.version: i.count for i in self.source.get_downloads_by_version()}

        table_releases = Table(
            'Version',
            'Date',
            'Downloads',
            'Dependency for',
            # title='Releases',
            title_justify='center',
            box=box.MINIMAL,
        )

        for release in releases:
            dependency_for_current_release = count_compatible_dependencies(dependency_for, release.version)

            table_releases.add_row(
                f'[bold bright_green]{release.version}[bold bright_green]',
                f'[bold bright_yellow]{release.date.strftime("%d-%m-%Y %H:%M")}[bold bright_yellow]',
                f'[bold bright_yellow]{downloads_by_releases.get(release.version, "")}[bold bright_yellow]',
                f'[bold bright_yellow]{dependency_for_current_release}[bold bright_yellow]',
            )

        panel = Panel.fit(
            title='[bold bright_magenta]Releases[bold bright_magenta]',
            title_align='center',
            renderable=table_releases,
        )
        return panel

    def make_month_details(self):
        downloads_by_mount = self.source.get_downloads_by_month()

        table_releases = Table(
            'Month',
            'Downloads',
            # title='Releases',
            title_justify='center',
            box=box.MINIMAL,
        )

        for download_and_mount in downloads_by_mount:
            table_releases.add_row(
                f'[bold bright_green]{download_and_mount.month}[bold bright_green]',
                f'[bold bright_yellow]{download_and_mount.count}[bold bright_yellow]',
            )

        panel = Panel.fit(
            title='[bold bright_magenta]Releases[bold bright_magenta]', title_align='center', renderable=table_releases
        )
        return panel

    def save_console(self):
        self.console.print()

    def save_sgv(self):
        self.console.save_svg('uv-stats.svg')

    def run(
        self,
        releases_details: bool = True,
        month_details: bool = True,
        to_svg: bool = True,
        to_console: bool = True,
    ):
        header_panel = self.make_header_panel()

        if header_panel is None:
            print(f'Package "{self.package_name}" was not found')
            return

        self.console.print()

        if any([releases_details, month_details]):
            renderables = []
            if releases_details:
                renderables.append(Align.left(self.make_releases_details()))

            if month_details:
                renderables.append(Align.right(self.make_month_details()))

            self.console.print(
                Columns(
                    equal=True,
                    expand=True,
                    renderables=renderables,
                ),
            )

        if to_svg or True:
            self.save_sgv()

        if to_console:
            self.save_console()
