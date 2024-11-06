from typing import List

from pydantic import Field

from kumo.model.config.base import KumoBaseConfig


class KumoProxyOptions(KumoBaseConfig):
    publish: List[str]
    volume: List[str]


class KumoProxyArgs(KumoBaseConfig):
    entryPoints_http_address: str = Field(..., alias="entryPoints.http.address")
    entryPoints_websecure_address: str = Field(
        ..., alias="entryPoints.websecure.address"
    )
    api_insecure: bool = Field(..., alias="api.insecure")
    api_dashboard: bool = Field(..., alias="api.dashboard")
    certificatesResolvers_acme_email: str = Field(
        ..., alias="certificatesResolvers.letsencrypt.acme.email"
    )
    certificatesResolvers_acme_storage: str = Field(
        ..., alias="certificatesResolvers.letsencrypt.acme.storage"
    )
    certificatesResolvers_acme_httpchallenge: bool = Field(
        ..., alias="certificatesResolvers.letsencrypt.acme.httpchallenge"
    )
    certificatesResolvers_acme_httpchallenge_entrypoint: str = Field(
        ..., alias="certificatesResolvers.letsencrypt.acme.httpchallenge.entrypoint"
    )


class KumoProxyLabels(KumoBaseConfig):
    traefik_http_routers_catchall_entryPoints: str = Field(
        ..., alias="traefik.http.routers.catchall.entryPoints"
    )
    traefik_http_routers_catchall_rule: str = Field(
        ..., alias="traefik.http.routers.catchall.rule"
    )
    traefik_http_routers_catchall_service: str = Field(
        ..., alias="traefik.http.routers.catchall.service"
    )
    traefik_http_routers_catchall_priority: str = Field(
        ..., alias="traefik.http.routers.catchall.priority"
    )
    traefik_http_services_unavailable_loadbalancer_server_port: str = Field(
        ..., alias="traefik.http.services.unavailable.loadbalancer.server.port"
    )
    traefik_http_routers_api_service: str = Field(
        ..., alias="traefik.http.routers.api.service"
    )
    traefik_http_routers_api_entrypoints: str = Field(
        ..., alias="traefik.http.routers.api.entrypoints"
    )
    traefik_http_routers_api_rule: str = Field(
        ..., alias="traefik.http.routers.api.rule"
    )
    traefik_http_routers_api_tls: bool = Field(
        ..., alias="traefik.http.routers.api.tls"
    )
    traefik_http_routers_api_middlewares: str = Field(
        ..., alias="traefik.http.routers.api.middlewares"
    )
    traefik_http_middlewares_auth_basicauth_users: str = Field(
        ..., alias="traefik.http.middlewares.auth.basicauth.users"
    )


class KumoProxyConfig(KumoBaseConfig):
    name: str
    options: KumoProxyOptions
    args: KumoProxyArgs
    labels: KumoProxyLabels
