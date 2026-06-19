#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR/immune"

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

cat <<'MSG'
SubReparo Immune installed.

Run:
  cd immune
  . .venv/bin/activate
  subreparo-immune scan .
  subreparo-immune inventory create .
  subreparo-immune watch . --once --write-ledger
MSG
