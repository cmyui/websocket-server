from __future__ import annotations

import argon2


def authenticate_credentials(passphrase: bytes, hashed_passphrase: bytes) -> bool:
    """Authenticate a user with a passphrase."""
    return argon2.verify_password(
        hashed_passphrase,
        passphrase,
        type=argon2.Type.ID,
    )
