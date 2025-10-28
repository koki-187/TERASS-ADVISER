#!/usr/bin/env bash
set -euo pipefail
# ===== iOS One-Command Build (EAS) =====
cd "$(dirname "$0")/.."
: "${BWS_PROJECT_ID:?BWS_PROJECT_ID 未設定}"
command -v bws >/dev/null || { echo "bws が必要です"; exit 1; }
mkdir -p ios
# Bitwarden の IOS_* だけを書き出して xcconfig 生成（鍵を章本に残さない）
bws secret list --project-id "$BWS_PROJECT_ID" --output env | grep '^IOS_' | sed 's/^IOS_//g' > ios/Config.xcconfig
if command -v npm >/dev/null; then npm i; else yarn; fi
eas build --platform ios --profile production --non-interactive
