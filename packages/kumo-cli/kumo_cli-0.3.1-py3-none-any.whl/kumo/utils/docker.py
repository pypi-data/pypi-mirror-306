import os

import docker

from kumo.internal.logger import KumoLogger

logger = KumoLogger(__name__)


class KumoUtilsDocker:

    def __init__(self, image_tag: str, network_name: str = "kumo-net") -> None:
        self.client = docker.from_env()
        self.image_tag = image_tag
        self.network_name = network_name

    def remove_image(self):
        """Remove the Docker image."""

        try:
            self.client.images.remove(image=self.image_tag, force=True)
            logger.info(f"Image {self.image_tag} removed successfully.")
        except docker.errors.ImageNotFound:
            logger.error(f"Image {self.image_tag} not found.")

    def create_network(self):
        """Cria uma nova rede Docker, ou usa uma existente."""
        existing_networks = (
            os.popen("docker network ls --format '{{.Name}}'")
            .read()
            .strip()
            .splitlines()
        )

        if self.network_name in existing_networks:
            logger.warning(
                f"A rede '{self.network_name}' já existe. Usando a rede existente."
            )
        else:
            os.system(f"docker network create {self.network_name}")
            logger.info(f"Rede '{self.network_name}' criada.")

    def remove_network(self):
        """Remove a rede Docker especificada, se existir."""
        existing_networks = (
            os.popen("docker network ls --format '{{.Name}}'")
            .read()
            .strip()
            .splitlines()
        )

        if self.network_name in existing_networks:
            os.system(f"docker network rm {self.network_name}")
            logger.info(f"Rede '{self.network_name}' removida.")
        else:
            logger.warning(f"A rede '{self.network_name}' não existe, nada a remover.")
