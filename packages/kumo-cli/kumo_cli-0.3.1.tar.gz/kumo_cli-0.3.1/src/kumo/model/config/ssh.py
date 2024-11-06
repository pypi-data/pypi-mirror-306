from typing import List

from kumo.model.config.base import KumoBaseConfig


class KumoSSHConfig(KumoBaseConfig):
    user: str
    keys: List[str]
