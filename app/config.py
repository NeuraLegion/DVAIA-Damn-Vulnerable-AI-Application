"""
App-level config from environment. No Flask coupling.
Load .env in api/__main__.py; app reads os.getenv.
"""
import os
from pathlib import Path
from typing import Optional


def get_database_uri() -> str:
    """SQLite path for app DB. Default: project root / data / app.db."""
    uri = os.getenv("DATABASE_URI", "")
    if uri:
        return uri
    root = Path(__file__).resolve().parent.parent
    data = root / "data"
    data.mkdir(exist_ok=True)
    return str(data / "app.db")


def get_secret_key() -> str:
    """Flask SECRET_KEY for sessions. Default: fixed dev key (set in prod)."""
    return os.getenv("SECRET_KEY", "dev-secret-change-in-production")


def get_upload_dir() -> str:
    """Directory for uploaded files. Default: project root / data / uploads."""
    path = os.getenv("UPLOAD_DIR", "")
    if path:
        return path
    root = Path(__file__).resolve().parent.parent
    uploads = root / "data" / "uploads"
    uploads.mkdir(parents=True, exist_ok=True)
    return str(uploads)


def get_mfa_issuer() -> str:
    """Optional MFA issuer name for display."""
    return os.getenv("MFA_ISSUER", "RedTeamApp")


def get_qdrant_url() -> str:
    """Qdrant server URL. When QDRANT_HOST is set (e.g. by Docker), use http://QDRANT_HOST:port so .env cannot override with localhost."""
    host = os.getenv("QDRANT_HOST", "").strip()
    if host:
        port = os.getenv("QDRANT_PORT", "6333").strip()
        return f"http://{host}:{port}"
    return os.getenv("QDRANT_URL", "http://localhost:6333").strip()


def get_qdrant_collection() -> str:
    """Qdrant collection name for RAG chunks. Default: rag_chunks."""
    return os.getenv("QDRANT_COLLECTION", "rag_chunks").strip()


def get_qdrant_api_key() -> Optional[str]:
    """Optional Qdrant API key (e.g. for Qdrant Cloud)."""
    val = os.getenv("QDRANT_API_KEY", "").strip()
    return val if val else None
