from datetime import date, datetime
from typing import ClassVar

import pydantic


class DownloadsResumeRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT 
        sumIf(count, date > today() - toIntervalDay(1)) AS last_day,
        sumIf(count, date > today() - toIntervalWeek(1)) AS last_week,
        sumIf(count, date > today() - toIntervalMonth(1)) AS last_month,
        sumIf(count, date > today() - toIntervalYear(1)) AS last_year,
        sum(count) AS total
    FROM 
        pypi.pypi_downloads_per_day 
    WHERE 
        project = '{package_name}'
    """

    last_day: int
    last_week: int
    last_month: int
    last_year: int
    total: int


class PackagesResumeRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT
        name,
        count(DISTINCT version) as count_version,
        round(avg(size)) as avg_size,
        min(upload_time) as created_at,
        max(upload_time) as updated_at
    FROM
        pypi.projects
    WHERE
        name = '{package_name}'
    GROUP BY
        name
    """

    name: str
    avg_size: int
    count_version: int
    created_at: datetime
    updated_at: datetime


class ReleasesResumeRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT
    countIf(DISTINCT version, upload_time > today() - toIntervalDay(1)) AS last_day,
        countIf(DISTINCT version, upload_time > today() - toIntervalWeek(1)) AS last_week,
        countIf(DISTINCT version, upload_time > today() - toIntervalMonth(1)) AS last_month,
        countIf(DISTINCT version, upload_time > today() - toIntervalYear(1)) AS last_year,
        count(DISTINCT version) AS total
    FROM
        pypi.projects
    WHERE
        name = '{package_name}'
    """

    last_day: int
    last_week: int
    last_month: int
    last_year: int
    total: int


class DependencyForPackagesResumeRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT
        count(DISTINCT name) AS count_packages,
        count(DISTINCT version) AS count_releases
    FROM
        pypi.projects
    WHERE
        arrayExists(x -> x = '{package_name}', requires_dist)
    """

    count_packages: int
    count_releases: int


class ReleasesByMonthRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT
        version,
        max(upload_time) AS date
    FROM
        pypi.projects
    WHERE
        name = '{package_name}'
    GROUP BY
        version
    ORDER BY
        date DESC
    LIMIT {limit}
    """

    version: str
    date: datetime


class DownloadsByVersionRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT
        version,
        count
    FROM
        pypi.pypi_downloads_by_version
    WHERE
        project = '{package_name}'
    """

    version: str
    count: int


class DependencyForByRequiresRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT
        arrayFilter(x -> x LIKE '{package_name}%', requires_dist)[1] AS requires,
        count(DISTINCT (name, version)) AS count
    FROM
        pypi.projects
    WHERE
        arrayExists(x -> x LIKE '{package_name}%', requires_dist)
    GROUP BY 
        requires

    """

    requires: str
    count: int


class DownloadsByMonthRequest(pydantic.BaseModel):
    SQL: ClassVar[str] = """
    SELECT
        month,
        count
    FROM
        pypi.pypi_downloads_per_month
    WHERE
        project = '{package_name}'
    ORDER BY
        month DESC
    LIMIT 12
    """

    month: date
    count: int
