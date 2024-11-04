from pprint import pp

import pytest
from typer.testing import CliRunner

from uvxt import cli


class TestCli(object):
    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test_root(self, runner: CliRunner):
        result = runner.invoke(cli)

        if result.exit_code != 0:
            pp(result.output)

        assert result.exit_code == 0

    def test_version(self, runner: CliRunner):
        result = runner.invoke(cli, ['--version'])

        if result.exit_code != 0:
            pp(result.output)

        assert result.exit_code == 0

    @pytest.mark.parametrize(
        'command',
        [
            'audit',
            'up',
            'version',
        ],
    )
    def test_sub_commands(self, runner: CliRunner, command: str):
        result = runner.invoke(cli, command.split())

        if result.exit_code != 0:
            pp(result.output)

        assert result.exit_code == 0
