from fastapi import APIRouter
from starlette.responses import PlainTextResponse
from prometheus_client import generate_latest
from .metrics import registry

metrics_router = APIRouter(prefix="")


@metrics_router.get("/prometheus")
async def metrics():
    return PlainTextResponse(content=generate_latest(registry))
