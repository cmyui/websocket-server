from __future__ import annotations

import fastapi

from app import services
from app.api.v1.websocket import websocket_router


def init_routers(app: fastapi.FastAPI) -> None:
    app.include_router(websocket_router)


def init_event_handlers(app: fastapi.FastAPI) -> None:
    @app.on_event("startup")
    async def on_startup() -> None:
        await services.database.connect()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await services.database.disconnect()


def init_api() -> fastapi.FastAPI:
    app = fastapi.FastAPI()

    init_routers(app)
    init_event_handlers(app)

    return app


app = init_api()
