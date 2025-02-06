from pathlib import Path

from starlette.config import Config

# Config will read first from environment variables,
# then from the `.env` file at the git repository's root
config = Config(Path(__file__).parent.parent / ".env")

# Static files
DEFAULT_ASSETS_DIR = Path(__file__).parent.parent / ".assets"
ASSETS_DIR = config("ASSETS_DIR", default=DEFAULT_ASSETS_DIR)

# Database
DATABASE_URL = config("DATABASE_URL", default="sqlite:///./app/database/database.db")
