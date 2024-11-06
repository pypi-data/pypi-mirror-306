from pathlib import Path

import typer
import yaml
from jinja2 import Environment, FileSystemLoader

from kumo.internal.logger import KumoLogger
from kumo.utils.common import get_config_template_path

logger = KumoLogger(__name__)

init_app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    name="init",
    help="Inicia o projeto kumo cli",
    invoke_without_command=True,
)


@init_app.callback(invoke_without_command=True)
def init_callback(
    ctx: typer.Context,
    stage: str = typer.Option(
        None, "--stage", help="Define o stage para a configuração"
    ),
):
    if ctx.invoked_subcommand is None:
        config(stage)


@init_app.command(None, hidden=True)
def config(
    stage: str = typer.Option(
        None, "--stage", help="Define o stage para a configuração"
    )
):

    if stage:
        logger.info(f"Criando config para o stage: {stage}")
    else:
        logger.info("Criando config padrão")

    _write_config(stage=stage)


def _write_config(stage: str = "", data: dict = {}):

    # Obtém o path da lib instalada para compor o caminho completo do config.j2
    config_template_path = get_config_template_path()

    # Configuração do ambiente Jinja2
    env = Environment(loader=FileSystemLoader(config_template_path))

    # Carregando o template Jinja2
    template_name = "config.j2"
    template = env.get_template(template_name)

    # Renderizando o template
    rendered_content = template.render(data)

    # Convertendo para YAML
    yaml_content = yaml.safe_load(rendered_content)

    # Escrevendo o YAML em um arquivo
    # Nome do arquivo de saída baseado no stage
    if stage:
        output_file = f"deploy.{stage}.yaml"
    else:
        output_file = "deploy.yaml"

    # Definindo o caminho do diretório
    output_dir = Path(".kumo/config")

    # Criando o diretório se não existir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Escrevendo o YAML em um arquivo
    file_path = output_dir / output_file
    with open(file_path, "w") as file:
        yaml.dump(yaml_content, file, default_flow_style=False)
