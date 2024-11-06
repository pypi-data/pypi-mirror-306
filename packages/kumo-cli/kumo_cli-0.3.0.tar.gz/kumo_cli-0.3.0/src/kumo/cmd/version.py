import typer

from kumo.utils.constants import APP_VERSION

version_app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    name="version",
    help="Mostra a versão atual do CLI",
    invoke_without_command=True,
)


@version_app.callback(invoke_without_command=True)
def version_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        execute()


def execute():
    typer.echo(f"Kumo CLI Version: {APP_VERSION}")
