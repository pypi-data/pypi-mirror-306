import typer

from kumo.internal.logger import KumoLogger

logger = KumoLogger(__name__)

system_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    name="system",
    help="Executa o system atual do projeto",
)


@system_app.command(name="service", no_args_is_help=True)
def service():
    print("Executando o system... docker")


@system_app.command(name="details", no_args_is_help=True)
def details():
    print("Executando o system... docker swarm")


@system_app.command(name="stats", no_args_is_help=True)
def stats():
    print("Executando o system... kubernetes")
