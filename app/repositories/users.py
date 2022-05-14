from __future__ import annotations

from typing import Any
from typing import Mapping
from typing import Optional

from app import models
from app import services


## create


async def sign_up(form_data: models.users.SignUpForm) -> int:
    async with services.database.transaction():
        user_id = await services.database.execute(
            "INSERT INTO profiles (email) VALUES (:email)",
            {"email": form_data.email},
        )
        assert user_id is not None  # TODO: is this even possible?

        await services.database.execute(
            "INSERT INTO credentials (user_id, passphrase) "
            "VALUES (:user_id, :passphrase)",
            {"user_id": user_id, "passphrase": form_data.passphrase},
        )

    return user_id


## read


async def fetch(email: str) -> Optional[Mapping[str, Any]]:
    return await services.database.fetch_one(
        "SELECT * FROM users WHERE email = :email",
        {"email": email},
    )


## update

## delete
