"""Non-secret settings, read from environment variables and an optional .env file."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Names of secrets that Argos knows about. Values are never stored here.
LLM_API_KEY = "LLM_API_KEY"


@dataclass(frozen=True)
class Settings:
    llm_provider: str = "groq"
    llm_model: str = "openai/gpt-oss-120b"


def load_settings() -> Settings:
    """Build settings from ARGOS_* environment variables, with defaults."""
    load_dotenv()
    defaults = Settings()
    return Settings(
        llm_provider=os.environ.get("ARGOS_LLM_PROVIDER", defaults.llm_provider),
        llm_model=os.environ.get("ARGOS_LLM_MODEL", defaults.llm_model),
    )
