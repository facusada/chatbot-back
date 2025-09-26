#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="$(dirname "${BASH_SOURCE[0]}")/..:${PYTHONPATH:-}"
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
