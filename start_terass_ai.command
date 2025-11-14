#!/usr/bin/env bash
# macOS launcher for TERASS業動サポートAI desktop app.
# This script sets up a Python virtual environment if needed, installs
# dependencies, and runs the Tkinter application. If the Bitwarden CLI
# (`bws`) is installed, secrets are injected automatically. Otherwise
# a normal launch is attempted.

set -euo pipefail

# Determine project root relative to this script
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Create virtual environment if not present
if [ ! -d "$ROOT_DIR/.venv" ]; then
    python3 -m venv "$ROOT_DIR/.venv"
fi

# Activate the virtual environment
source "$ROOT_DIR/.venv/bin/activate"

# Upgrade pip and install dependencies if requirements.txt exists
pip install --upgrade pip
if [ -f "$ROOT_DIR/requirements.txt" ]; then
    pip install -r "$ROOT_DIR/requirements.txt"
else
    pip install pillow
fi

# Define application entry point
APP_FILE="$ROOT_DIR/terass_assistant_with_scenarios.py"
if [ ! -f "$APP_FILE" ]; then
    echo "$APP_FILE not found. Please ensure you are running the script in the correct directory."
    exit 1
fi

# If Bitwarden CLI is available, use it to inject secrets
if command -v bws >/dev/null 2>&1; then
    echo "Injecting secrets via Bitwarden..."
    exec bws run -- python "$APP_FILE"
else
    echo "Bitwarden CLI not found. Running application without secret injection."
    exec python "$APP_FILE"
fi
