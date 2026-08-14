#!/usr/bin/env bash
# Run classify.py with the project virtualenv (avoids ModuleNotFoundError).
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

exec .venv/bin/python classify.py "$@"
