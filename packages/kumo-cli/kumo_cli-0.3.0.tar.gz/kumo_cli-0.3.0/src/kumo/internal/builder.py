import os
from typing import Dict, List

import docker

from kumo.internal.logger import KumoLogger
from kumo.utils.constants import BUILDER_NAME

logger = KumoLogger(__name__)


class KumoBuilder:
    def __init__(
        self,
        dockerfile_path: str,
        image_tag: str,
        multiarch: bool = False,
        builder_name: str = BUILDER_NAME,
        context: str = ".",
    ):
        self.client = docker.from_env()
        self.dockerfile_path = dockerfile_path
        self.image_tag = image_tag
        self.builder_name = builder_name
        self.multiarch = multiarch
        self.context = context

    def create_builder(self):
        """Cria um novo builder para buildx."""

        # Verifica se o builder já existe
        existing_builders = (
            os.popen("docker buildx ls --format '{{.Name}}'")
            .read()
            .strip()
            .splitlines()
        )

        if self.builder_name in existing_builders:
            logger.warning(f"O builder '{self.builder_name}' já existe.")
            self.use_builder()  # Use o builder existente
        else:
            os.system(f"docker buildx create --name {self.builder_name} --use")
            os.system(f"docker buildx inspect {self.builder_name} --bootstrap")
            logger.info(f"O builder '{self.builder_name}' foi criado e está ativo.")

    def remove_builder(self):
        """Remove o builder buildx especificado."""
        os.system(f"docker buildx rm {self.builder_name}")
        logger.info(f"O builder '{self.builder_name}' removido.")

    def use_builder(self):
        """Ativa o builder buildx especificado para uso."""
        os.system(f"docker buildx use {self.builder_name}")
        logger.info(f"O builder '{self.builder_name}' está em uso.")

    def validate_buildx_options(self, platforms: List[str], load: bool, push: bool):
        """Valida as opções de buildx para garantir que são compatíveis."""
        if self.multiarch and platforms and len(platforms) > 1:
            if load:
                raise ValueError(
                    "`--load` não é compatível com múltiplas plataformas. "
                    "Use uma única plataforma com `load=True` ou defina `push=True` para múltiplas plataformas."
                )
            if load and not push:
                raise ValueError(
                    "`--load` não é compatível com múltiplas plataformas. "
                    "Use uma única plataforma ou defina `push=True` com `load=False`."
                )

    def buildx_command(
        self,
        build_args: Dict[str, str],
        platforms: List[str],
        no_cache: bool,
        load: bool,
        push: bool,
    ):
        """Constroi o comando `docker buildx build`."""
        command = [
            "docker",
            "buildx",
            "build",
            "-t",
            self.image_tag,
            "-f",
            self.dockerfile_path,
            self.context,
        ]

        if platforms:
            command.extend(["--platform", ",".join(platforms)])
        if no_cache:
            command.append("--no-cache")
        if load:
            command.append("--load")
        if push:
            command.append("--push")
        if build_args:
            for key, value in build_args.items():
                command.extend(["--build-arg", f"{key}={value}"])

        return command

    def build_image(
        self,
        build_args: Dict[str, str] = None,
        platforms: List[str] = None,
        no_cache: bool = False,
        load: bool = True,
        push: bool = False,
    ):
        """
        Build the Docker image using `docker build` or `docker buildx build`.
        """
        # Validação para uso do build use
        self.create_builder()

        # Validação das opções de buildx
        self.validate_buildx_options(platforms, load, push)

        try:
            if self.multiarch and platforms is not None:
                # Gera o comando buildx e executa
                command = self.buildx_command(
                    build_args, platforms, no_cache, load, push
                )
                result = os.system(" ".join(command))

                if result == 0:
                    print("Build multiarch concluído com sucesso.")
                else:
                    raise RuntimeError("Falha no build multiarch.")
            else:
                # Build padrão usando o SDK do Docker
                image, logs = self.client.images.build(
                    path=self.context,
                    dockerfile=self.dockerfile_path,
                    tag=self.image_tag,
                    buildargs=build_args,
                    nocache=no_cache,
                )
                logger.info(
                    f"Build padrão concluído com sucesso, imagem: {image} {logs}"
                )
        except Exception as e:
            logger.error(f"Erro durante o build: {e}")
