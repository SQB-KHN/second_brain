"""SecondSelf shared configuration — paths, thresholds, and API settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.resolve()
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_ASSETS_DIR = RAW_DIR / "assets"
WIKI_DIR = DATA_DIR / "wiki"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
LOGS_DIR = ROOT / "logs"
GRAPH_FILE = DATA_DIR / "graph.json"
META_FILE = DATA_DIR / "meta.json"
LEGACY_META_FILE = RAW_DIR / "meta.json"
PIPELINE_LOG = LOGS_DIR / "pipeline.log"

SIMILARITY_THRESHOLD = 0.82
RAG_TOP_K = 5
MIN_RETRIEVAL_SCORE = 0.5
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

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
