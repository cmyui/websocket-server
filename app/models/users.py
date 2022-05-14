from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class AuthenticationForm(BaseModel):
    email: str  # TODO: regex?
    passphrase: str = Field(..., min_length=8)  # TODO: regex?


class SignUpForm(BaseModel):
    email: str  # TODO: regex?
    passphrase: str = Field(..., min_length=8)  # TODO: regex?

    # TODO: more
