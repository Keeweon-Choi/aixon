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
echo "[clean] commit $(git rev-parse --short HEAD), node $(node --version), $(python3 --version)"
taskset -c 0,1 nice -n 10 npm ci --no-audit --no-fund
python3 -m venv .venv
.venv/bin/pip install -q -r requirements-dev.txt
# Playwright browsers come from ~/.cache/ms-playwright (install with `npx playwright install chromium`).
taskset -c 0,1 nice -n 10 make verify
echo "[clean] verify finished; run dir: $(ls -d artifacts/verification/runs/* | tail -1)"
