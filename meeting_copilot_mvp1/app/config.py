"""Application configuration for Meeting Copilot MVP1."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment and `.env`."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Meeting Copilot MVP1"
    app_version: str = "0.1.0"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    whisper_model_size: str = "base"
    whisper_compute_type: str = "int8"
    chunk_seconds: int = 5
    summary_interval_seconds: int = 60

    database_url: str = Field(default="sqlite:///data/meetings.db")
    data_dir: Path = Path("data")
    export_dir: Path = Path("data/exports")

    report_brand: str = "Meeting Copilot"
    report_timeout_seconds: int = 90


settings = Settings()
