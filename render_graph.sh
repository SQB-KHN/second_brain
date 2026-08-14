#!/usr/bin/env bash
# Render graph.html from graph.json.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -f .venv/bin/python ]]; then
  echo "Virtual env not found. Set up first:"
  echo "  cd \"$ROOT\""
  echo "  python3 -m venv .venv"
  echo "  source .venv/bin/activate"
  echo "  pip install -r requirements.txt"
  exit 1
fi

exec .venv/bin/python render_graph.py "$@"
