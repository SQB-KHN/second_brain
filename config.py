"""SecondSelf shared configuration — paths, thresholds, and API settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.resolve()


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    """Parse an integer env/secret value; fall back on missing or invalid input."""
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return max(1, int(str(value).strip()))
    except (ValueError, TypeError):
        return default


def resolve_deploy_mode() -> bool:
    """
    Detect deploy/demo mode.

    Explicit ``DEPLOY_MODE`` env/secret wins. Otherwise, use the committed
    ``demo/`` bundle when ``data/graph.json`` is missing (typical on Streamlit Cloud).
    """
    if os.getenv("DEPLOY_MODE") is not None:
        return _env_flag("DEPLOY_MODE")

    data_graph = ROOT / "data" / "graph.json"
    demo_graph = ROOT / "demo" / "graph.json"
    knowledge_pointer = ROOT / "data" / "knowledge" / "current.json"
    return not data_graph.is_file() and not knowledge_pointer.is_file() and demo_graph.is_file()


def resolve_data_dir() -> Path:
    """
    Resolve the active data directory.

    Local development uses ``data/``. Cloud deploy sets ``DEPLOY_MODE=true``
    (or ``SECONDSELF_DATA_DIR=demo``) to read the committed demo bundle.
    """
    explicit = os.getenv("SECONDSELF_DATA_DIR", "").strip()
    if explicit:
        path = Path(explicit)
        return path if path.is_absolute() else (ROOT / path).resolve()

    if resolve_deploy_mode():
        return ROOT / "demo"

    return ROOT / "data"


DEPLOY_MODE = resolve_deploy_mode()
DATA_DIR = resolve_data_dir()
RAW_DIR = DATA_DIR / "raw"
RAW_ASSETS_DIR = RAW_DIR / "assets"
WIKI_DIR = DATA_DIR / "wiki"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
LOGS_DIR = ROOT / "logs"
GRAPH_FILE = DATA_DIR / "graph.json"
GRAPH_HTML = ROOT / "graph.html"
OBSIDIAN_VAULT_DIR = ROOT.parent / "secondself-obsidian-vault"
META_FILE = DATA_DIR / "meta.json"
LEGACY_META_FILE = RAW_DIR / "meta.json"
WIKI_INDEX_FILE = WIKI_DIR / ".index.json"
EMBEDDINGS_INDEX_FILE = EMBEDDINGS_DIR / "index.json"
PIPELINE_LOG = LOGS_DIR / "pipeline.log"

SIMILARITY_THRESHOLD = 0.82
RAG_TOP_K = 5
MIN_RETRIEVAL_SCORE = 0.5
RAG_MAX_EXCERPT_CHARS = 1200
RAG_MAX_CONTEXT_CHARS = 8000
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = "gpt-4o-mini"
BIDIRECTIONAL_LINKS = _env_flag("BIDIRECTIONAL_LINKS", default=True)

# Public deploy safeguards (EC-DEP-003, EC-DEP-006)
ENABLE_CAPTURE = _env_flag("ENABLE_CAPTURE", default=True)
ENABLE_REFRESH_BRAIN = _env_flag("ENABLE_REFRESH_BRAIN", default=not DEPLOY_MODE)
ASK_RATE_LIMIT_PER_MINUTE = _env_int("ASK_RATE_LIMIT", 10)
CAPTURE_RATE_LIMIT_PER_MINUTE = _env_int("CAPTURE_RATE_LIMIT", 5)

MAX_FILE_SIZE_MB = 25
URL_TIMEOUT_SECONDS = 30
URL_MAX_REDIRECTS = 5

PARA_FOLDERS = ["projects", "areas", "resources", "archives"]
PARA_COLORS = {
    "projects": "#22c55e",
    "areas": "#3b82f6",
    "resources": "#f97316",
    "archives": "#9ca3af",
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_LLM_MODEL = os.getenv("GROQ_LLM_MODEL", "llama-3.3-70b-versatile")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

REQUIRED_DIRS = [
    DATA_DIR,
    RAW_DIR,
    RAW_ASSETS_DIR,
    WIKI_DIR / "projects",
    WIKI_DIR / "areas",
    WIKI_DIR / "resources",
    WIKI_DIR / "archives",
    EMBEDDINGS_DIR,
    LOGS_DIR,
]


def ensure_directories() -> None:
    """Create project directories if they do not exist."""
    for directory in REQUIRED_DIRS:
        directory.mkdir(parents=True, exist_ok=True)


ensure_directories()
