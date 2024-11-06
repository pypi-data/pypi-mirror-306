import typer

from kumo.internal.logger import KumoLogger

logger = KumoLogger(__name__)

deploy_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    name="deploy",
    help="Executa o deploy atual do projeto",
)


@deploy_app.command(name="docker", no_args_is_help=True)
def docker():
    print("Executando o deploy... docker")


@deploy_app.command(name="swarm", no_args_is_help=True)
def docker():
    print("Executando o deploy... docker swarm")


@deploy_app.command(name="kubernetes", no_args_is_help=True)
def docker():
    print("Executando o deploy... kubernetes")
