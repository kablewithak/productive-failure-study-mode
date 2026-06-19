from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

StorageMode = Literal["local", "local_json", "memory"]


def _csv_env(name: str, default: list[str]) -> list[str]:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value.strip() == "":
        return default
    return [item.strip() for item in raw_value.split(",") if item.strip()]


class AppSettings(BaseModel):
    storage_mode: StorageMode = Field(
        default="local_json",
        description="Repository adapter mode for local development.",
    )
    local_store_path: Path = Field(
        default=Path("backend/.local_data/learning_store.json"),
        description="Local JSON persistence path used when storage mode is local/local_json.",
    )
    frontend_allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Browser origins allowed to call the backend API during local development.",
    )


def load_settings() -> AppSettings:
    return AppSettings(
        storage_mode=os.getenv("PF_STORAGE_MODE", "local_json"),
        local_store_path=Path(
            os.getenv("PF_LOCAL_STORE_PATH", "backend/.local_data/learning_store.json")
        ),
        frontend_allowed_origins=_csv_env(
            "PF_FRONTEND_ALLOWED_ORIGINS",
            ["http://localhost:3000", "http://127.0.0.1:3000"],
        ),
    )
