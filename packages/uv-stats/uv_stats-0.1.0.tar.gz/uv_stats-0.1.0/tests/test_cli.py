import logging
from pprint import pp

import pytest
from typer.testing import CliRunner

from uv_stats import cli


class TestCli(object):
    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test_root(self, runner: CliRunner):
        result = runner.invoke(cli)
        if result.exit_code != 0:
            logging.exception(result.exception, exc_info=result.exc_info)
        assert result.exit_code == 0

    def test_nothing(self, runner: CliRunner):
        result = runner.invoke(cli, ['nothing'])
        assert result.exit_code == 0

    def test_version(self, runner: CliRunner):
        result = runner.invoke(cli, ['--version'])
        pp(result.output)
        assert result.exit_code == 0
