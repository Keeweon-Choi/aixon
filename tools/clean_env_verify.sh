#!/usr/bin/env bash
# Clean-environment verification: fresh clone (committed files only), fresh `npm ci` and venv, then
# `make verify` on 2 CPU cores at low priority (shared PC).
# Usage: tools/clean_env_verify.sh <source repo> <commit> [target dir]
set -euo pipefail
SRC=${1:?source repository}
COMMIT=${2:?commit}
DEST=${3:-$HOME/wt/aixon-clean}
rm -rf "$DEST"
git clone -q "$SRC" "$DEST"
cd "$DEST"
git checkout -q "$COMMIT"
taskset -c 0,1 nice -n 10 npm ci --no-audit --no-fund
# uv-managed Python only (no Anaconda, no system site packages); requirements-dev.txt is compiled by uv
UV=${UV:-$HOME/.local/bin/uv}
"$UV" venv -q --python 3.12 .venv
"$UV" pip install -q --python .venv/bin/python -r requirements-dev.txt
echo "[clean] commit $(git rev-parse --short HEAD), node $(node --version), $(.venv/bin/python --version)"
# Playwright browsers come from ~/.cache/ms-playwright (install with `npx playwright install chromium`).
taskset -c 0,1 nice -n 10 make verify
echo "[clean] verify finished; run dir: $(ls -d artifacts/verification/runs/* | tail -1)"
