"""LLM provider configuration for Virtual Lab.

Supports three providers selectable via ``ACTIVE_PROVIDER``:

* ``"openai"``     — OpenAI official API (requires ``OPENAI_API_KEY``).
* ``"openrouter"`` — OpenRouter proxy (requires ``OPENROUTER_API_KEY``).
* ``"bigmodel"``   — BigModel / GLM-4-Flash, free tier available
                     (requires ``BIGMODEL_API_KEY``).

Change ``ACTIVE_PROVIDER`` below to switch providers. All keys are read
from the ``.env`` file in the project root via python-dotenv.

Exported module-level names
---------------------------
API_KEY      : str            Active API key.
BASE_URL     : str | None     Provider base URL (None uses the client default).
DEFAULT_MODEL: str            Default model name for the active provider.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# --- Load environment variables ---
_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

# --- API credentials (read from environment) ---
BIGMODEL_API_KEY = os.getenv("BIGMODEL_API_KEY")
BIGMODEL_BASE_URL = os.getenv("BIGMODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")  # None uses the SDK default

# --- Active provider selection ---
# Change this value to switch providers.
ACTIVE_PROVIDER = "openai"


def get_config() -> tuple[str, str | None, str]:
    """Return ``(api_key, base_url, default_model)`` for the active provider.

    Raises ``ValueError`` if the required API key for the selected provider
    is not set in the environment.

    :return: A tuple of (api_key, base_url, default_model).
    """
    if ACTIVE_PROVIDER == "bigmodel":
        if not BIGMODEL_API_KEY:
            raise ValueError(
                "BIGMODEL_API_KEY is not set. Add it to your .env file "
                "(see .env.example)."
            )
        return BIGMODEL_API_KEY, BIGMODEL_BASE_URL, "glm-4-flash"

    elif ACTIVE_PROVIDER == "openrouter":
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is not set. Add it to your .env file "
                "(see .env.example)."
            )
        return OPENROUTER_API_KEY, OPENROUTER_BASE_URL, "gpt-4o"

    elif ACTIVE_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. Add it to your .env file "
                "(see .env.example)."
            )
        return OPENAI_API_KEY, OPENAI_BASE_URL, "gpt-4o"

    else:
        raise ValueError(
            f"Unknown provider: {ACTIVE_PROVIDER!r}. "
            "Valid options are 'openai', 'openrouter', 'bigmodel'."
        )


# Resolve at import time so downstream modules can import these names directly.
API_KEY, BASE_URL, DEFAULT_MODEL = get_config()


if __name__ == "__main__":
    key, url, model = get_config()
    print(f"Provider : {ACTIVE_PROVIDER}")
    print(f"Base URL : {url}")
    print(f"Model    : {model}")
    print(f"Key      : {key[:8]}... (truncated)")
