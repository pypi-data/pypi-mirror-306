import typer
import uv_up
from uv_audit.cli import cli as uv_audit_cli
from uv_up.cli import app as uv_up_cli
from uv_version.cli import cli as uv_version_cli
from uv_stats.cli import cli as uv_stats_cli

cli = typer.Typer(help='uvxt')
cli.add_typer(uv_up_cli, name='up')
cli.add_typer(uv_version_cli, name='version')
cli.add_typer(uv_audit_cli, name='audit')
cli.add_typer(uv_stats_cli, name='stats')


def version_callback(value: bool):
    if value:
        print(f'Version of uvxt is {uv_up.__version__}')
        raise typer.Exit()


@cli.callback(invoke_without_command=True)
def callback(  # noqa: C901
    ctx: typer.Context,
    #
    version: bool = typer.Option(
        False,
        '--version',
        callback=version_callback,
        help='Print version of uvxt.',
        is_eager=True,
    ),
):
    pass
