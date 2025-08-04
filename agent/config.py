"""Configuration dataclass for API credentials."""

from dataclasses import dataclass
import os


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    strapi_url: str = os.getenv("STRAPI_URL", "")
    strapi_token: str | None = os.getenv("STRAPI_TOKEN")
    mux_token: str | None = os.getenv("MUX_TOKEN")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_key: str | None = os.getenv("SUPABASE_KEY")


settings = Settings()
