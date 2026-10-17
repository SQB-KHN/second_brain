"""Shared local/external embedding transport. No network access at import time."""
import json
import urllib.request
from urllib.parse import urlparse

import numpy as np
from config import EMBEDDING_PROVIDER, EMBEDDING_MODEL, OLLAMA_BASE_URL


def model_identity(model=EMBEDDING_MODEL, provider=EMBEDDING_PROVIDER):
    if provider not in ("ollama", "openai"):
        raise ValueError("EMBEDDING_PROVIDER must be ollama or openai")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Embedding model must be nonempty")
    return f"{provider}:{model}"


def validate_vector(value):
    try:
        raw = np.asarray(value)
        if raw.dtype.kind not in "fiu":
            raise ValueError("Invalid embedding response")
        vector = np.asarray(raw, dtype=np.float32)
        if vector.ndim != 1 or not vector.size or not np.isfinite(vector).all() or not np.linalg.norm(vector):
            raise ValueError("Invalid embedding response")
        return vector
    except (TypeError, OverflowError) as exc:
        raise ValueError("Invalid embedding response") from exc


def create_embedder(model=EMBEDDING_MODEL, provider=EMBEDDING_PROVIDER):
    model_identity(model, provider)
    if provider == "openai":
        from link import require_embedding_api_key
        client = require_embedding_api_key().with_options(max_retries=0)
        def embed(text):
            return validate_vector(client.embeddings.create(model=model, input=text).data[0].embedding)
        return embed
    # Local approval exemption is strictly limited to loopback HTTP. No redirects
    # or environment proxy can silently send note text to an external server.
    url = urlparse(OLLAMA_BASE_URL)
    if (url.scheme != "http" or url.hostname not in ("localhost", "127.0.0.1", "::1")
            or url.username or url.password or url.path not in ("", "/") or url.query or url.fragment):
        raise ValueError("OLLAMA_BASE_URL must be a loopback HTTP origin")
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            raise ValueError("Ollama redirects are disabled")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    def embed(text):
        request = urllib.request.Request(OLLAMA_BASE_URL.rstrip("/") + "/api/embed",
            data=json.dumps({"model": model, "input": text, "truncate": False}).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            with opener.open(request, timeout=120) as response:
                payload = json.load(response)
            vectors = payload["embeddings"]
            if not isinstance(vectors, list) or len(vectors) != 1:
                raise ValueError("Invalid Ollama embedding response")
            return validate_vector(vectors[0])
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Ollama embedding failed; check the local server and installed model") from exc
    return embed
