from typing import Dict

import yaml

from kumo.model.config.base import KumoBaseConfig
from kumo.model.config.builder import KumoBuilderConfig
from kumo.model.config.proxy import KumoProxyConfig
from kumo.model.config.registry import KumoRegistryConfig
from kumo.model.config.role import KumoRoleConfig
from kumo.model.config.ssh import KumoSSHConfig


class KumoConfig(KumoBaseConfig):

    service: str
    image: str
    role: Dict[str, KumoRoleConfig]
    builder: KumoBuilderConfig
    ssh: KumoSSHConfig
    registry: KumoRegistryConfig
    proxy: KumoProxyConfig

    # Método para carregar a configuração a partir de um arquivo YAML
    @classmethod
    def from_yaml(cls, file_path: str) -> "KumoConfig":
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)
