import os

from prometheus_client import CollectorRegistry, Summary, multiprocess

registry = CollectorRegistry()
sum_registry = registry
if "prometheus_multiproc_def" in os.environ:
    multiprocess.MultiProcessCollector(registry)
    # registry should be None in case of multiprocess
    sum_registry = None

SERVER_REQUEST = Summary(
    "server_req_seconds",
    "Server request metric",
    ["method", "uri", "status"],
    registry=sum_registry,
)

CLIENT_REQUEST = Summary(
    "client_req_seconds",
    "Client request metric",
    ["method", "uri", "status"],
    registry=sum_registry,
)
