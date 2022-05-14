from __future__ import annotations

import databases

import app.settings

database = databases.Database(app.settings.DB_DSN)
