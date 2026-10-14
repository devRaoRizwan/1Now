import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BACKEND_DIR.parent / "frontend" / "dist"
DEFAULT_DATABASE_PATH = BACKEND_DIR / "data" / "trust.db"

# Must never change once reports exist, or stored fingerprints stop matching.
NETWORK_SECRET = os.environ.get("TRUST_NETWORK_SECRET", "dev-only-secret-change-me").encode()

# Old incidents say little about a customer today, and people deserve a way back.
REPORT_RETENTION_DAYS = 730


def database_path() -> Path:
    return Path(os.environ.get("TRUST_DB_PATH", DEFAULT_DATABASE_PATH))
