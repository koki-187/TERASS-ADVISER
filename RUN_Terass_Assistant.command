#!/usr/bin/env bash
set -euo pipefail
# ===== Desktop One-Tap Start (macOS) =====
cd "$(dirname "$0")"
if ! command -v bws >/dev/null; then osascript -e 'display alert "bws が必要です" message "Bitwarden Secrets Manager CLI をインストールしてください"'; exit 1; fi
if ! command -v python3 >/dev/null; then osascript -e 'display alert "Python3 が必要です" message "python.org からインストールしてください"'; exit 1; fi
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python -m pip -q install --upgrade pip
[ -f requirements.txt ] && pip -q install -r requirements.txt
: "${BWS_PROJECT_ID:?BWS_PROJECT_ID が未設定です。ターミナルで export BWS_PROJECT_ID=... を設定してください。}"
exec bws run --project-id "$BWS_PROJECT_ID" -- python terass_assistant_with_scenarios.py
