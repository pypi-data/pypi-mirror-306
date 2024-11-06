import typer

from kumo.internal.logger import KumoLogger

logger = KumoLogger(__name__)

step_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    name="step",
    help="Executa um step específico do fluxo de deploy",
)


@step_app.command(
    name="send_image", no_args_is_help=True, help="Envia a imagem para o servidor"
)
def send_image():
    print("Executando o envio da imagem para o servidor")


@step_app.command(name="create_dc", no_args_is_help=True, help="Cria o docker-compose")
def create_dc():
    print("Executando a criação do docker compose")


@step_app.command(
    name="copy", no_args_is_help=True, help="Copia os arquivos e envia para o servidor"
)
def copy():
    print("Executando a cópia das configurações")


@step_app.command(name="up", no_args_is_help=True, help="Ativa uma release")
def up():
    print("Executando a ativação de uma release")


@step_app.command(
    name="rollback", no_args_is_help=True, help="Faz rollback da última versão ativada"
)
def rollback():
    print("Executando o rollback da última versão ativada")
