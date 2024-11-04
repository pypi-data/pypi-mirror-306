from collections.abc import Iterable, Mapping
from typing import Any, ClassVar, Optional

from blacksmith import (
    AbstractCollectionParser,
    HTTPTimeout,
    PrometheusMetrics,
    SyncAbstractServiceDiscovery,
    SyncAbstractTransport,
    SyncClient,
    SyncClientFactory,
    SyncConsulDiscovery,
    SyncHTTPMiddleware,
    SyncNomadDiscovery,
    SyncRouterDiscovery,
    SyncStaticDiscovery,
)
from blacksmith.typing import ClientName
from django.http.request import HttpRequest
from django.utils.module_loading import import_string

from dj_blacksmith._settings import get_clients, get_transport
from dj_blacksmith.client._sync.middleware import SyncHTTPMiddlewareBuilder
from dj_blacksmith.client._sync.middleware_factory import (
    SyncAbstractMiddlewareFactoryBuilder,
)


def build_sd(
    settings: Mapping[str, Mapping[str, Any]],
) -> SyncAbstractServiceDiscovery:
    sd_setting = settings.get("sd", "")
    if sd_setting == "consul":
        return SyncConsulDiscovery(**settings["consul_sd_config"])
    elif sd_setting == "nomad":
        return SyncNomadDiscovery(**settings["nomad_sd_config"])
    elif sd_setting == "router":
        return SyncRouterDiscovery(**settings["router_sd_config"])
    elif sd_setting == "static":
        endpoints: dict[tuple[str, Optional[str]], str] = {}
        for key, val in settings["static_sd_config"].items():
            if "/" in key:
                srv, ver = key.rsplit("/", 1)
            else:
                srv, ver = key, None
            endpoints[(srv, ver)] = val
        return SyncStaticDiscovery(endpoints)
    else:
        raise RuntimeError(f"Unkown service discovery {sd_setting}")


def build_collection_parser(settings: dict[str, Any]) -> type[AbstractCollectionParser]:
    cls = import_string(
        settings.get("collection_parser", "blacksmith.CollectionParser")
    )
    return cls


def build_transport() -> Optional[type[SyncAbstractTransport]]:
    transport = get_transport()
    if not transport:
        return None
    cls = import_string(transport)
    return cls


def build_metrics(settings: dict[str, Any]) -> PrometheusMetrics:
    metrics = settings.get("metrics", {})
    return PrometheusMetrics(**metrics)


def build_middlewares(
    settings: Mapping[str, Any],
    metrics: PrometheusMetrics,
) -> Iterable[SyncHTTPMiddleware]:
    middlewares: list[str] = settings.get("middlewares", [])
    for middleware in middlewares:
        cls: type[SyncHTTPMiddlewareBuilder] = import_string(middleware)
        yield cls(settings, metrics).build()


def client_factory(name: str = "default") -> SyncClientFactory[Any]:
    settings = get_clients().get(name)
    if settings is None:
        raise RuntimeError(f"Client {name} does not exists")
    sd = build_sd(settings)
    timeout = settings.get("timeout", {})
    collection_parser = build_collection_parser(settings)
    transport = build_transport()
    cli: SyncClientFactory[Any] = SyncClientFactory(
        sd,
        proxies=settings.get("proxies"),
        verify_certificate=settings.get("verify_certificate", True),
        timeout=HTTPTimeout(**timeout),
        collection_parser=collection_parser,
        transport=transport() if transport else None,
    )
    metrics = build_metrics(settings)
    for middleware in build_middlewares(settings, metrics):
        cli.add_middleware(middleware)
    cli.initialize()
    return cli


def build_middlewares_factories(
    settings: Mapping[str, Any],
) -> Iterable[SyncAbstractMiddlewareFactoryBuilder]:
    middlewares: list[str] = settings.get("middleware_factories", [])
    for middleware in middlewares:
        cls: type[SyncAbstractMiddlewareFactoryBuilder] = import_string(middleware)
        yield cls(settings)


def middleware_factories(name: str = "default"):
    settings = get_clients()[name]
    return list(build_middlewares_factories(settings))


class SyncClientProxy:
    def __init__(
        self,
        client_factory: SyncClientFactory[Any],
        middlewares: list[SyncHTTPMiddleware],
    ):
        self.client_factory = client_factory
        self.middlewares = middlewares

    def __call__(self, client_name: ClientName) -> SyncClient[Any]:
        cli = self.client_factory(client_name)
        for middleware in self.middlewares:
            cli.add_middleware(middleware)
        return cli


class SyncDjBlacksmithClient:
    client_factories: ClassVar[dict[str, SyncClientFactory[Any]]] = {}
    middleware_factories: ClassVar[
        dict[str, list[SyncAbstractMiddlewareFactoryBuilder]]
    ] = {}

    def __init__(self, request: HttpRequest):
        self.request = request

    def __call__(self, factory_name: str = "default") -> SyncClientProxy:
        if factory_name not in self.client_factories:
            self.client_factories[factory_name] = client_factory(factory_name)
            self.middleware_factories[factory_name] = middleware_factories(factory_name)

        return SyncClientProxy(
            self.client_factories[factory_name],
            [m(self.request) for m in self.middleware_factories[factory_name]],
        )
