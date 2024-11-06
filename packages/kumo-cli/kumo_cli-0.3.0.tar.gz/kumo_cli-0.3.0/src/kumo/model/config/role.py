from typing import List, Optional

from pydantic import Field
from typing_extensions import Annotated

from kumo.model.config.base import KumoBaseConfig


class KumoRoleLabels(KumoBaseConfig):
    traefik_enable: Optional[bool] = Field(..., alias="traefik.enable")
    traefik_http_routers_rule: Optional[str] = Field(
        ..., alias="traefik.http.routers.router-name.rule"
    )

    traefik_http_routers_entrypoints: Optional[str] = Field(
        ..., alias="traefik.http.routers.router-name.entrypoints"
    )

    traefik_http_routers_tls: Optional[bool] = Field(
        ..., alias="traefik.http.routers.router-name.tls"
    )

    traefik_http_routers_tls_certresolver: Optional[str] = Field(
        ..., alias="traefik.http.routers.router-name.tls.certresolver"
    )


class KumoRoleOptions(KumoBaseConfig):
    memory: Optional[str]
    cpus: Optional[Annotated[int, Field(strict=True, ge=1)]]


class KumoRoleConfig(KumoBaseConfig):
    hosts: List[str]
    labels: Optional[KumoRoleLabels]
    options: Optional[KumoRoleOptions]
    env: Optional[List[str]]
