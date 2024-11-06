import typer

from kumo.cmd.build import build_app
from kumo.cmd.deploy import deploy_app
from kumo.cmd.init import init_app
from kumo.cmd.step import step_app
from kumo.cmd.system import system_app
from kumo.cmd.version import version_app

app = typer.Typer(add_completion=True, no_args_is_help=True)


app.add_typer(build_app, name="build")
app.add_typer(deploy_app, name="deploy")
app.add_typer(init_app, name="init")
app.add_typer(step_app, name="step")
app.add_typer(system_app, name="system")
app.add_typer(version_app, name="version")
