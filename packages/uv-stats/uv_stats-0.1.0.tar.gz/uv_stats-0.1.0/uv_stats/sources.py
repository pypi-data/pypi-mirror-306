import clickhouse_connect

from uv_stats.requests import *


class ClickHouseSource(object):
    package_name: str

    def __init__(self, package_name: str) -> None:
        self.package_name = package_name
        self.client = clickhouse_connect.get_client(
            host='clickpy-clickhouse.clickhouse.com',
            secure=True,
            username='play',
            password='',
        )

    def get_package_info(self) -> PackagesResumeRequest | None:
        res = self.client.query(PackagesResumeRequest.SQL.format(package_name=self.package_name))

        if not res.row_count:
            return

        return [PackagesResumeRequest.model_validate(i) for i in res.named_results()][0]

    def get_downloads_resume(self) -> DownloadsResumeRequest | None:
        res = self.client.query(DownloadsResumeRequest.SQL.format(package_name=self.package_name))

        if not res.row_count:
            return

        return [DownloadsResumeRequest.model_validate(i) for i in res.named_results()][0]

    def get_releases_resume(self) -> ReleasesResumeRequest | None:
        res = self.client.query(ReleasesResumeRequest.SQL.format(package_name=self.package_name))
        if not res.row_count:
            return

        return [ReleasesResumeRequest.model_validate(i) for i in res.named_results()][0]

    def get_dependency_for_packages_resume(self) -> DependencyForPackagesResumeRequest | None:
        res = self.client.query(DependencyForPackagesResumeRequest.SQL.format(package_name=self.package_name))

        if not res.row_count:
            return

        return [DependencyForPackagesResumeRequest.model_validate(i) for i in res.named_results()][0]

    def get_releases(self, limit: int = 10) -> list[ReleasesByMonthRequest]:
        res = self.client.query(ReleasesByMonthRequest.SQL.format(package_name=self.package_name, limit=limit))
        return [ReleasesByMonthRequest.model_validate(i) for i in res.named_results()]

    def get_downloads_by_version(self) -> list[DownloadsByVersionRequest]:
        res = self.client.query(DownloadsByVersionRequest.SQL.format(package_name=self.package_name))
        return [DownloadsByVersionRequest.model_validate(i) for i in res.named_results()]

    def get_dependency_for_by_deps(self) -> list[DependencyForByRequiresRequest]:
        res = self.client.query(DependencyForByRequiresRequest.SQL.format(package_name=self.package_name))
        return [DependencyForByRequiresRequest.model_validate(i) for i in res.named_results()]

    def get_downloads_by_month(self) -> list[DownloadsByMonthRequest]:
        res = self.client.query(DownloadsByMonthRequest.SQL.format(package_name=self.package_name))
        return [DownloadsByMonthRequest.model_validate(i) for i in res.named_results()]
