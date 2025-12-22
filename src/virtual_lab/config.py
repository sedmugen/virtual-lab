import os
from pathlib import Path
from dotenv import load_dotenv

# --- 1. Load Environment Variables ---
# Automatically find the project root (3 levels up from this file)
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent.parent
env_path = project_root / '.env'

# Load the .env file
load_success = load_dotenv(dotenv_path=env_path)

# --- 2. Define API Providers ---

# Option A: BigModel / GLM-4 (Free)
BIGMODEL_API_KEY = os.getenv("BIGMODEL_API_KEY")
BIGMODEL_BASE_URL = os.getenv("BIGMODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")

# Option B: OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Option C: OpenAI (Official)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") # Optional, defaults to OpenAI's standard URL

# --- 3. Intelligent Selection Logic ---
# You can change the 'provider' variable below to switch providers easily.
# Options: "bigmodel", "openrouter", "openai"
ACTIVE_PROVIDER = "openai" 

if ACTIVE_PROVIDER == "bigmodel":
    if not BIGMODEL_API_KEY:
        raise ValueError("Error: BIGMODEL_API_KEY missing in .env")
    API_KEY = BIGMODEL_API_KEY
    BASE_URL = BIGMODEL_BASE_URL
    DEFAULT_MODEL = "glm-4-flash"
    print(f"🔧 Config: Using BigModel (GLM-4)")

elif ACTIVE_PROVIDER == "openrouter":
    if not OPENROUTER_API_KEY:
        raise ValueError("Error: OPENROUTER_API_KEY missing in .env")
    API_KEY = OPENROUTER_API_KEY
    BASE_URL = OPENROUTER_BASE_URL
    DEFAULT_MODEL = "gpt-4o" # Or whatever model you prefer on OpenRouter
    print(f"🔧 Config: Using OpenRouter")

elif ACTIVE_PROVIDER == "openai":
    if not OPENAI_API_KEY:
        raise ValueError("Error: OPENAI_API_KEY missing in .env")
    API_KEY = OPENAI_API_KEY
    BASE_URL = OPENAI_BASE_URL # Can be None, client handles it
    DEFAULT_MODEL = "gpt-4o"
    print(f"🔧 Config: Using OpenAI")

else:
    raise ValueError(f"Unknown provider: {ACTIVE_PROVIDER}")

# --- 4. Validation (Runs only if executed directly) ---
if __name__ == "__main__":
    print(f"Checking .env at: {env_path}")
    print(f"Loaded successfully? {load_success}")
    print(f"Active Key: {API_KEY[:5]}... (hidden)")
    print(f"Active URL: {BASE_URL}")
    print(f"Default Model: {DEFAULT_MODEL}")