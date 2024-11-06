from typing import Dict, List, Literal, Optional

from kumo.model.config.base import KumoBaseConfig


class KumoBuilderConfig(KumoBaseConfig):

    multiarch: bool
    dockerfile: str
    context: str
    versioning: Literal["timestamp", "hash", "tag"]
    environment: str
    arch: List[str]
    args: Optional[Dict[str, Optional[str]]]
    env: List[str]
