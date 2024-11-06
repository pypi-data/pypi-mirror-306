import os

import typer

from kumo.internal.builder import KumoBuilder
from kumo.internal.config import KumoConfig
from kumo.internal.logger import KumoLogger

logger = KumoLogger(__name__)

build_app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    name="build",
    help="Faz o build do projeto",
    invoke_without_command=True,
)


@build_app.callback(invoke_without_command=True)
def build_callback(
    ctx: typer.Context,
    stage: str = typer.Option(
        None, "--stage", help="Define o stage para a configuração"
    ),
):
    if ctx.invoked_subcommand is None:
        config(stage)


@build_app.command(None, hidden=True)
def config(
    stage: str = typer.Option(
        None, "--stage", help="Define o stage para a configuração"
    )
):

    config_file = ".kumo/config/deploy.yaml"

    if stage:
        config_file = f".kumo/config/deploy.{stage}.yaml"
        logger.info(f"Criando o build para o stage: {stage}")

    if os.path.isfile(config_file):
        config_data = KumoConfig.from_yaml(config_file)
        logger.info("Build iniciado")
        result = build(config_data=config_data)
        # print(result)
        if result:
            logger.info("Build finalizado")
    else:
        logger.error(f"Arquivo de configuração: {config_file} não existe")


def build(config_data):
    builder = KumoBuilder(
        dockerfile_path=config_data.builder.dockerfile,
        image_tag=config_data.image,
        multiarch=config_data.builder.multiarch,
    )
    builder.build_image(
        build_args=config_data.builder.args,
        platforms=config_data.builder.arch,
        no_cache=True,
        load=(
            True if config_data.builder.multiarch == False else False
        ),  # Load image locally after build
        push=True if config_data.builder.multiarch == True else False,
    )
