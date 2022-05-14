from __future__ import annotations

from starlette.config import Config

config = Config(".env")

DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT", cast=int)
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_NAME = config("DB_NAME")

DB_DSN = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
