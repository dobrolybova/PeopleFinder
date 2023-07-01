import os

from prometheus_client import CollectorRegistry, Summary, multiprocess

registry = CollectorRegistry()
if "prometheus_multiproc_def" in os.environ:
    multiprocess.MultiProcessCollector(registry)

SERVER_REQUEST_COUNT = Summary(
    "server_req_seconds",
    "Server request metric",
    ["method", "outcome", "uri", "status"],
    registry=None,
)

CLIENT_REQUEST_COUNT = Summary(
    "client_req_seconds",
    "Client request metric",
    ["method", "outcome", "uri", "status"],
    registry=None,
)
