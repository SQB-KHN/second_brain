#!/usr/bin/env bash
# Ask a question over your SecondSelf knowledge base.
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

if [[ $# -eq 0 ]]; then
  echo "Usage: ./ask.sh \"What do I know about PARA?\"" >&2
  exit 1
fi

exec .venv/bin/python ask.py "$@"
