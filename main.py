#!/usr/bin/env python3.9
from __future__ import annotations

import uvicorn


def main() -> int:
    uvicorn.run("app.api.init_api:app")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
