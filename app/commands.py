from __future__ import annotations

import asyncio
import secrets
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import TypeVar

from app import connections
from app import models
from app import repositories
from app import usecases

CommandHandler = Callable[
    [connections.Connection, Mapping[str, Any]],
    Coroutine[Any, Any, Optional[Mapping[str, Any]]],
]


commands: MutableMapping[str, CommandHandler] = {}

T = TypeVar("T", bound=CommandHandler)


def register_command(trigger: str) -> Callable[[T], T]:
    def wrapper(f: T) -> T:
        commands[trigger] = f

        return f

    return wrapper


@register_command("signup")
async def sign_up(
    connection: connections.Connection,
    request_data: Mapping[str, Any],
) -> Optional[Mapping[str, Any]]:
    form_data = models.users.SignUpForm(
        email=request_data["email"],
        passphrase=request_data["passphrase"],
    )

    assert not connection.authenticated

    user_id = await repositories.users.sign_up(form_data)

    return {
        "status": "success",
        # "user_id": user_id,
        "request": request_data,
    }


@register_command("authenticate")
async def authenticate(
    connection: connections.Connection,
    request_data: Mapping[str, Any],
) -> Optional[Mapping[str, Any]]:
    form_data = models.users.AuthenticationForm(
        email=request_data["email"],
        passphrase=request_data["passphrase"],
    )

    user_row = await repositories.users.fetch(form_data.email)
    if user_row is None:
        # auth failed - user account does not exist
        return {
            "status": "failure",
            "reason": "invalid credentials",
        }

    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(
        None,  # default executor
        usecases.users.authenticate_credentials,
        form_data.passphrase,
        user_row["hashed_passphrase"],
    )
    if not result:
        # auth failed - password is incorrect
        return {
            "status": "failure",
            "reason": "invalid credentials",
        }

    # auth succeeded - create a session for them
    connection.session = connections.Session(token=secrets.token_urlsafe(32))

    return {
        "status": "success",
        "session_token": connection.session.token,
        "request": form_data.__dict__,
    }
