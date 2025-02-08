from pathlib import Path

from starlette.config import Config

# Config will read first from environment variables,
# then from the `.env` file at the git repository's root
config = Config(Path(__file__).parent.parent / ".env")

# Database
DATABASE_URL = config("DATABASE_URL", default="sqlite:///./app/database/database.db")
