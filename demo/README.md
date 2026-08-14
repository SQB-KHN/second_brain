# SecondSelf demo bundle

Public deployment data for Streamlit Cloud / Hugging Face Spaces.

- **Notes:** 13 wiki markdown files (sanitized sample corpus)
- **Graph:** 13 nodes, 0 edges in `graph.json`
- **Embeddings:** 0 file(s) in `embeddings/`

Streamlit secrets (see `.streamlit/secrets.toml.example`):

```toml
DEPLOY_MODE = "true"
OPENAI_API_KEY = "sk-..."
```

Refresh locally: `./link.sh && python prepare_deploy.py`
