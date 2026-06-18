from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

StorageMode = Literal["local", "local_json", "memory"]


class AppSettings(BaseModel):
    storage_mode: StorageMode = Field(
        default="local_json",
        description="Repository adapter mode for local development.",
    )
    local_store_path: Path = Field(
        default=Path("backend/.local_data/learning_store.json"),
        description="Local JSON persistence path used when storage mode is local/local_json.",
    )


def load_settings() -> AppSettings:
    return AppSettings(
        storage_mode=os.getenv("PF_STORAGE_MODE", "local_json"),
        local_store_path=Path(
            os.getenv("PF_LOCAL_STORE_PATH", "backend/.local_data/learning_store.json")
        ),
    )
