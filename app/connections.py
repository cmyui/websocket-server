from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Optional

import fastapi


@dataclass
class Session:
    token: str


@dataclass
class Connection:
    websocket: fastapi.WebSocket
    session: Optional[Session] = None

    @property
    def authenticated(self) -> bool:
        return self.session is not None


@dataclass
class ConnectionManager:
    connections: list[Connection] = field(default_factory=list)

    async def connect(self, connection: Connection) -> None:
        await connection.websocket.accept()
        self.connections.append(connection)

    def disconnect(self, connection: Connection) -> None:
        self.connections.remove(connection)

    async def broadcast(self, data: bytes) -> None:
        for connection in self.connections:
            await connection.websocket.send_bytes(data)
