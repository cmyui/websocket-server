from __future__ import annotations

import fastapi

from app import commands
from app import connections

websocket_router = fastapi.APIRouter()


manager = connections.ConnectionManager()


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: fastapi.WebSocket):
    """Handle a websocket connection from an external client."""
    connection = connections.Connection(websocket)
    await manager.connect(connection)

    try:
        # handle indefinite messages from this client
        while True:
            request_data = await websocket.receive_json()  # TODO: use (ultra|or)json?
            assert "command" in request_data

            command_handler = commands.commands.get(request_data["command"])
            if command_handler is None:
                return {
                    "status": "failure",
                    "reason": "unknown command",
                }

            response_data = await command_handler(connection, request_data)
            await websocket.send_json(response_data)

    except fastapi.WebSocketDisconnect:
        manager.disconnect(connection)
        await manager.broadcast(b"client disconnected")
    except Exception as exc:
        manager.disconnect(connection)
        print(exc)
